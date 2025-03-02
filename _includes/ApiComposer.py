from typing import Optional, List, Dict, Any

class ApiComposer:
    def estimate_tokens(self, text: str) -> int:
        return len(text) // 4
        
    def trim_content(self, content: str, max_tokens: int) -> str:
        paragraphs = content.split('\n\n')
        current_tokens = self.estimate_tokens(content)
        
        while current_tokens > max_tokens and len(paragraphs) > 1:
            paragraphs.pop(0)
            content = '\n\n'.join(paragraphs)
            current_tokens = self.estimate_tokens(content)
            
        return content
        
    def compose_messages(self, config, 
                        history: Optional[str] = None,
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
                "content": f"{config.user_preprompt}{config.user_prompt}{config.user_postprompt}".strip()
        })
        
        if assistant_response:
            messages.append({"role": "assistant", "content": assistant_response})
        
        return messages