from typing import Optional, List, Dict
from _includes import config
from ..Utility.Utility import Utility

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
    
    @staticmethod
    def compose_chat_messages(history) -> List[Dict[str, str]]:
        messages = []

        ApiComposer.append_message(messages, "system", history.custom_instructions)

        for i, part in enumerate(history.parts):
            part_even = i % 2 == 0
            role = "user" if part_even else "assistant"
            ApiComposer.append_message(messages, role, part)
    
        if config.print_messages:
            Utility.print_with_newlines(messages)
            
        return messages