import openai
import sys

from typing import Optional, List, Dict, Any

def stream_response_with_openai_client(self, messages: List[Dict[str, str]], 
                    config,
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
            
            # Handle reasoning content if present
            if hasattr(delta, 'reasoning') and delta.reasoning:
                reasoning_seen = True
                if first_reasoning:
                    self.write_file(config.history_path, "<think>\n")
                    first_reasoning = False
                self.write_file(config.history_path, delta.reasoning)
                # print(delta.reasoning_content, end='', flush=True)
                # sys.stdout.flush()
            
            # Handle regular content if present
            if hasattr(delta, 'content') and delta.content:
                if reasoning_seen and not reasoning_is_complete:
                    self.write_file(config.history_path, "</think>\n\n")
                    reasoning_is_complete = True
                self.write_file(config.history_path, delta.content)
                # print(delta.content, end='', flush=True)
                # sys.stdout.flush()

        self.write_file(config.history_path, f"\n\n{config.separator}\n\n")
            
    except KeyboardInterrupt:
        print('\nProgram terminated by user')
        sys.exit(0)
    except Exception as e:
        print(f"Error during streaming: {e}")