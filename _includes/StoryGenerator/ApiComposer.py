from typing import Optional, List, Dict, Any
from ..chat_settings import config

class ChatHistory:

    @staticmethod
    def read() -> str:
        with open(config.history_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    
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
    def compose_messages(history: Optional[str] = None,
                        assistant_response: Optional[str] = None) -> List[Dict[str, str]]:
        messages = []

        if config.system_prompt:
            messages.append({"role": "system", "content": config.system_prompt})

        if config.first_prompt:
            messages.append({"role": "user", "content": config.first_prompt})

        if history:
            messages.append({"role": "assistant", "content": history})

        if history and config.user_prompt:
            messages.append({
                "role": "user",
                "content": f"{config.user_prompt}".strip()
        })
        
        if assistant_response:
            messages.append({"role": "assistant", "content": assistant_response})
        
        return messages