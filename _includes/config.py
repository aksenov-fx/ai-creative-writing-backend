import yaml, os
from .StoryGenerator.ConfigClass import ChatConfig

def read_yaml(file_path):
    if os.path.getsize(file_path) == 0 or not os.path.isfile(file_path):
        return {}
    
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def update_config_from_yaml(config_instance, file_path):
    yaml_data = read_yaml(file_path)
    
    for key, value in yaml_data.items():
        if hasattr(config_instance, key):
            setattr(config_instance, key, value)

config = read_yaml('./_includes/Settings/settings.yaml')
config = ChatConfig(**config)

endpoints = read_yaml('./_includes/Settings/endpoints.yaml')
endpoints['api_key'] = open(endpoints['api_key_file'], 'r').read().strip()
models = read_yaml('_includes/Settings/models.yaml')

config.abbreviations = read_yaml('_includes/Settings/abbreviations.yaml')
vars = read_yaml('_includes/Settings/vars.yaml')