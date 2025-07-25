from typing import Optional, List, Dict, Any
from _includes import config
from .Utility import Utility

class ApiComposer:

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
            Utility.print_with_newlines(messages)
            
        return messages