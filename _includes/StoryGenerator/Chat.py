from _includes import config, endpoints, vars, history, prompts, summary
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
    def write_scene(model):
        Chat.initialize()
        user_prompt = vars["guidelines"] + "\n" + vars["instructions_preprompt"] + "\n" + vars["user_preprompt"] + config.user_prompt + "\n\n" + vars["user_postprompt"]
        StoryGenerator.generate(endpoints, model, config.first_prompt, user_prompt)

    @staticmethod
    def custom_prompt(model):
        Chat.initialize()
        user_prompt = vars["instructions_preprompt"] + "\n" + config.user_prompt
        StoryGenerator.generate(endpoints, model, config.first_prompt, user_prompt)
    
    @staticmethod
    def rewrite(model, part):
        Chat.initialize()
        config.part_number = part
        prompt = vars["instructions_preprompt"] + "\n" + config.user_prompt + "\n" + vars["rewrite_postprompt"]
        StoryGenerator.change_part(endpoints, model, config.first_prompt, prompt)

    @staticmethod
    def rewrite_parts(model, part):
        Chat.initialize()
        config.part_number = part
        prompt = vars["instructions_preprompt"] + "\n" + config.user_prompt + "\n" + vars["rewrite_postprompt"]
        StoryGenerator.change_parts(endpoints, model, config.first_prompt, prompt)

    @staticmethod
    def regenenerate(model, part):
        Chat.initialize()
        config.part_number = part
        user_prompt = vars["guidelines"] + "\n" + vars["instructions_preprompt"] + "\n" + vars["user_preprompt"] + config.user_prompt + "\n\n" + vars["user_postprompt"]
        StoryGenerator.regenerate(endpoints, model, config.first_prompt, user_prompt)

    @staticmethod
    def add_part(model, part):
        Chat.initialize()
        config.part_number = part
        user_prompt = vars["guidelines"] + "\n" + vars["instructions_preprompt"] + "\n" + vars["user_preprompt"] + config.user_prompt + "\n\n" + vars["user_postprompt"]
        StoryGenerator.add_part(endpoints, model, config.first_prompt, user_prompt)

    @staticmethod
    def summarize(model):
        Chat.initialize(validate=False)
        prompt = vars["instructions_preprompt"] + "\n" + vars["summarize_preprompt"]
        StoryGenerator.summarize_all(endpoints, model, prompt)

    @staticmethod
    def update_summary(model):
        Chat.initialize(validate=False)
        prompt = vars["instructions_preprompt"] + "\n" + vars["summarize_preprompt"]
        StoryGenerator.update_summary(endpoints, model, prompt)

    @staticmethod
    def set_prompt(part_value):
        Chat.initialize(validate=False)

        part_value -= 1
        prompts.insert_separator()
        config.user_prompt = prompts.return_part(part_value)

        prompt_to_print = Utility.expand_abbreviations(config.user_prompt)
        print(prompt_to_print)

    @staticmethod
    def remove_last_response():
        Chat.initialize(validate=False)
        history.remove_last_response()
