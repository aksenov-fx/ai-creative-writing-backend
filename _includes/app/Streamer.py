import openai
import sys
from typing import List, Dict, Callable

from _includes import config

class Streamer:

    def __init__(self, token_callback: Callable[[str], None]):
        self.token_callback = token_callback
        self.endpoint = config.endpoint['url']
        self.api_key = config.endpoint['api_key']
    
    def stream_response(self, messages: List[Dict[str, str]]) -> None:

        try:
            client = openai.OpenAI(base_url=self.endpoint, api_key=self.api_key)

            response = client.chat.completions.create(
                model=config.model,
                messages=messages,
                stream=True,
                temperature=config.temperature,
                extra_body={ "include_reasoning": config.include_reasoning }
            )

            for chunk in response:
                delta = chunk.choices[0].delta
                
                if config.interrupt_flag:
                    config.interrupt_flag = False
                    break

                # Handle reasoning content if present
                if hasattr(delta, 'reasoning') and delta.reasoning and config.print_reasoning:
                    print(delta.reasoning, end='', flush=True)
                    sys.stdout.flush()

                # Handle regular content
                if hasattr(delta, 'content') and delta.content:
                    self.token_callback(delta.content)
            
        except KeyboardInterrupt:
            print('\nProgram terminated by user')
            sys.exit(0)
        except Exception as e:
            raise
