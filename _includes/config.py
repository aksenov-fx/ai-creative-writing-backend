import os

from .app.ConfigManager.ConfigDataClass import ConfigDataClass
from .app.ConfigManager import load_config
from .app.Utility.readers import read_yaml

folder = './_includes/settings/'
default_config = read_yaml(os.path.join(folder, 'Settings.yaml'))
load_config(folder, default_config)

config = ConfigDataClass(**default_config)