from .vars import vars
from . import endpoints as endpoints
from .StoryGenerator.StoryGenerator import StoryGenerator
from .settings import config

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
        user_prompt = vars["guidelines"] + "\n" + "**Instructions**" + "\n" + vars["user_preprompt"] + config.user_prompt + "\n\n" + vars["user_postprompt"]
        StoryGenerator.generate(endpoints.endpoint, model, config.first_prompt, user_prompt)

    @staticmethod
    def custom_prompt(model):
        Chat.validate_prompts()
        StoryGenerator.generate(endpoints.endpoint, model, config.first_prompt, config.user_prompt)
    
    @staticmethod
    def change_part(model, part, prompt):
        Chat.validate_prompts()
        config.part_number = part
        StoryGenerator.rewrite(endpoints.endpoint, model, config.first_prompt, prompt)

    @staticmethod
    def refine(model, part):
        prompt = "**Instructions**" + "\n" + config.user_prompt + "\n" + vars["refine_postprompt"]
        Chat.change_part(model, part, prompt)
    
    @staticmethod
    def rewrite(model, part):
        prompt = vars["guidelines"] + "\n" + "**Instructions**" + "\n" + config.user_prompt + vars["rewrite_postprompt"]
        Chat.change_part(model, part, prompt)

    @staticmethod
    def regenenerate(model, part):
        user_prompt = vars["guidelines"] + "\n" + "**Instructions**" + "\n" + vars["user_preprompt"] + config.user_prompt + "\n" + vars["user_postprompt"]
        Chat.validate_prompts()
        config.part_number = part
        StoryGenerator.regenerate(endpoints.endpoint, model, config.first_prompt, user_prompt)

    @staticmethod
    def add_part(model, part):
        Chat.validate_prompts()
        config.part_number = part
        
        user_prompt = vars["guidelines"] + "\n" + "**Instructions**" + "\n" + vars["user_preprompt"] + config.user_prompt + "\n" + vars["user_postprompt"]
        StoryGenerator.add_part(endpoints.endpoint, model, config.first_prompt, user_prompt)

    @staticmethod
    def summarize(model):
        prompt = vars["summarize_preprompt"]
        StoryGenerator.summarize_all(endpoints.endpoint, model, prompt)

    @staticmethod
    def update_summary(model):
        prompt = vars["summarize_preprompt"]
        StoryGenerator.update_summary(endpoints.endpoint, model, prompt)