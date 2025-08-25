import os
from typing import List

from tests.config import tests_config
from tests._logic.utils import read_yaml
from tests._logic.utils import read_expected_file
from tests._logic.ConfigManager import get_app_config

from _includes.app import Chat

def get_callback(module, class_name, method_name):
    """Get obj.class.method by string names"""

    modules = {
        'Chat': Chat,
    }

    class_obj = getattr(modules[module], class_name)
    method_obj = getattr(class_obj, method_name)
    return method_obj

def get_class_params(module, class_name):
    """Get class parameters from YAML file."""

    class_params_folder = os.path.join(tests_config.params_dir, module)

    module_default_params_path = os.path.join(class_params_folder, 'Default.yaml')
    module_default_params = read_yaml(module_default_params_path)

    class_params_path = os.path.join(class_params_folder, f'{class_name}.yaml')
    class_params = read_yaml(class_params_path)

    for i, item in enumerate(class_params['parameters']):
        class_params['parameters'][i] = {**module_default_params, **item}

    return class_params

def load_params(module, class_name) -> List:
    """Load test parameters from YAML file and return as list of tuples."""

    params = []
    class_params = get_class_params(module, class_name)

    for item in class_params['parameters']:

        callback =                 get_callback(module, class_name, item['method'])
        method =                   item['method']
        test_file =                item['test_file']
        should_pass =              item['should_pass']
        arg =                      item['arg']
        overrides =                item['overrides']

        app_config = get_app_config(tests_config, method, test_file)
        expected_content = read_expected_file(tests_config.story_folder_path, method, test_file)

        params.append([app_config, expected_content, callback, class_name, should_pass, arg, overrides])

    return params
