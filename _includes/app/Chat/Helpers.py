from ..Composers.PromptComposer import compose_helper_prompt
from ..Streaming.stream import stream
from ...config import config


class Helpers:
    """
    Helper methods 

    Do not send any context to model - only selected text
    Return the result without writing anything to files
    """
    
    @staticmethod
    def rewrite_selection(selected_text: str):
        """Rewrites the selected text according to user prompt"""

        config.model = config.models[config.rewrite_model]['name']

        messages = compose_helper_prompt('Rewrite selection', selected_text)
        result = stream(None, messages, write_history=False)
        return result
    
    @staticmethod
    def translate(selected_text: str):
        """Translates the selected text to the language specified in config"""
        
        config.model = config.models[config.translation_model]['name']

        messages = compose_helper_prompt('Translate', selected_text)
        result = stream(None, messages, write_history=False)
        return result

    @staticmethod
    def explain(selected_text: str):
        """Explains the meaning of the unknown word"""

        config.model = config.models[config.explain_model]['name']

        messages = compose_helper_prompt('Explain', selected_text)
        result = stream(None, messages, write_history=False)
        return result
