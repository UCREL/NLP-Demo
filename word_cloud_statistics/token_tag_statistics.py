import argparse
import json
from collections import Counter, defaultdict
import logging
from pathlib import Path
from time import sleep
import sys
from typing import List, Dict, Any
import typing
import tempfile
import os

from ucrel_api.api import UCREL_API, UCREL_Doc

DETERMINER_TAGS = set("""
DA DA1 DA2 DAR DAT DB DB2 DD DD1 DD2 DDQ DDQGE DDQV
""".split())

DIGIT_TAGS = set("""
FO MC MC1 MC2 MCGE MCMC MD MF
""".split())

# Taken from SpaCy:
# https://github.com/explosion/spaCy/blob/master/spacy/lang/char_classes.py
PUNCTUATION_SYMBOLS = set("""
.. … …… , : ; ! ? ¿ ؟ ¡ ( ) [ ] { } < > _ # * & 。 ？ ！ ， 、 ； ： ～ · । ، ۔ ؛ ٪ % 
' " ” “ ` ‘ ´ ’ ‚ , „ » « 「 」 『 』 （ ） 〔 〕 【 】 《 》 〈 〉 
- – — -- --- —— ~ 
$ £ € ¥ ฿ US$ C$ A$ ₽ ﷼ ₴
""".split())

# The stop words have come from SpaCy, reference:
# https://github.com/explosion/spaCy/blob/master/spacy/lang/en/stop_words.py
STOP_WORDS = set(
    """
a about above across after afterwards again against all almost alone along
already also although always am among amongst amount an and another any anyhow
anyone anything anyway anywhere are around as at
back be became because become becomes becoming been before beforehand behind
being below beside besides between beyond both bottom but by
call can cannot ca could
did do does doing done down due during
each eight either eleven else elsewhere empty enough even ever every
everyone everything everywhere except
few fifteen fifty first five for former formerly forty four from front full
further
get give go
had has have he hence her here hereafter hereby herein hereupon hers herself
him himself his how however hundred
i if in indeed into is it its itself
keep
last latter latterly least less
just
made make many may me meanwhile might mine more moreover most mostly move much
must my myself
name namely neither never nevertheless next nine no nobody none noone nor not
nothing now nowhere
of off often on once one only onto or other others otherwise our ours ourselves
out over own
part per perhaps please put
quite
rather re really regarding
same say see seem seemed seeming seems serious several she should show side
since six sixty so some somehow someone something sometime sometimes somewhere
still such
take ten than that the their them themselves then thence there thereafter
thereby therefore therein thereupon these they third this those though three
through throughout thru thus to together too top toward towards twelve twenty
two
under until up unless upon us used using
various very very via was we well were what whatever when whence whenever where
whereafter whereas whereby wherein whereupon wherever whether which while
whither who whoever whole whom whose why will with within without would
yet you your yours yourself yourselves
""".split()
)

contractions = ["n't", "'d", "'ll", "'m", "'re", "'s", "'ve"]
STOP_WORDS.update(contractions)

for apostrophe in ["‘", "’"]:
    for stopword in contractions:
        STOP_WORDS.add(stopword.replace("'", apostrophe))


def path_type(_file_path: str) -> Path:
    file_path = Path(_file_path)
    if file_path.is_dir():
        raise TypeError(f'The path given {_file_path} cannot be a directory.')
    return Path(_file_path).resolve()

def exist_dir_path(_dir_string: str) -> Path:
    _dir_path = Path(_dir_string)
    if not _dir_path.is_dir():
        raise TypeError(f'The path given {_dir_string} is not a directory. '
                        'Require a file path to a directory.')
    return _dir_path

def create_dir_path(_dir_string: str) -> Path:
    _dir_path = Path(_dir_string)
    if _dir_path.exists():
        if not _dir_path.is_dir():
            raise TypeError(f'The path given {_dir_string} is not a directory. '
                            'Require a file path to a directory or to a '
                            'directory that currently does not exist.')
    else:
        _dir_path.mkdir(parents=True)
    return _dir_path

def create_output_file(_file_path: Path, data: Dict[str, Dict[str, Any]]) -> None:
    '''
    :param _file_path: File to store the data in JSON format.
    :param data: A dictionary like object.
    :returns: None
    '''
    logger.info(f'Writing token/tag information to: {_file_path.name}')
    
    with _file_path.open('w') as _file:
         json.dump(data, _file)

