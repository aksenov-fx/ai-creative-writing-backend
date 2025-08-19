import os
from dataclasses import asdict

from .. import Utility
from .commons import get_endpoint, get_model


def load_config(folder_path, config_dict, extension='.yaml'):

    keys = ['Variables', 'Abbreviations', 'Prompts Structure', 'Models', 'Endpoints']
    
    for key in keys:
        path = os.path.join(folder_path, key + extension)
        key_name = key.lower().replace(" ", "_")
        config_dict[key_name].update(Utility.read_yaml(path))
    
    config_dict['endpoint'] = get_endpoint(config_dict)
    config_dict['model'] = get_model(config_dict)
    config_dict['introduction'] = Utility.read_file(os.path.join(folder_path, 'Introduction.md'))

    return config_dict


def get_story_config(folder: str):
    from _includes import config

    settings_folder = os.path.join(folder, 'Settings/')
    config.folder_path = os.path.join(folder + "/")
    config.interrupt_flag = False

    old_config = asdict(config)
    new_config = Utility.read_yaml(os.path.join(settings_folder, 'Settings.md'), convert_keys_to_snake_case=True)
    old_config.update(new_config)
    new_config = load_config(settings_folder, old_config, ".md")

    return new_config
