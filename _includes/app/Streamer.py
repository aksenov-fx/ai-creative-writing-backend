import openai
import sys
import time
import threading
from typing import List, Dict

from _includes import config

class Streamer:

    def __init__(self, history_object: str,
                 rewriting: bool = False,
                 part_number: int = 0):
        self.history = history_object
        self.endpoint = config.endpoint['url']
        self.api_key = config.endpoint['api_key']
        self.rewriting = rewriting
        self.part_number = part_number
        self.token_buffer = ""
        self.complete_response = ""
        self.last_write_time = time.time()
        self.buffer_lock = threading.Lock()
    
    def write_file(self, content):
        if self.rewriting:
            self.history.replace_history_part(self.complete_response, self.part_number)
        else:
            self.history.append_history(content)

    def buffer_and_write(self, content):
        with self.buffer_lock:
            self.token_buffer += content
            
            if time.time() - self.last_write_time >= config.write_interval:
                self.write_file(self.token_buffer)
                self.token_buffer = ""
                self.last_write_time = time.time()

    def flush_buffer(self):
        with self.buffer_lock:
            if self.token_buffer:
                self.write_file(self.token_buffer)
                self.token_buffer = ""
                self.last_write_time = time.time()

    def stream_response(self, messages: List[Dict[str, str]]) -> None:

        try:
            client = openai.OpenAI(base_url=self.endpoint, api_key=self.api_key)

            response = client.chat.completions.create(
                model=config.model['name'],
                messages=messages,
                stream=True,
                #max_tokens=config.max_tokens,
                temperature=config.temperature,
                extra_body={ "include_reasoning": config.include_reasoning }
            )

            for chunk in response:
                delta = chunk.choices[0].delta
                self.complete_response += delta.content
                
                if config.interrupt_flag:
                    config.interrupt_flag = False
                    return

                # Handle reasoning content if present
                if hasattr(delta, 'reasoning') and delta.reasoning and config.print_reasoning:
                    print(delta.reasoning, end='', flush=True)
                    sys.stdout.flush()

                # Handle regular content
                if hasattr(delta, 'content') and delta.content:
                    self.buffer_and_write(delta.content)
                
            self.flush_buffer()
            self.history.fix_separator()
            
            return self.complete_response
            
        except KeyboardInterrupt:
            print('\nProgram terminated by user')
            sys.exit(0)