from .app.ConfigManager import ChatConfig, read_yaml
from .app.Utility import Utility

folder = './_includes/settings/'

default_config =    read_yaml(folder + 'Settings.yaml')
abbreviations =     read_yaml(folder + 'Abbreviations.yaml')
models =            read_yaml(folder + 'Models.yaml')
endpoints =         read_yaml(folder + 'Endpoints.yaml')
variables =         read_yaml(folder + 'Variables.yaml')
prompts_structure = read_yaml(folder + 'Prompts structure.yaml')

config = ChatConfig(**default_config)
config.abbreviations = abbreviations
config.variables = variables
config.prompts_structure = prompts_structure
config.model = models[config.default_model]['name']

endpoint = endpoints['openrouter']
endpoint['api_key'] = Utility.read_file(endpoint['api_key_file']).strip()
config.endpoint = endpoint