import argparse
import logging
from pathlib import Path
from typing import Callable, Dict
import re
import functools
from collections import Counter
import sys

from science_parse_api.api import parse_pdf

logger = logging.getLogger(__name__)

def _header_pre_processing(header: str) -> str:
    '''
    :param header: Header within a PDF
    :returns: The header, lower cased, whitespace removed from the start and end
              of the header, colons removed throughout, roman numerals removed 
              from the end of the header, numbers from the start and end of the 
              header.
    '''
    header = header.strip().lower()
    # Removes all colons from the header
    header = re.sub(r':', '', header)
    # Removes roman numerals from the end
    header = re.sub(r'\s*(i*v?i*)+$', '', header)
    # removes patterns like 1.2.1 and 12.2 and 12 from the start of the header
    header = re.sub(r'^(\d+.?)+\s*', '', header)
    # removes patterns like 1.2.1 and 12.2 and 12 from the end of the header
    header = re.sub(r'\s*(\d+.?)$', '', header)
    return header

def header_wrapper(func: Callable[[str], bool]) -> Callable[[str], bool]:
    @functools.wraps(func)
    def header_pre_processing(header: str) -> bool:
        header = _header_pre_processing(header)
        return func(header)
    return header_pre_processing

@header_wrapper
def is_declaration_header(header: str) -> bool:
    '''
    :param header: Header within a PDF.
    :returns: True if the header is a declaration statement header.
    '''
    if header=='statement of originality':
        return True
    elif header == 'declaration':
        return True
    elif header == 'declaration of originality':
        return True
    elif header == 'declaration of authorship':
        return True
    return False

def is_declaration_paragraph(paragraph: str) -> bool:
    '''
    Returns True if the paragraph is believed to come from the declaration 
    statement.

    The paragraph is checked to see if one of the following sentences is in 
    the given paragraph and if so then it is believed to be the declaration 
    paragraph. Both these sentences and the given paragraph are lower cased 
    first:

    1. `I certify that the material contained in this dissertation is my own work`
    2. `I certify that the material contained within this dissertation is my own work`
    3. `I hereby declare that the entirety of the content of this dissertation is my own work`
    4. `I certify that this dissertation is my own work and that the material`
    5. `I declare that the work presented in this thesis is, to the best of my 
        knowledge and belief, original and my own work`

    :param paragraph: paragraph of text from a thesis.
    :returns: True if the paragraph is believed to be the declaration statement
              paragraph.
    '''

    declaration_sentences = [("I certify that the material contained in this "
                              "dissertation is my own work"),
                             ("I certify that the material contained within "
                              "this dissertation is my own work"),
                             ("I hereby declare that the entirety of the "
                              "content of this dissertation is my own work"),
                             ("I certify that this dissertation is my own work "
                              "and that the material"),
                             ("I declare that the work presented in this thesis"
                              " is, to the best of my knowledge and belief, "
                              "original and my own work")]

    lower_paragraph = paragraph.lower()
    for declaration_sentence in declaration_sentences:
        if declaration_sentence.lower() in lower_paragraph:
            return True
    return False

@header_wrapper
def is_table_of_contents_header(header: str) -> bool:
    '''
    :param header: Header within a PDF.
    :returns: True if the header is a table of contents header.
    '''
    if header=='contents':
        return True
    elif header == 'table of contents':
        return True
    return False

def remove_table_of_content_info(paragraph: str) -> str:
    '''
    :param paragraph: The text that may contain table of contents like text 
                      within it.
    :returns: The given text but with any table of contents like text removed.

    Example of Table Of Contents like text below:

    Example 1: Abstract. . . . . . .  . 12
    Example 2: Chapter 3 . . . . ..... 5
    
    '''
    new_paragraph = paragraph
    for item_in_table in re.findall(r'(.+(\s*\.){3,}.*\d+\s*)', paragraph):
        new_paragraph = new_paragraph.replace(item_in_table[0], '')
    return new_paragraph

@header_wrapper
def is_acknowledgements_header(header: str) -> bool:
    '''
    :param header: Header within a PDF.
    :returns: True if the header is an acknowledgements header.
    '''
    if header=='acknowledgements':
        return True
    elif header == 'acknowledgement':
        return True
    return False