def read_frequency_file(_file_path: Path, lower_case: bool) -> Dict[str, int]:
    '''
    :param _file_path: File that will contains a TSV/space delimited like file.
                       The file should only have two columns. The first column
                       containing the word/tag and the second the frequency.
                       The first row is reserved for the word 
                       `Total` and the sum of all frequencies in the first and 
                       second column respectively.
    :param lower_case: To lower case the word/tag.
    :returns: A dictionary of word and frequency from the information in the 
              file. It ignores the first row e.g. the `Total` is not in the 
              returned dictionary.
    '''
    frequency_counter = dict()
    with _file_path.open('r', newline='') as csv_file:
        for index, line in enumerate(csv_file):
            # Skip the first line as it contains the total frequency count 
            # which we are not interested in.
            if index == 0:
                continue
            line = line.strip()
            word, frequency = line.split()
            if word in frequency_counter:
                raise ValueError(f'This word {word} has already occurred in the '
                                 'frequency list, all words in the frequency '
                                 'list should be unique.')
            frequency_counter[word] = int(frequency)
    
    return frequency_counter

def sigeff_input_file(_file_path: Path, target_frequency_count: Dict[str, int], 
                      reference_frequency_count: Dict[str, int], 
                      min_target_frequency_count: int = 5) -> None:
    '''
    This first removes all of the words in the reference and target frequency 
    count that are less than `min_target_frequency_count`. Then removes all of 
    the words in the reference frequency count which are not in the target 
    frequency count. 
    
    This then writes the following for each word in the `target_frequency_count`:

    `WORD\t{target_frequency_count_for_word}\t{reference_frequency_count_for_word}\n`

    This is written to the given `_file_path`. The top line is reserved for the 
    following line:
    
    `Total\t{sum of all frequencies in this target column}\t
     {sum of all frequencies in this reference column}\n`

    This file will then be in the format required for the SigEff C script. An 
    example of this file format can be seen below (acknowledge Paul Rayson):

    TOTAL	10000	100000
    Word1	1500	15000
    Word2	340	2500
    Word3	200	2500
    Word4	7	0
    Word5	654	654
    Word6	89	536

    :param _file_path: To write the sigeff data too that will be used as input 
                       to the sigeff C script.
    :param target_frequency_count: The token/tag frequency counts from the 
                                   corpus you are interested in.
    :param reference_frequency_count: The token/tag frequency counts from the  
                                      reference corpus e.g. BNC. 
    :param min_target_frequency_count: Minimum frequency count of a word/tag.
                                       Any word/tag less than this is removed 
                                       from the reference/target frequency 
                                       dictionaries.
    '''
    reduced_target_frequency_count = {word: freq for word, freq in target_frequency_count.items() 
                                      if freq>=min_target_frequency_count}
    reduced_reference_frequency_count = {word: freq for word, freq in reference_frequency_count.items()
                                         if word in reduced_target_frequency_count}
    total_target_frequency_count = sum([freq for freq in reduced_target_frequency_count.values()])
    total_reference_frequency_count = sum([freq for freq in reduced_reference_frequency_count.values()])
    
    with _file_path.open('w') as _file:
        _file.write(f'Total\t{total_target_frequency_count}\t{total_reference_frequency_count}\n')
        for word, target_frequency in reduced_target_frequency_count.items():
            reference_frequency = reduced_reference_frequency_count.get(word, 0)
            _file.write(f'{word}\t{target_frequency}\t{reference_frequency}\n')

