from .app.ConfigManager import ChatConfig, read_yaml
from .app.Utility import Utility

folder = './_includes/settings/'

default_config =    read_yaml(folder + 'Settings.yaml')
abbreviations =     read_yaml(folder + 'Abbreviations.yaml')
variables =         read_yaml(folder + 'Variables.yaml')
prompts_structure = read_yaml(folder + 'Prompts structure.yaml')

models =            read_yaml(folder + 'Models.yaml')
endpoints =         read_yaml(folder + 'Endpoints.yaml')

default_config['abbreviations'] = abbreviations
default_config['variables'] = variables
default_config['prompts_structure'] = prompts_structure

#

endpoint = endpoints[default_config['default_endpoint']]
endpoint['api_key'] = Utility.read_file(endpoint['api_key_file']).strip()

default_config['endpoint'] = endpoint
default_config['model'] = models[default_config['default_model']]['name']

#

config = ChatConfig(**default_config)