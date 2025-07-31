from .app.ConfigClass import ChatConfig
from .app.Utility import Utility

settings_folder = './_includes/settings/'

default_config =    Utility.read_yaml(settings_folder + 'settings.yaml')
abbreviations =     Utility.read_yaml(settings_folder + 'abbreviations.yaml')
endpoints =         Utility.read_yaml(settings_folder + 'endpoints.yaml')
models =            Utility.read_yaml(settings_folder + 'models.yaml')
vars =              Utility.read_yaml(settings_folder + 'vars.yaml')

config = ChatConfig(**default_config)
endpoint = endpoints['openrouter']
endpoint['api_key'] = open(endpoint['api_key_file'], 'r').read().strip()
config.endpoint = endpoint
config.abbreviations = abbreviations
config.model = models[config.model]