def _get_significant_key_words(file_lines: List[str], 
                               significance_level: float = 0.05
                               ) -> Dict[str, Dict[str, Any]]:
    '''
    :param file_lines: The output of the function readlines on the file that 
                       contains the result from running the SigEff C script.
    :param significance_level: The level of significance. 0.05 = 95% 0.01 = 99%.
                               significance levels allowed are: 0.05, 0.01,
                               0.001, and 0.0001.
    :returns: All of the words that are significantly more likely to occur in the 
              target corpus than the reference at the given significance level. 
              The words are the keys and the values are a dictionary of statistics
              with the statistic name as key with it's associated value e.g. 
              `log-likelihood` : 12.3
    '''
    significant_words = {}
    log_likelihood_sig_value_mapper = {0.05: 3.84, 0.01: 6.63, 0.001: 10.83,
                                       0.0001: 15.13}
    log_likelihood_sig_value = log_likelihood_sig_value_mapper[significance_level]
    for line_index, line in enumerate(file_lines):
        # The first line only contains the total and the second are the headers
        if line_index == 0 or line_index == 1:
            continue
        line_data = line.split()
        # Number of fields should be 13 after splitting on whitespace
        number_fields = len(line_data)
        number_error = (f'number of fields on line {line_index} is {number_fields}'
                        f' when it should be at least 13.')
        assert number_fields > 12, number_error
        # Only want words that are significantly more likely to occur in the 
        # target than the reference corpus.
        higher_symbol = line_data[5]
        if higher_symbol != '+':
            continue
        # Checking if the word is significant
        log_likelihood = float(line_data[6])
        if log_likelihood < log_likelihood_sig_value:
            continue
        log_ratio = float(line_data[11])
        frequency_in_target_corpus = int(line_data[1])
        relative_frequency_in_target_corpus = float(line_data[2])
        word = line_data[0]
        significant_words[word] = {'Log Likelihood': log_likelihood, 
                                   'Log Ratio': log_ratio, 
                                   'Frequency': frequency_in_target_corpus,
                                   'Relative Frequency (%)': relative_frequency_in_target_corpus}
    return significant_words

def extract_significant_key_words(target_counter: Dict[str, int], 
                                  reference_counter: Dict[str, int],
                                  sigeff_binary_file_path: Path,
                                  semtag_summary_file_path: Path,
                                  significance_level: float = 0.05,
                                  min_target_frequency_count: int = 5
                                  ) -> Dict[str, Dict[str, Any]]:
    '''
    :param target_counter: The frequency counts of the token/tag from the corpus 
                           you are interested in.
    :param reference_counter: The frequency counts of the token/tag from the  
                              reference corpus e.g. BNC.
    :param sigeff_binary_file_path: File path to the SigEff C binary
    :param semtag_summary_file_path: File path to the USAS tag summary file. 
                                     This is used by the SigEff binary.
    :param significance_level: The level of significance. 0.05 = 95% 0.01 = 99%.
                               significance levels allowed are: 0.05, 0.01,
                               0.001, and 0.0001.
    :param min_target_frequency_count: Minimum frequency count of a token/tag 
                                       in the target counter to be considered 
                                       in the token/tag significance list that 
                                       is returned.
    :returns: All of the token/tags that are significantly more likely to occur in the 
              target corpus than the reference at the given significance level. 
              The words are the keys and the values are a dictionary of statistics
              with the statistic name as key with it's associated value e.g. 
              `log-likelihood` : 12.3
    '''
    with tempfile.NamedTemporaryFile('w+') as a_file:
        temp_file_path = Path(a_file.name)
        sigeff_input_file(temp_file_path, target_counter, reference_counter, 
                          min_target_frequency_count=min_target_frequency_count)

        with tempfile.NamedTemporaryFile('w+') as result_file:
            run_command = [f"{str(sigeff_binary_file_path)}", "-X", 
                           f"{str(semtag_summary_file_path)}", "<", 
                           f"{a_file.name}", ">", f"{result_file.name}"]
            os.system(' '.join(run_command))
            lines = result_file.readlines()
            return _get_significant_key_words(lines, significance_level)

def USAS_tag_to_label(usas_mapper: Dict[str, str], tag: str) -> str:
    '''
    :param usas_mapper: Maps USAS tags to labels e.g. T to Time.
    :param tag: USAS tag to convert to label.
    :returns: The label for the given USAS tag. This process performs removal 
              of the USAS special symbols like `+` and `%` to find the relevant 
              USAS label. It also adds these special specials symbols back on 
              to the label so that it is possible to convert the returned label 
              back to it's original tag.
    '''
    # For the list of symbols see page 2 of the following guide:
    # http://ucrel.lancs.ac.uk/usas/usas_guide.pdf
    other_usas_symbols = set(['%', '@', 'f', 'm', 'c', 'n', 'i', '+', '-'])
    # Some USAS tags are not in the USAS tags to labels list as they 
    # can have additional + or - sings at the end of the USAS tags. 
    # Therefore we remove the + or - until we find the label.
    temp_tag = tag
    chars_removed = ''
    while temp_tag not in usas_mapper:
        last_tag_char = temp_tag[-1]
        if last_tag_char in other_usas_symbols:
            chars_removed += last_tag_char
            temp_tag = temp_tag[:-1]
        else:
            break
    else:
        label = usas_mapper[temp_tag]
        if chars_removed:
            label += f' - {chars_removed}'
        return label
    raise ValueError(f'Special symbol in the USAS tag {tag} that is not one '
                     f'of the special symbols: {other_usas_symbols} or a '
                     'USAS tag itself.')


