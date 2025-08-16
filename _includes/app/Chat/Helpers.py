from ..Composers.PromptComposer import compose_helper_prompt
from ..Streaming.stream import stream

class Helpers:

    @staticmethod
    def rewrite_selection(selected_text: str):
        messages = compose_helper_prompt('Rewrite selection', selected_text)
        result = stream(None, messages, write_history=False)
        return result
    
    @staticmethod
    def translate(selected_text: str):
        messages = compose_helper_prompt('Translate', selected_text)
        result = stream(None, messages, write_history=False)
        return result

    @staticmethod
    def explain(selected_text: str):
        messages = compose_helper_prompt('Explain', selected_text)
        result = stream(None, messages, write_history=False)
        return result
