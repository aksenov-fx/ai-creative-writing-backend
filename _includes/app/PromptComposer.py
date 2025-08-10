from _includes import config
from .Utility import Utility
from .ApiComposer import ApiComposer
from .History import HistoryParser

class PromptComposer:
    
    @staticmethod
    def validate(include_introduction):

        introduction_error = "config.introduction is not set. Please set it before beginning a story."
        user_prompt_error = "User prompt is not set. Please set it before writing a scene."

        if include_introduction and not config.introduction:
            raise ValueError(introduction_error)

        if not config.variables['#user_prompt']:
            raise ValueError(user_prompt_error)
        
    @staticmethod
    def compose_prompt(method: str, history_parsed: HistoryParser, include_introduction = True):
        
        PromptComposer.validate(include_introduction)

        # Prepare user prompt
        config.variables['#user_prompt'] = Utility.expand_abbreviations(config.variables['#user_prompt'])
        prompt_structure = config.prompts_structure[method] # Get structure defined in prompts_structure.yaml
        prompt = Utility.expand_abbreviations(prompt_structure, config.variables) # Compose prompt according to structure

        # Prepare history
        if config.trim_history: history_parsed.trim_content()
        history = config.history_prefix + "\n" + history_parsed.parsed if history_parsed.parsed else ""

        # Prepare introduction
        introduction = Utility.expand_abbreviations(config.introduction)
        introduction += "\n\n" if include_introduction else ""

        # Combine introduction, history and user prompt
        combined_prompt = introduction + history + "\n\n" + prompt + "\n\n" + history_parsed.part_number_content
        combined_prompt = combined_prompt.replace("\n\n\n", "\n\n").strip()

        messages = ApiComposer.compose_messages(combined_prompt, history_parsed.assistant_response)
        
        return messages
    
    @staticmethod
    def compose_prompt_to_rewrite_selection(selected_text: str):
        config.variables['#user_prompt'] = Utility.expand_abbreviations(config.variables['#user_prompt'])
        prompt_structure = config.prompts_structure['Rewrite selection']
        prompt = Utility.expand_abbreviations(prompt_structure, config.variables)

        combined_prompt = prompt + selected_text 
        messages = ApiComposer.compose_messages(combined_prompt, None)
        return messages