if __name__ == '__main__':

    description = ('Given a directory of texts (1st argument) each text will '
                   'be processed by the USAS tool chain and the result cached'
                   ' (2nd argument). The Tokens and USAS tags that are used '
                   'significantly more in the given texts compared to the '
                   'reference texts will be stored with their metadata in the '
                   'token and usas output files (3rd and 4th arguments).')
    text_directory_help = ('Directory that contains files of plain text '
                           'that is to be analysed')
    usas_caching_directory_help = ('Directory that stores for each exported text'
                                   ' the output of the USAS tagging in JSON '
                                   'format.')
    token_output_path_help = ('File path to store the tokens that occur statistically'
                              'more often in the given texts compared to the '
                              'reference. The file will be in JSON format '
                              'whereby all tokens are stored in one JSON object'
                              ' the names/keys are the tokens and each value '
                              'is another JSON object with the following name '
                              'and values: 1. `Log Likelihood`, 2. `Log Ratio,`'
                              ' 3.`Frequency`, 4. `Relative Frequency`, and '
                              '5. `Common associated USAS tags (%%)`. Only '
                              'the 5th value is not an int or float.')
    usas_output_path_help = ('File path to store the USAS tags that occur statistically'
                             'more often in the given texts compared to the '
                             'reference. The file will be in JSON format '
                             'whereby all tags are stored in one JSON object'
                             ' the names/keys are the tags and each value '
                             'is another JSON object with the following name '
                             'and values: 1. `Log Likelihood`, 2. `Log Ratio,`'
                             ' 3.`Frequency`, 4. `Relative Frequency`. All these '
                             'values are either a float or an int.')
    reference_token_frequency_path_help = ('File Path to a reference of the '
                                           'token_frequency_path e.g. '
                                           'BNC sample word frequency.'
                                           'It should be in the same file '
                                           'format as the token_frequency_path'
                                           ' will be.')
    reference_usas_tag_frequency_path_help = ('File Path to a reference of the '
                                              'usas_frequency_path e.g. '
                                              'BNC Semantic tag frequency.'
                                              'It should be in the same file '
                                              'format as the usas_frequency_path'
                                              ' will be.')
    sigeff_binary_file_path_help = ('File path to the SigEff C binary')
    semtag_summary_file_path_help = ('File path to the USAS tag summary file. '
                                     'This is used by the SifEff binary. This '
                                     'has to be in UTF-8 or ASCII encoding.')
    replace_usas_cache_help = ('If the `usas_caching_directory` exists will '
                               're-run the USAS tagging and store the new '
                               'results in that directory.')
    remove_punctuation_help = ('Do not include punctuation in the frequency lists.')
    remove_determiners_help = ('Do not include determiners in the frequency lists.')
    remove_stop_words_help = ('Do not include stop words in the frequency lists. '
                              'This has come from SpaCy: '
                              'https://github.com/explosion/spaCy/blob/master/spacy/lang/en/stop_words.py')
    remove_digits_help = ('Do not include any standalone digits in the '
                          'frequency lists. This is determined by the POS tag.'
                          'It also includes any formula tokens like > or <')
    significance_help = ('The level of significance, that the token/tags are '
                         'significantly more likely to occur in the target '
                         'corpus compared to the reference corpus. 0.05 = 95%% '
                         '0.01 = 99%%. significance levels allowed '
                         'are: 0.05, 0.01, 0.001, and 0.0001.')
    minimum_token_frequency_help = ('The minimum frequency per token/tag that'
                                    ' the token has to occur in the target '
                                    'corpus for it to be considered a '
                                    'significant word compared to the '
                                    'reference corpus. This is to remove low '
                                    'frequency tokens in the target corpus.')
    USAS_tags_to_labels_help = ('When writing the USAS tags to files it will '
                                'convert the tags to their labels e.g. the '
                                'tag T will become Time.')
    time_to_wait_between_usas_api_calls_help = ('Time to wait, in seconds, '
                                                'between calls to the USAS API,'
                                                ' their is one call per text '
                                                'file in the `text_directory`.')
    
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('text_directory', type=exist_dir_path,
                        help=text_directory_help)
    parser.add_argument('usas_caching_directory', type=create_dir_path,
                        help=usas_caching_directory_help)
    parser.add_argument('token_output_path', type=path_type, 
                        help=token_output_path_help)
    parser.add_argument('usas_output_path', type=path_type, 
                        help=usas_output_path_help)
    parser.add_argument('reference_token_frequency_path', type=path_type,
                        help=reference_token_frequency_path_help)
    parser.add_argument('reference_usas_tag_frequency_path', type=path_type,
                        help=reference_usas_tag_frequency_path_help)
    parser.add_argument('sigeff_binary_file_path', type=path_type, 
                        help=sigeff_binary_file_path_help)
    parser.add_argument('semtag_summary_file_path', type=path_type, 
                        help=semtag_summary_file_path_help)
    parser.add_argument('--replace-usas-cache', action='store_true', 
                        help=replace_usas_cache_help)
    parser.add_argument('--remove-punctuation', action='store_true', 
                        help=remove_punctuation_help)
    parser.add_argument('--remove-determiners', action='store_true', 
                        help=remove_determiners_help)
    parser.add_argument('--remove-stop-words', action='store_true', 
                        help=remove_stop_words_help)
    parser.add_argument('--remove-digits', action='store_true', 
                        help=remove_digits_help)
    parser.add_argument('--lower-case', action='store_true', 
                        help='Lower case all words')
    parser.add_argument('--significance-level', default=0.05, type=float,
                        choices=[0.05, 0.01, 0.001, 0.0001], 
                        help=significance_help)
    parser.add_argument('--minimum-token-frequency', default=5, type=int,
                        help=minimum_token_frequency_help)
    parser.add_argument('--USAS-tags-to-labels', action='store_true',
                        help=USAS_tags_to_labels_help)
    parser.add_argument('--time-to-wait-between-usas-api-calls', default=10, 
                        type=int, help=time_to_wait_between_usas_api_calls_help)
    args = parser.parse_args()

    text_directory: Path = args.text_directory
    usas_caching_directory: Path = args.usas_caching_directory
    
    # logs to stdout
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    ucrel_api = UCREL_API('a.moore@lancaster.ac.uk', 
                          'http://ucrel-api.lancaster.ac.uk')

    sleep_time: int = args.time_to_wait_between_usas_api_calls
    logger.info(f'Tagging text and caching to {usas_caching_directory}')
    for _file_path in text_directory.iterdir():
        usas_file_path = Path(usas_caching_directory, f'{_file_path.stem}.json')
        if usas_file_path.exists() and not args.replace_usas_cache:
            continue
        
        with _file_path.open('r') as _file:
            text = _file.read()
            
            logger.info(f'Tagging text for: {_file_path.name}')
            ucrel_doc = ucrel_api.usas(text)
            logger.info(f'Tagging finished')
            with usas_file_path.open('w') as usas_file:
                usas_file.write(ucrel_doc.to_json())
            logger.info('Tagged data has been written and cached to '
                        f'{usas_file_path.name}')
            
            logger.info(f'Waiting {sleep_time}s between calls of the UCREL API,'
                    ' to ensure that we are not calling the API to frequently.')
            sleep(sleep_time)
    logger.info('Tagging completed and all tagged data has been cached to '
                f'the {usas_caching_directory} directory.')
    
    # Flags that control what tokens are added
    remove_punctuation: bool = args.remove_punctuation
    remove_determiners: bool = args.remove_determiners
    remove_stop_words: bool = args.remove_stop_words
    remove_digits: bool = args.remove_digits
    lower_case: bool = args.lower_case
    
    token_counter = Counter()
    token_usas_tag: Dict[str, typing.Counter[str]] = defaultdict(lambda: Counter())
    usas_counter = Counter()
    for _file_path in text_directory.iterdir():
        usas_file_path = Path(usas_caching_directory, f'{_file_path.stem}.json')
        with usas_file_path.open('r') as usas_file:
            ucrel_doc = UCREL_Doc.from_json(usas_file.read())

            token_texts: List[str] = []
            token_usas_tags: List[str] = []
            for token in ucrel_doc:

                token_text = token.text
                usas_tag = token.usas_tag
                pos_tag = token.pos_tag
                lemma = token.lemma
                
                if lower_case:
                    token_text = token_text.lower()
                
                if remove_punctuation and token_text in PUNCTUATION_SYMBOLS:
                    continue
                if lemma is not None:
                    if remove_punctuation and lemma == 'PUNC':
                        continue
                if pos_tag is not None:
                    if remove_determiners and pos_tag in DETERMINER_TAGS:
                        continue
                    if remove_digits and pos_tag in DIGIT_TAGS:
                        continue
                if remove_stop_words and token_text.lower() in STOP_WORDS:
                    continue

                token_texts.append(token_text)
                if usas_tag is not None:
                    all_usas_tags = usas_tag.split('/')
                    for a_tag in all_usas_tags:
                        token_usas_tags.append(a_tag)
                    if all_usas_tags:
                        token_usas_tag[token_text].update(all_usas_tags)
            token_counter.update(token_texts)
            usas_counter.update(token_usas_tags)
    
    dict_token_counter = dict(token_counter)
    dict_usas_counter = dict(usas_counter)

    # Reference token and usas counts
    reference_token_frequency_path: Path = args.reference_token_frequency_path
    bnc_token_counter = read_frequency_file(reference_token_frequency_path, lower_case)
    reference_usas_tag_frequency_path: Path = args.reference_usas_tag_frequency_path
    bnc_usas_counter = read_frequency_file(reference_usas_tag_frequency_path, False)

    # Extraction of significant token and tags
    sigeff_binary_file_path: Path = args.sigeff_binary_file_path
    semtag_summary_file_path: Path = args.semtag_summary_file_path
    significance_level: float = args.significance_level
    minimum_token_frequency: int = args.minimum_token_frequency

    significant_tokens = extract_significant_key_words(dict_token_counter, bnc_token_counter, 
                                                       sigeff_binary_file_path, semtag_summary_file_path, 
                                                       significance_level, minimum_token_frequency)
    # Add the most and second most frequent usas tags to the token information
    for token, token_values in significant_tokens.items():
        _usas_tags = token_usas_tag[token]
        num_usas_tags = float(sum(_usas_tags.values()))
        # Normalize the number of times the USAS tag occurred by the number of 
        # USAS tags for that token.
        tag_occurrence = [(tag, (float(value) / num_usas_tags) * 100)
                          for tag, value in _usas_tags.most_common(2)]
        token_values['Common associated USAS tags (%)'] = tag_occurrence

    significant_tags = extract_significant_key_words(dict_usas_counter, bnc_usas_counter, 
                                                     sigeff_binary_file_path, semtag_summary_file_path, 
                                                     significance_level, minimum_token_frequency)
    # Remove the Z99 and Z9 SemTags
    temp_sig_tags = {tag: value for tag, value in significant_tags.items() if 'Z9' not in tag}
    significant_tags = temp_sig_tags

    if args.USAS_tags_to_labels:
        temp_sig_tags = {}

        usas_tag_label: Dict[str, str] = {}
        with semtag_summary_file_path.open('r') as semtag_file:
            for line in semtag_file:
                if not line.strip():
                    continue
                tag, label = line.split('\t')
                tag = tag.strip()
                label = label.strip()
                usas_tag_label[tag] = label

        for tag, values in significant_tags.items():
            label = USAS_tag_to_label(usas_tag_label, tag)
            if label in temp_sig_tags:
                raise ValueError(f'This label {label} appears twice in the '
                                 'significantly occuring USAS labels.')
            temp_sig_tags[label] = values
        significant_tags = temp_sig_tags

        for token, values in significant_tokens.items():
            token_usas_tags = values['Common associated USAS tags (%)']
            if not token_usas_tags:
                continue
            _token_usas_tags = []
            for tag, value in token_usas_tags:
                label = USAS_tag_to_label(usas_tag_label, tag)
                _token_usas_tags.append((label, value))
            values['Common associated USAS tags (%)'] = _token_usas_tags
    create_output_file(args.token_output_path, significant_tokens)
    create_output_file(args.usas_output_path, significant_tags)
    
    
    
