from _includes import config, vars, story, prompts
from .StoryGenerator import StoryGenerator
from .Utility import Utility

# --- Chat methods --- #
# Define custom promts here

class Chat:
    
    first_prompt_error = "config.first_prompt is not set. Please set it before beginning a story."
    user_prompt_error = "config.user_prompt is not set. Please set it before writing a scene."

    @staticmethod
    def initialize(validate=True):

        Utility.reset_history()

        if validate and not config.first_prompt:
            raise ValueError(Chat.first_prompt_error)

        if validate and not config.user_prompt:
            raise ValueError(Chat.user_prompt_error)

    @staticmethod
    def write_scene():
        Chat.initialize()
        user_prompt = vars["guidelines"] + "\n" + vars["instructions_preprompt"] + "\n" + vars["user_preprompt"] + config.user_prompt + "\n\n" + vars["user_postprompt"]
        StoryGenerator.generate(config.first_prompt, user_prompt)

    @staticmethod
    def custom_prompt():
        Chat.initialize()
        user_prompt = vars["instructions_preprompt"] + "\n" + config.user_prompt
        StoryGenerator.generate(config.first_prompt, user_prompt)
    
    @staticmethod
    def rewrite(part):
        Chat.initialize()
        prompt = vars["instructions_preprompt"] + "\n" + config.user_prompt + "\n" + vars["rewrite_postprompt"]
        StoryGenerator.change_part(config.first_prompt, prompt, part)

    @staticmethod
    def rewrite_parts(part):
        Chat.initialize()
        prompt = vars["instructions_preprompt"] + "\n" + config.user_prompt + "\n" + vars["rewrite_postprompt"]
        StoryGenerator.change_parts(config.first_prompt, prompt,part)

    @staticmethod
    def regenenerate(part):
        Chat.initialize()
        user_prompt = vars["guidelines"] + "\n" + vars["instructions_preprompt"] + "\n" + vars["user_preprompt"] + config.user_prompt + "\n\n" + vars["user_postprompt"]
        StoryGenerator.regenerate(config.first_prompt, user_prompt, part)

    @staticmethod
    def add_part(part):
        Chat.initialize()
        user_prompt = vars["guidelines"] + "\n" + vars["instructions_preprompt"] + "\n" + vars["user_preprompt"] + config.user_prompt + "\n\n" + vars["user_postprompt"]
        StoryGenerator.add_part(config.first_prompt, user_prompt, part)

    @staticmethod
    def summarize():
        Chat.initialize(validate=False)
        prompt = vars["instructions_preprompt"] + "\n" + vars["summarize_preprompt"]
        StoryGenerator.summarize_all(prompt)

    @staticmethod
    def update_summary():
        Chat.initialize(validate=False)
        prompt = vars["instructions_preprompt"] + "\n" + vars["summarize_preprompt"]
        StoryGenerator.update_summary(prompt)

    @staticmethod
    def set_prompt(part_value):
        Chat.initialize(validate=False)

        part_value -= 1
        prompts.fix_separator()
        config.user_prompt = prompts.return_part(part_value)

        prompt_to_print = Utility.expand_abbreviations(config.user_prompt)
        print(prompt_to_print)

    @staticmethod
    def remove_last_response():
        Chat.initialize(validate=False)
        story.remove_last_response()
