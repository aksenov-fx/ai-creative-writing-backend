from _includes import config
from .Streamer import Streamer
from .TokenHandler import TokenHandler

def stream(history_object,
           messages,
           rewrite: bool = False,
           write_history: bool = True,
           part_number: int = 0,
           append: bool = False) -> None:

    print(f"\nModel: {config.model}")
    if config.debug:
        print("\nDebug mode is on")
        return "debug response"

    token_handler = TokenHandler(history_object, rewrite, write_history, part_number, append)
    streamer = Streamer(token_handler.get_token_callback())
    streamer.stream_response(messages)
    return token_handler.finalize()