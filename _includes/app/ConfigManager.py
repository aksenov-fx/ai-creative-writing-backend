from dataclasses import dataclass, asdict
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
    abbreviations: str
    translation_language: str

    endpoints: dict
    default_endpoint: str
    endpoint: dict

    models: dict
    default_model: str
    summary_model: str
    model: dict

    temperature: float
    max_tokens: int
    trim_history: bool
    history_prefix: str
    use_summary: bool

    print_messages: bool
    include_reasoning: bool
    print_reasoning: bool
    separator: str
    write_interval: float

    history_path: Path
    summary_path: Path
    prompts_path: Path
    folder_path: Path

    include_previous_part_when_summarizing: bool
    include_previous_part_when_rewriting: bool

    interrupt_flag: bool
    debug: bool

@contextmanager
def override_config(config: ChatConfig, **overrides: Any):

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
    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        return {}
    
    content = Utility.read_file(file_path)
    if file_path.endswith('.md'): content = content.split('---\n')[1]
    return yaml.safe_load(content)

def get_model(config_dict):

    model = config_dict['model']
    
    if not model:
        return config_dict['models'][config_dict['default_model']]['name']
    
    try:
        model_number = int(model)
        return list(config_dict['models'].values())[model_number - 1]['name']
    except ValueError:
        return model

def get_endpoint(config_dict):
    endpoint = config_dict['endpoints'][config_dict['default_endpoint']]
    endpoint['api_key'] = Utility.read_file(endpoint['api_key_file']).strip()
    return endpoint

def load_config(folder_path, config_dict, extension = '.yaml'):

    keys = ['Variables', 'Abbreviations', 'Prompts_structure', 'Models', 'Endpoints']
    
    for key in keys:
        path = os.path.join(folder_path, key + extension)
        key_name = key.lower()
        config_dict[key_name].update(read_yaml(path))
    
    config_dict['endpoint'] = get_endpoint(config_dict)
    config_dict['model'] = get_model(config_dict)
    config_dict['introduction'] = Utility.read_file(folder_path + 'Introduction.md')

    return config_dict

def update_config(folder: str):
    from _includes import config

    settings_folder = folder + '/Settings/'

    old_config = asdict(config)
    new_config = read_yaml(settings_folder + 'Settings.md')
    old_config.update(new_config)
    new_config = load_config(settings_folder, old_config, ".md")

    config.interrupt_flag = False
    config.folder_path = folder + '/'

    return new_config