import os
from _includes import config

from .Story import StoryChanger
from .Story import StoryParser

from .ChatHistory import ChatHistoryChanger
from .ChatHistory import ChatHistoryParser

from .Summary import SummaryChanger
from .Summary import SummaryParser

class Factory:
    
    @staticmethod
    def get_story() -> StoryChanger:
        return StoryChanger(os.path.join(config.folder_path, config.history_path))

    @staticmethod
    def get_prompts() -> StoryChanger:
        return StoryChanger(os.path.join(config.folder_path, config.prompts_path))

    @staticmethod
    def get_story_parsed() -> StoryParser:
        return StoryParser(os.path.join(config.folder_path, config.history_path))

    @staticmethod
    def get_objects():
        return Factory.get_story(), Factory.get_story_parsed(), Factory.get_summary()

# Summary

    @staticmethod
    def get_summary() -> SummaryChanger:
        return SummaryChanger(os.path.join(config.folder_path, config.summary_yaml_path))

    @staticmethod
    def get_summary_parsed() -> SummaryParser:
        return SummaryParser(os.path.join(config.folder_path, config.summary_yaml_path))
    
# Chat

    @staticmethod
    def get_chat_history(file_path) -> ChatHistoryChanger:
        return ChatHistoryChanger(file_path)

    @staticmethod
    def get_chat_history_parsed(file_path) -> ChatHistoryParser:
        return ChatHistoryParser(file_path)

    @staticmethod
    def get_chat_objects(file_path):
        return Factory.get_chat_history(file_path), Factory.get_chat_history_parsed(file_path)