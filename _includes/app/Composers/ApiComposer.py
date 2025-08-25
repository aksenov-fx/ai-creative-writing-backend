from typing import List
from _includes import config
from .. import Utility

class ApiComposer:

    @staticmethod
    def append_message(messages: List, role: str, content: str) -> None:
        if content:
            messages.append({"role": role, "content": content.strip()})

    @staticmethod
    def compose_messages(system_prompt, parts) -> List:
        messages = []

        ApiComposer.append_message(messages, "system", system_prompt)

        for i, part in enumerate(parts):
            is_user_message = i % 2 == 0
            role = "user" if is_user_message else "assistant"
            ApiComposer.append_message(messages, role, part)
    
        if config.print_messages:
            Utility.print_with_newlines(messages)
            
        return messages