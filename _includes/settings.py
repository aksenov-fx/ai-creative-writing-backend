from .StoryGenerator.ConfigClass import ChatConfig
import yaml, os

# --- Chat settings --- #

def create_config_from_yaml(yaml_file_path):
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        yaml_data = yaml.safe_load(file)
    return ChatConfig(**yaml_data)

def update_config_from_yaml(config_instance, yaml_file_path):
    if not os.path.isfile(yaml_file_path):
        return
    
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        yaml_data = yaml.safe_load(file)
    
    for key, value in yaml_data.items():
        if hasattr(config_instance, key):
            setattr(config_instance, key, value)

config = create_config_from_yaml('./_includes/settings.yaml')