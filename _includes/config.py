from .StoryGenerator.ConfigClass import ChatConfig
from .StoryGenerator.Utility import Utility
from .StoryGenerator.History import HistoryChanger, HistoryParser

default_config = Utility.read_yaml('./_includes/Settings/settings.yaml')
abbreviations = Utility.read_yaml('_includes/Settings/abbreviations.yaml')

endpoints = Utility.read_yaml('./_includes/Settings/endpoints.yaml')
endpoint = endpoints['openrouter']
endpoint['api_key'] = open(endpoint['api_key_file'], 'r').read().strip()

config = ChatConfig(**default_config)
config.endpoint = endpoint
config.abbreviations = abbreviations

models = Utility.read_yaml('_includes/Settings/models.yaml')
vars = Utility.read_yaml('_includes/Settings/vars.yaml')

story = HistoryChanger(config.history_path)
summary = HistoryChanger(config.summary_path)
prompts = HistoryChanger(config.prompts_path)

story_parsed = HistoryParser(config.history_path)
summary_parsed = HistoryParser(config.summary_path)