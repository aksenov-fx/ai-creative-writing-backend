from dataclasses import dataclass, asdict
from contextlib import contextmanager
from pathlib import Path
from typing import Any
import os

from .Utility import Utility

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
    summary_yaml_path: Path
    summary_md_path: Path
    prompts_path: Path
    folder_path: Path

    include_previous_part_when_summarizing: bool
    include_previous_part_when_rewriting: bool

    interrupt_flag: bool
    debug: bool

    # Chat settings
    splitter: str
    add_header: bool
    chat_with_story: bool
    include_file: str

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

    keys = ['Variables', 'Abbreviations', 'Prompts Structure', 'Models', 'Endpoints']
    
    for key in keys:
        path = os.path.join(folder_path, key + extension)
        key_name = key.lower().replace(" ", "_")
        config_dict[key_name].update(Utility.read_yaml(path))
    
    config_dict['endpoint'] = get_endpoint(config_dict)
    config_dict['model'] = get_model(config_dict)
    config_dict['introduction'] = Utility.read_file(folder_path + 'Introduction.md')

    return config_dict

def get_story_config(folder: str):
    from _includes import config

    settings_folder = folder + '/Settings/'
    config.folder_path = folder + '/'
    config.interrupt_flag = False

    old_config = asdict(config)
    new_config = Utility.read_yaml(settings_folder + 'Settings.md', convert_keys_to_snake_case=True)
    old_config.update(new_config)
    new_config = load_config(settings_folder, old_config, ".md")

    return new_config

def get_chat_config(file):
    from ...config import config, default_config
    from pathlib import Path

    current_config = asdict(config)
    default_chat_config = Utility.read_yaml('./_includes/settings/Chat Settings.yaml')
    new_config = Utility.read_yaml(file, convert_keys_to_snake_case=True)
    
    current_config.update(default_chat_config)
    current_config.update(new_config)
    
    current_config['model'] = get_model(current_config)

    # Get story path if chat_with_story is True
    if current_config['chat_with_story']: 

        parent_directory = Path(file).parent.parent
        
        # Get story config to get history and summary paths
        story_config = Utility.read_yaml(str(parent_directory / 'Settings' / 'Settings.md'))
        story_config = {**default_config, **story_config}

        story_path = parent_directory / story_config["history_path"]
        summary_path = parent_directory / story_config["summary_path"]

        file_path = summary_path if current_config['use_summary'] else story_path
        current_config['include_file'] = file_path

    return current_config