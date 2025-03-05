import requests
import json
import sys

from typing import Optional, List, Dict, Any

def stream_response_with_openrouter_api(self, messages: List[Dict[str, str]], 
                config,
                model: str) -> None:
    try:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": config.max_tokens,
            "temperature": config.temperature,
            "stream": True,
            "include_reasoning": config.include_reasoning
        }

        endpoint = f"{self.endpoint}/chat/completions"

        response = requests.post(
            endpoint,
            headers=headers,
            json=payload,
            stream=True
        )

        first_reasoning = False if "<think>" in messages[-1]['content'] else True
        reasoning_is_complete = True if "</think>" in messages[-1]['content'] else False
        reasoning_seen = False

        for line in response.iter_lines():

            if config.interrupt_flag:
                config.interrupt_flag = False
                return
            
            if line:
                # Remove 'data: ' prefix and handle SSE format
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    line = line[6:]
                if line == '[DONE]':
                    break
                
                try:
                    chunk = json.loads(line)

                    if content := chunk.get('choices', [{}])[0].get('delta', {}).get('reasoning'):
                        reasoning_seen = True
                        if first_reasoning:
                            self.write_file(config.history_path, f"{config.reasoning_header}\n<think>\n")
                            first_reasoning = False
                        self.write_file(config.history_path, content)

                    if content := chunk.get('choices', [{}])[0].get('delta', {}).get('content'):
                        if reasoning_seen and not reasoning_is_complete:
                            self.write_file(config.history_path, "</think>\n\n")
                            reasoning_is_complete = True
                        self.write_file(config.history_path, content)
                        # Print to terminal
                        #print(content, end='', flush=True)
                        #sys.stdout.flush()

                except json.JSONDecodeError:
                    continue

        self.write_file(config.history_path, f"\n\n{config.separator}\n\n")
        
    except KeyboardInterrupt:
        print('\nProgram terminated by user')
        sys.exit(0)
    except Exception as e:
        print(f"Error during streaming: {e}")