@header_wrapper
def is_figures_header(header: str) -> bool:
    '''
    :param header: Header within a PDF.
    :returns: True if the header is a list of figures header.
    '''
    if header == 'figures & tables':
        return True
    elif header == 'table of figures':
        return True
    elif header == 'figures':
        return True
    elif header == 'list of figures':
        return True
    return False

@header_wrapper
def is_tables_header(header: str) -> bool:
    '''
    :param header: Header within a PDF.
    :returns: True if the header is a list of tables header.
    '''
    if header == 'tables':
        return True
    elif header == 'table of tables':
        return True
    elif header == 'list of tables':
        return True
    return False

@header_wrapper
def is_bibliography_header(header: str) -> bool:
    '''
    :param header: Header within a PDF.
    :returns: True if the header is the bibliography header.
    '''
    if header == 'bibliography':
        return True
    elif header == 'citations':
        return True
    elif header == 'references':
        return True
    return False

@header_wrapper
def is_appendix_header(header: str) -> bool:
    '''
    :param header: Header within a PDF.
    :returns: True if the header is an appendix header.
    '''
    if 'appendix' in header:
        return True
    elif 'appendices' in header:
        return True
    return False

def is_header_to_remove(header: str) -> bool:
    '''
    :param header: Header within a PDF
    :returns: True if it is a header that is not required. Header that are not 
              required are the following: 1. List of tables, 2. list of figures, 
              3. Acknowledgements, 4. Table of Contents, 
              5. Declaration of originality, 6. Bibliography, and 7. Appendix.
    '''
    if is_tables_header(header):
        return True
    elif is_figures_header(header):
        return True
    elif is_acknowledgements_header(header):
        return True
    elif is_table_of_contents_header(header):
        return True
    elif is_declaration_header(header):
        return True
    elif is_bibliography_header(header):
        return True
    elif is_appendix_header(header):
        return True
    return False

