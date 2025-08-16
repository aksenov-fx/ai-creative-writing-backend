from ..History.Factory import Factory
from ..Streaming.stream import stream
from ..Composers.ApiComposer import ApiComposer

class Chatter:
    
    @staticmethod
    def chat(file_path: str) -> None:

        history, history_parsed = Factory.get_chat_objects(file_path)
        history_parsed.process()
        messages = ApiComposer.compose_chat_messages(history_parsed)

        history.fix_separator()
        stream(history, messages)