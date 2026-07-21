import os
import argparse

from .app.ConfigManager.ConfigDataClass import ConfigDataClass
from .app.ConfigManager import load_config
from .app.Utility.readers import read_yaml


def _get_settings_folder():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--settings', '-c', dest='settings_folder', default=None)
    args, _ = parser.parse_known_args()
    return args.settings_folder or './_includes/settings/'


folder = _get_settings_folder()
default_config = read_yaml(os.path.join(folder, 'Settings.yaml'))
default_config['settings_folder'] = folder
load_config(folder, default_config)
config = ConfigDataClass(**default_config)

default_chat_config = read_yaml(os.path.join(folder, 'Chat Settings.yaml'))
merged_chat_config = {**default_config, **default_chat_config}
chat_config = ConfigDataClass(**merged_chat_config)