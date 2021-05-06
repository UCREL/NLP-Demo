import argparse
import logging
import json
from pathlib import Path
from typing import Dict, Optional

from ucrel_api.api import UCREL_API

def tag_to_label(tag_to_label_mapper: Dict[str, str], tag: str, 
                 lemma: Optional[str] = None) -> str:
    '''
    This works for both the CLAWS C7 tagset and the USAS tagset.

    Some Exceptions:

    1. If the value of the tag is `...` the return will be `...`
    2. If the value of the lemma (if provided) is `PUNC` then `PUNC` will be 
       returned.

    :param tag_to_label_mapper: Maps tags to labels e.g. T to Time if using a 
                                USAS tagset mapper.
    :param tag: tag to convert to label.
    :param lemma: The lemma that is associated with the tag.
    :returns: The label for the given tag. This process performs removal 
              of special symbols like `+` and `%` from the tag to find the  
              relevant label. It also adds these special specials symbols back on 
              to the label so that it is possible to convert the returned label 
              back to it's original tag.
    '''
    # These are two edge cases.
    if tag == '...':
        return tag
    if lemma is not None:
        if lemma == 'PUNC':
            return lemma
    
    # For the list of symbols see page 2 of the following guide:
    # http://ucrel.lancs.ac.uk/usas/usas_guide.pdf
    # and the ditto tag guidelines for the CLAWS C7 tagset:
    # http://ucrel.lancs.ac.uk/claws7tags.html
    other_symbols = set(['%', '@', 'f', 'm', 'c', 'n', 'i', '+', '-', '.'])
    ditto_numbers = set([str(number) for number in range(1,10)])
    # For a tag we remove the last symbols until the tag is found in the mapper.
    # If not tag is found in the mapper a ValueError is raised.
    temp_tag = tag
    chars_removed = ''
    while temp_tag not in tag_to_label_mapper:
        last_tag_char = temp_tag[-1]
        if last_tag_char in other_symbols or last_tag_char in ditto_numbers:
            chars_removed += last_tag_char
            temp_tag = temp_tag[:-1]
        else:
            break
    else:
        label = tag_to_label_mapper[temp_tag]
        if chars_removed:
            label += f' - {chars_removed}'
        return label
    error_msg = (f'Special symbol in the USAS tag {tag} that is not one '
                   f'of the special symbols: {other_symbols}, or a ditto '
                   f'number: {ditto_numbers}, or a tag itself.')
    raise ValueError(error_msg)

def path_exists(file_path: str) -> Path:
    _fp = Path(file_path)
    if not _fp.exists():
        raise FileNotFoundError(f'File {file_path} does not exist')
    return _fp.resolve()

def path_type(file_path: str) -> Path:
    return Path(file_path)

if __name__ == '__main__':
    description = '''Given a text file (1st argument) it will process the text 
                  using USAS and output that to the given output file 
                  (2nd argument). In addition to the expected USAS output 
                  (see https://ucrel.github.io/ucrel-python-api/ucrel_doc.html#UCREL_Doc.to_json) 
                  each token will have a POS and USAS label as well as the 
                  tags. The USAS and POS labels are more human readable.'''
    input_file_path_help = ('File path that contains the text to be '
                            'processed by USAS.')
    output_file_path_help = ('File path that will contains the USAS data in '
                             'JSON formatted, whereby all USAS and POS tags '
                             'will include a label field.')
    semtag_summary_file_path_help = ('File path to the USAS tag summary file. '
                                     'This has to be in UTF-8 or ASCII encoding.')
    pos_tag_file_path_help = ('File path to a JSON file that contains an object'
                              ' whereby the keys are tags and the values are '
                              'the associated label for the tag.')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('input_file_path', type=path_exists, 
                        help=input_file_path_help)
    parser.add_argument('output_file_path', type=path_type, 
                        help=output_file_path_help)
    parser.add_argument('semtag_summary_file_path', type=path_exists, 
                        help=semtag_summary_file_path_help)
    parser.add_argument('pos_tag_to_label_json_file_path', type=path_exists, 
                        help=pos_tag_file_path_help)
    args = parser.parse_args()

    input_file_path = args.input_file_path

    api = UCREL_API('a.moore@lancaster.ac.uk', 'http://ucrel-api.lancaster.ac.uk')
    with input_file_path.open('r') as input_fp:
        ucrel_doc = api.usas(input_fp.read())


        usas_tag_label: Dict[str, str] = {}
        semtag_summary_file_path = args.semtag_summary_file_path
        with semtag_summary_file_path.open('r') as semtag_file:
            for line in semtag_file:
                if not line.strip():
                    continue
                tag, label = line.split('\t')
                tag = tag.strip()
                label = label.strip()
                usas_tag_label[tag] = label

        pos_tag_label: Dict[str, str] = {}
        pos_tag_to_label_json_file_path = args.pos_tag_to_label_json_file_path
        with pos_tag_to_label_json_file_path.open('r') as pos_file:
            pos_tag_label = json.load(pos_file)
        for token in ucrel_doc:
            if token.pos_tag is not None:
                token.pos_label = tag_to_label(pos_tag_label, token.pos_tag, token.lemma)
            if token.usas_tag is not None:
                usas_tag = token.usas_tag
                if '/' in usas_tag:
                    usas_tags = [] 
                    for tag in usas_tag.split('/'):
                        usas_tags.append(tag_to_label(usas_tag_label, tag, token.lemma))
                    token.usas_label = '/'.join(usas_tags)
                else:
                    token.usas_label = tag_to_label(usas_tag_label, usas_tag, token.lemma)


        output_file_path = args.output_file_path
        with output_file_path.open('w') as _fp:
            _fp.write(ucrel_doc.to_json())

