from ..History.Factory import Factory
from ..Streaming.stream import stream
from ..Composers.ApiComposer import ApiComposer

class Chatter:
    
    @staticmethod
    def chat() -> None:
        """Chat method for conversations - not for story writing"""
        
        history, history_parsed = Factory.get_chat_objects()
        history_parsed.process()
        messages = ApiComposer.compose_messages(history_parsed.custom_instructions, history_parsed.parts)

        stream(history, messages)