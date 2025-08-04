from dataclasses import dataclass
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from .Utility import Utility
import os, yaml

@dataclass
class ChatConfig:
    system_prompt: str
    introduction: str
    variables: dict
    prompts_structure: dict
    default_endpoint: str
    endpoint: dict
    default_model: str
    model: dict
    temperature: float
    max_tokens: int
    trim_history: bool
    print_messages: bool
    include_reasoning: bool
    separator: str
    interrupt_flag: bool
    print_reasoning: bool
    abbreviations: str
    write_interval: float
    use_summary: bool
    history_path: Path
    summary_path: Path
    prompts_path: Path
    folder_path: Path
    include_previous_part_when_summarizing: bool
    include_previous_part_when_rewriting: bool
    debug: bool
    history_prefix: str

@contextmanager
def override_config(config, **overrides: Any):
    original_values = {}
    for key, value in overrides.items():
        if hasattr(config, key):
            original_values[key] = getattr(config, key)
            setattr(config, key, value)
    
    try:
        yield config
    finally:
        for key, value in original_values.items():
            setattr(config, key, value)

def read_yaml(file_path):
    if os.path.getsize(file_path) == 0 or not os.path.isfile(file_path):
        return {}
    
    return yaml.safe_load(Utility.read_file(file_path))

def parse_frontmatter(file_path):
    if not os.path.isfile(file_path): return {}
    content = Utility.read_file(file_path)
    content = content.split('---\n')[1]
    return yaml.safe_load(content)

def parse_model(frontmatter):
    from _includes import models

    try:
        model_number = int(frontmatter['model'])
        return list(models.values())[model_number - 1]['name']
    except ValueError:
        return frontmatter['model']

def read_config(folder_path):
    from ..config import abbreviations, prompts_structure, variables
    settings_folder = folder_path + '/Settings/'

    # Read values
    new_config =        parse_frontmatter(settings_folder + 'Settings.md')
    new_abbreviations = parse_frontmatter(settings_folder + 'Abbreviations.md')
    new_variables     = parse_frontmatter(settings_folder + 'Variables.md')
    new_prompts =       parse_frontmatter(settings_folder + 'Prompts structure.md')

    introduction =      Utility.read_file(settings_folder + 'Introduction.md')
    introduction =      Utility.expand_abbreviations(introduction)

    new_config['abbreviations'] = {**abbreviations, **new_abbreviations}
    new_config['variables'] = {**variables, **new_variables}
    new_config['prompts_structure'] = {**prompts_structure, **new_prompts}
    new_config['introduction'] = introduction
    
    if 'model' in new_config and not new_config['model']: #if the key is present but value is empty
        new_config.pop('model')
    elif 'model' in new_config and new_config['model']: 
        new_config['model'] = parse_model(new_config)

    return(new_config)