def debug(pdf_directory: Path) -> None:
    '''
    This function through logging outputs various statistics about the PDFs
    that are given in the PDF directory. The statistics are the following:
    
    1. Number of PDFs in the directory.
    2. Number of PDFs without any sections/data.
    3. Number of sections without a header.
    4. Number of sections with a header.
    5. The 20 most common section headers with the count of how often those
       headers occurred.
    6. A list of PDFs that are believed to have no declaration of originality 
       according to that text that can be parsed from the PDF.
    7. A list of headers that were found to be bibliography headers.
    8. A list of headers that were found to be appendix headers.
    9. An ordered list of PDF name and the number of tokens in that PDF that 
       has been extracted as text to be processed. The order is based on 
       ascending number of tokens. Tokenization to performed based on 
       whitespace.

    It will also output:
    
    1. If a file in the directory is not a PDF file.
    2. If the PDF file could not be parsed by Science Parse, which is the 
       system that transforms PDFs to text.
    3. If the PDF contains no text data. E.g. The PDF contains no sections. The
       reason for this is more likely due to the Science Parse system not being 
       able to extract the data rather than the PDF containing no data to 
       extract.

    This function should not be used in production.
    '''
    count = 0
    pdfs_with_no_section = []
    sections_without_headers = 0
    sections_with_headers = 0
    popular_header_names = Counter()
    bibliography_headers = Counter()
    appendix_headers = Counter()

    pdfs_with_no_declaration = []
    pdf_name_number_of_tokens: Dict[str, int] = {}

    for project_pdf in pdf_directory.iterdir(): 
        if project_pdf.suffix != '.pdf':
            error_msg = ('The following file is not a PDF and will not be '
                        'used/parsed, if it is a PDF then please ensure it has '
                        f'a `.pdf` extension/suffix: {project_pdf.name}')
            logger.debug(error_msg)
            continue
        count += 1
        logger.debug(f'Processing: {project_pdf.name}')
        project_pdf = project_pdf.resolve()

        pdf_json = parse_pdf(server_address, project_pdf, port)
        pdf_text = ''
        if pdf_json is None:
            error_msg = ('Science Parse server could not parse the '
                         f'following PDF: {project_pdf.name}')
            logger.info(error_msg)
            pdfs_with_no_section.append(project_pdf.name)
            continue
        if 'sections' not in pdf_json:
            error_msg = ('No data was extracted from the following PDF: '
                        f'{project_pdf.name}')
            logger.info(error_msg)
            pdfs_with_no_section.append(project_pdf.name)
            continue
        contains_declaration = False
        for section in pdf_json['sections']:
            section_header = section.get('heading')
            if section_header is not None:
                if is_declaration_header(section['heading']):
                    contains_declaration = True
                if is_bibliography_header(section_header):
                    bibliography_headers.update([_header_pre_processing(section_header)])
                if is_appendix_header(section_header):
                    appendix_headers.update([_header_pre_processing(section_header)])
                if is_header_to_remove(section['heading']):
                    continue
            section_text = section.get('text')
            if section_text is not None:
                if is_declaration_paragraph(section_text):
                    contains_declaration = True
                    continue
                section_text = remove_table_of_content_info(section_text)
                pdf_text += section_text
            
            if section_header is not None:
                sections_with_headers += 1
                
                popular_header_names.update([_header_pre_processing(section_header)])
            else:
                sections_without_headers += 1
        if not contains_declaration:
            pdfs_with_no_declaration.append(project_pdf)
        pdf_name_number_of_tokens[project_pdf.name] = len(pdf_text.split())

    logger.info(f'Number of PDFs in the directory: {count}')
    logger.info(f'Number of PDFs without any sections/data: {len(pdfs_with_no_section)}')
    logger.info(f'Number of sections without a header: {sections_without_headers}')
    logger.info(f'Number of sections with a header: {sections_with_headers}')
    logger.info('\nThe 20 most popular header names (header names have been '
                'normalised/pre-processed to remove colons and numbers '
                f'etc.): {sections_with_headers}')
    for header, count in popular_header_names.most_common(20):
        logger.info(f'Header: {header}: and Count: {count}')

    logger.info('\nPDFs with what is believed to have no declaration:')
    for pdf_name in pdfs_with_no_declaration:
        logger.info(pdf_name)
    logger.info('\nHeaders that were found to be bibliography headers:')
    for header, count in bibliography_headers.items():
        logger.info(f'Bibliography Header: {header} and Count: {count}')
    logger.info('\nHeader that were found to be appendix headers:')
    for header, count in appendix_headers.items():
        logger.info(f'Appendix Header: {header} and Count: {count}')

    for name, number_tokens in sorted(pdf_name_number_of_tokens.items(), key=lambda x: x[1]):
        logger.info(f'PDF {name}, number of tokens {number_tokens}')

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

