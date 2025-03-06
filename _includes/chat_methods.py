from .StoryGenerator._story_generator import chat
from .chat_settings import config
from . import chat_endpoints as chat_endpoints

# --- Chat methods --- #
# Define custom promts here

class Chat:
    @staticmethod
    def write_scene(model):
        if config.user_prompt:
            config.user_prompt = f"{config.user_preprompt}{config.user_prompt}{config.user_postprompt}"
        chat(chat_endpoints.endpoint, model)

    @staticmethod
    def custom_prompt(model):
        chat(chat_endpoints.endpoint, model)