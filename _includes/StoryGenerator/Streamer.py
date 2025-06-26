import openai
import sys
from typing import Optional, List, Dict, Any
from ..chat_settings import config

class Streamer:

    def __init__(self, endpoint: str,
                 api_key: str,
                 rewriting: bool = False):
        self.endpoint = endpoint
        self.api_key = api_key
        self.rewriting = rewriting
    
    def write_file(self, filepath, content):
        if self.rewriting:
            return

        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(content)

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
            complete_response = ''

            for chunk in response:
                delta = chunk.choices[0].delta
                
                if config.interrupt_flag:
                    config.interrupt_flag = False
                    return

                # Handle reasoning content if present
                if hasattr(delta, 'reasoning') and delta.reasoning:
                    
                    if config.write_reasoning:
                        reasoning_seen = True
                        if first_reasoning:
                            self.write_file(config.history_path, f"{config.reasoning_header}\n<think>\n")
                            first_reasoning = False

                        self.write_file(config.history_path, delta.reasoning)

                    if config.print_reasoning:
                        #print(delta.reasoning.replace('.', '.\n'), end='', flush=True)
                        print(delta.reasoning, end='', flush=True)
                        sys.stdout.flush()

                # Handle regular content
                if hasattr(delta, 'content') and delta.content:

                    if reasoning_seen and not reasoning_is_complete:
                        self.write_file(config.history_path, "</think>\n\n")
                        reasoning_is_complete = True

                    self.write_file(config.history_path, delta.content)
                    
                    if config.print_output:
                        # Print each sentence from a new line
                        print(delta.content.replace('.', '.\n'), end='', flush=True) 
                        sys.stdout.flush()

                    complete_response += delta.content

            self.write_file(config.history_path, f"\n\n{config.separator}\n\n")
            
            return complete_response
            
        except KeyboardInterrupt:
            print('\nProgram terminated by user')
            sys.exit(0)
        except Exception as e:
            print(f"Error during streaming: {e}")