from .app.ConfigManager import ChatConfig, read_yaml, load_config

folder = './_includes/settings/'
default_config = read_yaml(folder + 'Settings.yaml')
load_config(folder, default_config)

config = ChatConfig(**default_config)