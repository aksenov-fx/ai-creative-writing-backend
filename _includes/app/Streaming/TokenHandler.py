import time
import threading
from typing import Callable

from ..History.History import HistoryChanger
from _includes import config

class TokenHandler:
    
    def __init__(self, 
                 history_object: HistoryChanger = None,
                 rewriting: bool = False,
                 write_history: bool = True,
                 part_number: int = 0):
        
        self.history = history_object
        self.rewriting = rewriting
        self.write_history = write_history
        self.part_number = part_number

        self.token_buffer = ""
        self.complete_response = ""
        self.last_write_time = time.time()
        self.buffer_lock = threading.Lock()
    
    def write_file(self, content: str) -> None:
        
        if not self.write_history:
            return
            
        elif self.rewriting:
            self.history.replace_history_part(self.complete_response, self.part_number)

        else:
            self.history.append_history(content)
    
    def handle_token(self, content: str) -> None:
        """
        Handle a token from the stream.
        
        Buffering is introduced to prevent high I/O operations
        when rewriting parts instead of appending to the end of the file.
        When rewriting parts, the whole file content is being written.
        """
        with self.buffer_lock:
            self.complete_response += content
            
            if not self.rewriting:
                self.write_file(content)
                return
            
            self.token_buffer += content
            if time.time() - self.last_write_time < config.write_interval:
                return
                
            self.write_file(self.token_buffer)
            self.token_buffer = ""
            self.last_write_time = time.time()
    
    def flush_buffer(self) -> None:
        with self.buffer_lock:
            if self.token_buffer:
                self.write_file(self.token_buffer)
                self.token_buffer = ""
                self.last_write_time = time.time()
    
    def finalize(self) -> str:
        self.flush_buffer()
        if self.write_history: self.history.fix_separator()
        return self.complete_response
    
    def get_token_callback(self) -> Callable[[str], None]:
        """Return a callback function for token handling."""
        return self.handle_token
