from . import prompt_vars
from .StoryGenerator._story_generator import chat
from .chat_settings import config
from . import chat_endpoints as chat_endpoints
from .StoryGenerator.ChatHistory import ChatHistory
from .StoryGenerator._story_rewriter import rewrite_part

# --- Chat methods --- #
# Define custom promts here

class Chat:
    
    first_prompt_error = "config.first_prompt is not set. Please set it before beginning a story."
    user_prompt_error = "config.user_prompt is not set. Please set it before writing a scene."

    @staticmethod
    def validate_prompts():
        if not config.first_prompt:
            raise ValueError(Chat.first_prompt_error)

        if not config.user_prompt:
            raise ValueError(Chat.user_prompt_error)

    @staticmethod
    def write_scene(model):
        Chat.validate_prompts()

        if ChatHistory.has_separator():
            user_prompt = f"{prompt_vars.user_preprompt}{config.user_prompt}{prompt_vars.user_postprompt}"
            chat(chat_endpoints.endpoint, model, config.first_prompt, user_prompt)
        else:
            user_prompt = config.user_prompt + prompt_vars.user_postprompt
            first_prompt = config.first_prompt + user_prompt
            chat(chat_endpoints.endpoint, model, first_prompt, None)

    @staticmethod
    def custom_prompt(model):
        Chat.validate_prompts()
        chat(chat_endpoints.endpoint, model, config.first_prompt, config.user_prompt)

    @staticmethod
    def rewrite(model, part):
        Chat.validate_prompts()
        config.part_to_rewrite = part
        rewrite_part(chat_endpoints.endpoint, model, config.first_prompt, config.user_prompt)