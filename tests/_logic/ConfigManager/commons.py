import os

from tests._logic.utils import read_yaml
from tests._logic.utils import setup_temp_folder, read_expected_file

from tests._logic.ConfigManager.TestsConfigClass import TestsConfig
from _includes.app.ConfigManager import get_story_config 
from _includes.app.ConfigManager import get_chat_config

from _includes import config
from _includes import default_config

def get_tests_config(path):
    yaml_data = read_yaml(path)
    conf = TestsConfig(**yaml_data)

    conf.story_folder_path = os.path.join(conf.temp_dir, conf.story_folder)

    return conf

def get_app_config(tests_conf, method, test_file):
    
    if method == "chat":
        path = tests_conf.story_folder_path + "/Conversation/" + test_file 
        new_config = get_chat_config(path, config, default_config)
    else:
        path = tests_conf.story_folder_path
        new_config = get_story_config(path, config)
        new_config['history_path'] = test_file
    
    return new_config
