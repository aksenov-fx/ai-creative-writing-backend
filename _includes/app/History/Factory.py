from _includes import config
from .History import HistoryChanger, HistoryParser
from .ChatHistory import ChatHistoryChanger, ChatHistoryParser

class Factory:
    
    @staticmethod
    def get_story() -> HistoryChanger:
        return HistoryChanger(config.folder_path + config.history_path)

    @staticmethod
    def get_summary() -> HistoryChanger:
        return HistoryChanger(config.folder_path + config.summary_path)

    @staticmethod
    def get_prompts() -> HistoryChanger:
        return HistoryChanger(config.folder_path + config.prompts_path)

    @staticmethod
    def get_story_parsed() -> HistoryParser:
        return HistoryParser(config.folder_path + config.history_path)

    @staticmethod
    def get_summary_parsed() -> HistoryParser:
        return HistoryParser(config.folder_path + config.summary_path)
    
    @staticmethod
    def get_objects():
        return Factory.get_story(), Factory.get_story_parsed(), Factory.get_summary()

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