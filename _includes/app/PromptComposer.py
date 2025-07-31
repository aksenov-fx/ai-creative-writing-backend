from _includes import config, vars
from .Utility import Utility

class PromptComposer:
    
    @staticmethod
    def validate():

        first_prompt_error = "config.first_prompt is not set. Please set it before beginning a story."
        user_prompt_error = "config.user_prompt is not set. Please set it before writing a scene."

        if not config.first_prompt:
            raise ValueError(first_prompt_error)

        if not config.user_prompt:
            raise ValueError(user_prompt_error)
        
    @staticmethod
    def compose_prompt(mode):
        
        if config.user_prompt:
            user_prompt = Utility.expand_abbreviations(config.user_prompt)

        if mode in ['write_scene', 'regenerate', 'add_part']:
            PromptComposer.validate()
            prompt = vars["guidelines"] + "\n" + vars["instructions_preprompt"] + "\n" + vars["user_preprompt"] + user_prompt + "\n\n" + vars["user_postprompt"]
        
        elif mode == 'custom_prompt':
            PromptComposer.validate()
            prompt = vars["instructions_preprompt"] + "\n" + user_prompt
        
        elif mode == 'change_part':
            PromptComposer.validate()
            prompt = vars["instructions_preprompt"] + "\n" + user_prompt + "\n" + vars["rewrite_postprompt"]
        
        elif mode == 'summarize_part':
            prompt = vars["instructions_preprompt"] + "\n" + vars["summarize_preprompt"]
        
        else:
            raise ValueError(f"Unknown mode: {mode}")
        
        return prompt