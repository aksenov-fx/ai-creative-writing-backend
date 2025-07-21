from .StoryGenerator.ConfigClass import ChatConfig
from .StoryGenerator.Utility import Utility
from .StoryGenerator.History import History

config = Utility.read_yaml('./_includes/Settings/settings.yaml')
config = ChatConfig(**config)

config.abbreviations = Utility.read_yaml('_includes/Settings/abbreviations.yaml')
vars = Utility.read_yaml('_includes/Settings/vars.yaml')

endpoints = Utility.read_yaml('./_includes/Settings/endpoints.yaml')
endpoints['api_key'] = open(endpoints['api_key_file'], 'r').read().strip()
models = Utility.read_yaml('_includes/Settings/models.yaml')

history = History(config.history_path, config)
summary = History(config.summary_path, config)
prompts = History(config.prompts_path, config)