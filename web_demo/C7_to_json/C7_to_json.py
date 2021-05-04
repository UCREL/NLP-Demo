import argparse
import json
from pathlib import Path
from typing import Dict

def path_exists(file_path: str) -> Path:
    _fp = Path(file_path)
    if not _fp.exists():
        raise FileNotFoundError(f'File {file_path} does not exist')
    return _fp.resolve()

def path_type(file_path: str) -> Path:
    return Path(file_path)

if __name__ == '__main__':

    description = '''Given a file path (1st argument) that contains POS tag as 
                     the first word and all other words are the label associated 
                     with that POS tag, like the list of tags and labels at 
                     the following URL: 
                     http://ucrel.lancs.ac.uk/claws7tags.html it will write 
                     to a new JSON file at the 2nd argument's file path a 
                     dictionary object of POS tags as keys and the associated 
                     label as the value.''' 
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('tag_label_file_path', type=path_exists)
    parser.add_argument('tag_label_json_path', type=path_type)
    args = parser.parse_args()
    
    tag_label_file_path = args.tag_label_file_path
    tag_label_json_path = args.tag_label_json_path

    tag_label_dict: Dict[str, str] = {}
    with tag_label_file_path.open('r') as _fp:
        for line in _fp:
            line = line.strip()
            if not line:
                continue
            tag_label = line
            if '(' in tag_label:
                tag_label = tag_label[:tag_label.find('(')].strip()
            tag_label = tag_label.split()
            tag = tag_label[0]
            label = ' '.join(tag_label[1:]).rstrip(' -,')
            tag_label_dict[tag] = label
    with tag_label_json_path.open('w') as _fp:
        json.dump(tag_label_dict, _fp)
