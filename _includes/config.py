from .app.Utility.ConfigManager import ChatConfig, load_config
from .app.Utility.Utility import Utility

folder = './_includes/settings/'
default_config = Utility.read_yaml(folder + 'Settings.yaml')
load_config(folder, default_config)

config = ChatConfig(**default_config)