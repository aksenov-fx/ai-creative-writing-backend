from .app.ConfigManager.ConfigDataClass import ConfigDataClass
from .app.ConfigManager import load_config
from .app import Utility
import os

folder = './_includes/settings/'
default_config = Utility.read_yaml(os.path.join(folder, 'Settings.yaml'))
load_config(folder, default_config)

config = ConfigDataClass(**default_config)