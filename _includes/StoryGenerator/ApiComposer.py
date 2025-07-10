import json

from typing import Optional, List, Dict, Any
from ..settings import config

class ApiComposer:

    @staticmethod
    def estimate_tokens(text: str) -> int:
        return len(text) // 4
        
    @staticmethod
    def trim_content(content: str, max_tokens: int) -> str:
        paragraphs = content.split('\n\n')
        current_tokens = ApiComposer.estimate_tokens(content)
        
        while current_tokens > max_tokens and len(paragraphs) > 1:
            paragraphs.pop(0)
            content = '\n\n'.join(paragraphs)
            current_tokens = ApiComposer.estimate_tokens(content)
            
        return content
    
    @staticmethod
    def print_with_newlines(obj):
        json_str = json.dumps(obj, indent=2, ensure_ascii=False)
        formatted_str = json_str.replace('\\n', '\n')
        print(formatted_str)

    @staticmethod
    def append_message(messages: List[Dict[str, str]], role: str, content: Optional[str]) -> None:
        if content:
            messages.append({"role": role, "content": content.strip()})

    @staticmethod
    def compose_messages(user_prompt, assistant_response) -> List[Dict[str, str]]:
        messages = []

        ApiComposer.append_message(messages, "system",       config.system_prompt)
        ApiComposer.append_message(messages, "user",         user_prompt)
        ApiComposer.append_message(messages, "assistant",    assistant_response)
    
        if config.print_messages:
            ApiComposer.print_with_newlines(messages)
            
        return messages