import openai
import sys
import time
import threading
from typing import List, Dict

from _includes import config

class Streamer:

    def __init__(self, history_object: str,
                 endpoint: str,
                 api_key: str,
                 rewriting: bool = False):
        self.history_object = history_object
        self.filepath = history_object.path
        self.endpoint = endpoint
        self.api_key = api_key
        self.rewriting = rewriting
        self.token_buffer = ""
        self.complete_response = ""
        self.last_write_time = time.time()
        self.buffer_lock = threading.Lock()
    
    def write_file(self, filepath, content):
        if self.rewriting:
            self.history_object.replace_history_part(self.complete_response)
        else:
            with open(filepath, 'a', encoding='utf-8') as f: f.write(content)

    def buffer_and_write(self, filepath, content):
        with self.buffer_lock:
            self.token_buffer += content
            current_time = time.time()
            
            if current_time - self.last_write_time >= config.write_interval:
                self.write_file(filepath, self.token_buffer)
                self.token_buffer = ""
                self.last_write_time = current_time

    def flush_buffer(self, filepath):
        with self.buffer_lock:
            if self.token_buffer:
                self.write_file(filepath, self.token_buffer)
                self.token_buffer = ""
                self.last_write_time = time.time()

    def stream_response(self, messages: List[Dict[str, str]], 
                                        model: str) -> None:

        try:
            client = openai.OpenAI(base_url=self.endpoint, api_key=self.api_key)

            response = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                extra_body={
                    "include_reasoning": config.include_reasoning
                }
            )

            first_reasoning = False if "<think>" in messages[-1]['content'] else True
            reasoning_is_complete = True if "</think>" in messages[-1]['content'] else False
            reasoning_seen = False

            for chunk in response:
                delta = chunk.choices[0].delta
                self.complete_response += delta.content
                
                if config.interrupt_flag:
                    config.interrupt_flag = False
                    return

                # Handle reasoning content if present
                if hasattr(delta, 'reasoning') and delta.reasoning:
                    
                    if config.write_reasoning:
                        reasoning_seen = True
                        if first_reasoning:
                            self.write_file(self.filepath, f"{config.reasoning_header}\n<think>\n")
                            first_reasoning = False

                        self.buffer_and_write(self.filepath, delta.reasoning)

                    if config.print_reasoning:
                        print(delta.reasoning, end='', flush=True)
                        sys.stdout.flush()

                # Handle regular content
                if hasattr(delta, 'content') and delta.content:

                    if reasoning_seen and not reasoning_is_complete:
                        self.flush_buffer(self.filepath)
                        self.write_file(self.filepath, "</think>\n\n")
                        reasoning_is_complete = True

                    self.buffer_and_write(self.filepath, delta.content)
                    
                    if config.print_output:
                        # Print each sentence from a new line
                        print(delta.content.replace('.', '.\n'), end='', flush=True) 
                        sys.stdout.flush()

            self.flush_buffer(self.filepath)
            self.write_file(self.filepath, f"\n\n{config.separator}\n\n")
            
            return self.complete_response
            
        except KeyboardInterrupt:
            print('\nProgram terminated by user')
            sys.exit(0)
        except Exception as e:
            print(f"Error during streaming: {e}")