if __name__ == '__main__':

    description = ('Given a directory of student thesis in PDF format (1st argument), '
                   'this will export each thesis into text format. Each thesis'
                   ' export will go into the given export folder (2nd argument)'
                   ' in that export folder each thesis will have the same file '
                   'as the original PDF file.\n**BY DEFAULT** this does not '
                   'replace any files that have already been exported into the '
                   'export directory, if you want to replace these files use '
                   'the --replace flag or point it to a new export directory.')
    thesis_directory_help = ('Directory that contains the thesis in PDF '
                             'format, that will be converted into text format')
    export_directory_help = ('Directory that either currently does not exist '
                             'or to a directory that does BUT not a file. '
                             'This direcotry will store the converted '
                             'thesis in their text format')
    debug_help = ('Runs the `debug` function on the given thesis_directory to '
                  'give various statistics on the PDFs in that directory, '
                  'nothing will be exported.')
    replace_help = ('Will convert all thesis into text format and replace '
                    'thesis that currently exist in the exported folder.')
    minimum_number_words_help = ('Minimum number of words, based on whitespace'
                                 ' that a thesis must have for it to be '
                                 'exported.')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('thesis_directory', type=exist_dir_path, 
                        help=thesis_directory_help)
    parser.add_argument('export_directory', type=create_dir_path,
                        help=export_directory_help)
    parser.add_argument('--science-parse-server-url', default="http://127.0.0.1", 
                        type=str, help='The URL to the science parse server')
    parser.add_argument('--science-parse-server-port', default='8080', type=str, 
                        help='The Port to the science parse server')
    parser.add_argument('--debug', action='store_true', help=debug_help)
    parser.add_argument('--replace', action='store_true', help=replace_help)
    parser.add_argument('--min-number-words', type=int, default=1000, 
                        help=minimum_number_words_help)
    args = parser.parse_args()

    server_address: str = args.science_parse_server_url
    port: str = args.science_parse_server_port

    # logs to stdout
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)


    thesis_directory: Path = args.thesis_directory
    replace_files: bool = args.replace
    minimum_number_of_words = args.min_number_words
    
    if args.debug:
        logger.info('Debug Mode: Will not be exporting any data to the '
                    'export direcotry')
        debug(thesis_directory)
    else:
        export_directory: Path = args.export_directory

        number_of_non_pdf_files = 0
        number_of_pdfs_that_could_not_be_parsed = 0
        number_of_pdfs_that_contain_no_data = 0
        number_of_pdfs_less_than_min_words = 0
        number_of_files_in_thesis_directory = 0
        number_of_files_replaced = 0
        number_of_files_exported = 0

        for _pdf in thesis_directory.iterdir():
            number_of_files_in_thesis_directory += 1
            if _pdf.suffix != '.pdf':
                error_msg = ('The following file is not a PDF and will not be '
                            'used/parsed, if it is a PDF then please ensure it has '
                            f'a `.pdf` extension/suffix: {_pdf.name}')
                logger.debug(error_msg)
                number_of_non_pdf_files += 1
                continue
            # Check before processing if the file already exists.
            export_file_path = Path(export_directory, f'{_pdf.stem}.txt')
            if not replace_files and export_file_path.exists():
                continue
            
            logger.info(f'Processing: {_pdf.name}')
            pdf_json = parse_pdf(server_address, _pdf, port)

            if pdf_json is None:
                error_msg = ('Science Parse server could not parse the '
                             f'following PDF: {_pdf.name}')
                logger.debug(error_msg)
                number_of_pdfs_that_could_not_be_parsed += 1
                continue

            if 'sections' not in pdf_json:
                error_msg = ('Science Parse could not extract any text from the'
                             f' following PDF: {_pdf.name}')
                logger.info(error_msg)
                number_of_pdfs_that_contain_no_data += 1
                continue
            
            pdf_text = ''
            for section in pdf_json['sections']:
                section_header = section.get('heading')
                # Skip sections for headers that are not of interest
                if section_header is not None:
                    if is_header_to_remove(section['heading']):
                        continue
                section_text = section.get('text')
                if section_text is not None:
                    # Skip text that is likely a declaration of originality
                    if is_declaration_paragraph(section_text):
                        continue
                    # Remove text that is similar in format to table of
                    # contents text
                    section_text = remove_table_of_content_info(section_text)
                    pdf_text += section_text
            pdf_text = pdf_text.strip()
            if pdf_text:
                number_words = len(pdf_text.split())
                if number_words < minimum_number_of_words:
                    error_msg = (f'PDF contains {number_words} words which is '
                                 'fewer than the minimum of '
                                 f'{minimum_number_of_words} words: {_pdf.name}')
                    logger.info(error_msg)
                    number_of_pdfs_less_than_min_words += 1
                    continue

                if replace_files and export_file_path.exists():
                    number_of_files_replaced += 1

                with export_file_path.open('w') as export_file:
                    export_file.write(pdf_text)
                    number_of_files_exported += 1
            else:
                number_of_pdfs_that_contain_no_data += 1
                error_msg = ('Science Parse could not extract any text from the'
                             f' following PDF: {_pdf.name}')
                logger.info(error_msg)
        
        logger.debug('\n')
        logger.debug('Number of files that were not PDFs in the '
                     f'thesis directory: {number_of_non_pdf_files}')
        logger.debug('Number of PDF files that could not be parsed by the '
                     f'Science Parse server: {number_of_pdfs_that_could_not_be_parsed}')
        logger.debug('Number of PDF files that Science Parse could not extract '
                     f'any text from: {number_of_pdfs_that_contain_no_data}')
        logger.debug('Number of PDF files that contain less than the minimum '
                     'number of words/tokens: '
                     f'{number_of_pdfs_less_than_min_words}')
        logger.debug('Total number of files in the thesis directory: '
                     f'{number_of_files_in_thesis_directory}')
        logger.debug('Number of files replaced in the export directory: '
                     f'{number_of_files_replaced}')
        logger.debug('Number of files exported to the export directory: '
                     f'{number_of_files_exported}')
        