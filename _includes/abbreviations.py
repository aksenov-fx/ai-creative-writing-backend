import yaml, os
from .settings import config

def read_yaml_file_to_hash(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def update_abbreviations(update_file_path):
    if os.path.getsize(update_file_path) > 0:
        new_dict = read_yaml_file_to_hash(update_file_path)
        config.abbreviations.update(new_dict)

config.abbreviations = read_yaml_file_to_hash('_includes/abbreviations.yaml')