from _includes import config
from .Streaming.Streamer import Streamer
from .Streaming.TokenHandler import TokenHandler
from .History.History import HistoryChanger

from .ChatMethods.Generator import Generator
from .ChatMethods.Changer import Changer
from .ChatMethods.Helpers import Helpers
from .ChatMethods.Summarizer import Summarizer
from .ChatMethods.Chatter import Chatter

class Chat:

    Generator = Generator
    Changer = Changer
    Helpers = Helpers
    Summarizer = Summarizer
    Chatter = Chatter

    @staticmethod
    def stream(history_object: HistoryChanger,
               messages,
               rewrite: bool = False,
               write_history: bool = True,
               part_number: int = 0) -> None:
               
        print(f"\nModel: {config.model}")
        if config.debug:
            print("\nDebug mode is on")
            return "debug response"

        token_handler = TokenHandler(history_object, rewrite, write_history, part_number)
        streamer = Streamer(token_handler.get_token_callback())
        streamer.stream_response(messages)
        return token_handler.finalize()
