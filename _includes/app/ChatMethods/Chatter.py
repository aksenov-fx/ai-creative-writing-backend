from ..History.Factory import Factory

class Chatter:
    
    @staticmethod
    def chat(file_path: str) -> None:
        from .Composers.ApiComposer import ApiComposer

        history, history_parsed = Factory.get_chat_objects(file_path)
        history_parsed.process()
        messages = ApiComposer.compose_chat_messages(history_parsed)

        history.fix_separator()
        Chat.stream(history, messages)