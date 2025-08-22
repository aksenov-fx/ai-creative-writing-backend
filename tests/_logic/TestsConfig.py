import os
import csv
from dataclasses import dataclass
from typing import List, Tuple, Any

from tests._logic.utils import read_yaml

from _includes.app.Chat.Generator import Generator
from _includes.app.Chat.Changer import Changer
from _includes.app.Chat.Summarizer import Summarizer
from _includes.app.Chat.Helpers import Helpers

@dataclass
class TestsConfig:
    temp_dir: str
    originals_dir: str
    story_folder: str
    story_folder_path: str

def get_tests_config(path: str):
    yaml_data = read_yaml(path)
    conf = TestsConfig(**yaml_data)

    conf.story_folder_path = os.path.join(conf.temp_dir, conf.story_folder)

    return conf

FUNCTION_MAPPING = {
    'write_scene': Generator.write_scene,
    'custom_prompt': Generator.custom_prompt,
    'regenerate': Generator.regenerate,
    'add_part': Generator.add_part,
    'continue_response': Generator.continue_response,
    'change_part': Changer.change_part,
    'summarize_part': Summarizer.summarize_part,
    'rewrite_selection': Helpers.rewrite_selection,
    'translate': Helpers.translate,
    'explain': Helpers.explain,
}

def get_function(function_name: str):
    return FUNCTION_MAPPING[function_name]

def try_parse_int(value: str) -> int | str:
    try:
        return int(value)
    except ValueError:
        return value

def load_params(csv_file: str) -> List[Tuple[str, str, Any, bool, int | str]]:
    """Load test parameters from CSV file and return as list of tuples."""

    params = []
    csv_path = os.path.join('tests', '_settings', 'Params', 'Chat', csv_file)
    
    with open(csv_path, 'r', newline='', encoding='utf-8') as file:

        reader = csv.DictReader(file)

        for row in reader:
            prompt_type =   row['prompt_type']
            story_file =    row['story_file']
            callback =      get_function(row['function_name'])
            should_pass =   row['should_pass'].lower() == 'true'
            arg =           try_parse_int(row['arg'])

            params.append([prompt_type, story_file, callback, should_pass, arg])
    
    return params

generator_params =    load_params('generator_params.csv')
changer_params =      load_params('changer_params.csv')
summarizer_params =   load_params('summarizer_params.csv')
helper_params =       load_params('helper_params.csv')
