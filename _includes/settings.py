from .StoryGenerator.ConfigClass import ChatConfig
import json, os

# --- Chat settings --- #

def create_config_from_json(json_file_path):
	
    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    return ChatConfig(**json_data)

def update_config_from_json(config_instance, json_file_path):
	if not os.path.isfile(json_file_path):
		return
	
	with open(json_file_path, 'r', encoding='utf-8') as file:
		json_data = json.load(file)
	
	for key, value in json_data.items():
		if hasattr(config_instance, key):
			setattr(config_instance, key, value)
	
config = create_config_from_json('./_includes/config.json')