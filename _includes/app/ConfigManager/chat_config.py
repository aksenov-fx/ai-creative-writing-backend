import os
from dataclasses import asdict
from pathlib import Path

from .. import Utility
from .commons import get_model


def get_story_path(file, current_config, default_config):
    if not current_config['chat_with_story']: return ""

    parent_directory = Path(file).parent.parent
    
    # Get story config to get history and summary paths
    story_config = Utility.read_yaml(os.path.join(parent_directory, 'Settings', 'Settings.md'))
    story_config = {**default_config, **story_config}

    story_path = os.path.join(parent_directory, story_config["history_path"])
    summary_path = os.path.join(parent_directory, story_config["summary_md_path"])

    file_path = summary_path if current_config['use_summary'] else story_path

    return file_path


def get_chat_config(file, config, default_config):
    
    current_config = asdict(config)
    default_chat_config = Utility.read_yaml(os.path.join(config.settings_folder, 'Chat Settings.yaml'))
    new_config = Utility.read_yaml(file, convert_keys_to_snake_case=True)
    
    current_config.update(default_chat_config)
    current_config.update(new_config)
    
    current_config['model'] = get_model(current_config)

    # Get story path if chat_with_story is True
    current_config['include_file'] = get_story_path(file, current_config, default_config)

    return current_config
