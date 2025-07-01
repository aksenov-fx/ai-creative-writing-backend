from . import prompt_vars
from .StoryGenerator._story_generator import chat
from .chat_settings import config
from . import chat_endpoints as chat_endpoints
from .StoryGenerator.ChatHistory import ChatHistory
from .StoryGenerator._story_changer import change_part as story_changer_change_part
from .StoryGenerator._story_changer import add_part as story_changer_add_part
from .StoryGenerator._story_summarizer import summarize_all, update_summary

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
        user_prompt = prompt_vars.user_preprompt + config.user_prompt + prompt_vars.user_postprompt
        chat(chat_endpoints.endpoint, model, config.first_prompt, user_prompt)

    @staticmethod
    def custom_prompt(model):
        Chat.validate_prompts()
        chat(chat_endpoints.endpoint, model, config.first_prompt, config.user_prompt)
    
    @staticmethod
    def change_part(model, part, prompt, rewrite):
        Chat.validate_prompts()
        config.part_number = part
        story_changer_change_part(chat_endpoints.endpoint, model, config.first_prompt, prompt, rewrite)

    @staticmethod
    def refine(model, part):
        prompt = prompt_vars.change_part_preprompt + config.user_prompt + prompt_vars.refine_postprompt
        Chat.change_part(model, part, prompt, True)
    
    @staticmethod
    def rewrite(model, part):
        prompt = prompt_vars.change_part_preprompt + config.user_prompt + prompt_vars.rewrite_postprompt
        Chat.change_part(model, part, prompt, True)

    @staticmethod
    def regenenerate(model, part):
        user_prompt = prompt_vars.user_preprompt + config.user_prompt + prompt_vars.user_postprompt
        Chat.change_part(model, part, user_prompt, False)

    @staticmethod
    def add_part(model, part):
        Chat.validate_prompts()
        config.part_number = part
        
        user_prompt = prompt_vars.user_preprompt + config.user_prompt + prompt_vars.user_postprompt
        story_changer_add_part(chat_endpoints.endpoint, model, config.first_prompt, user_prompt)

    @staticmethod
    def summarize(model):
        prompt = prompt_vars.summarize_preprompt
        summarize_all(chat_endpoints.endpoint, model, prompt)

    @staticmethod
    def update_summary(model):
        prompt = prompt_vars.summarize_preprompt
        update_summary(chat_endpoints.endpoint, model, prompt)