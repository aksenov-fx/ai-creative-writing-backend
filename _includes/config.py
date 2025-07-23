from .StoryGenerator.ConfigClass import ChatConfig
from .StoryGenerator.Utility import Utility
from .StoryGenerator.History import HistoryChanger, HistoryParser

config = Utility.read_yaml('./_includes/Settings/settings.yaml')
config = ChatConfig(**config)

config.abbreviations = Utility.read_yaml('_includes/Settings/abbreviations.yaml')
vars = Utility.read_yaml('_includes/Settings/vars.yaml')

endpoints = Utility.read_yaml('./_includes/Settings/endpoints.yaml')
endpoint = endpoints['openrouter']
endpoint['api_key'] = open(endpoint['api_key_file'], 'r').read().strip()
config.endpoint = endpoint

models = Utility.read_yaml('_includes/Settings/models.yaml')

story = HistoryChanger(config.history_path)
summary = HistoryChanger(config.summary_path)
prompts = HistoryChanger(config.prompts_path)

story_parsed = HistoryParser(config.history_path)
summary_parsed = HistoryParser(config.summary_path)