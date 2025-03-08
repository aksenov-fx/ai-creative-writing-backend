from ..chat_settings import config

class ChatHistory:
    
    @staticmethod
    def read() -> str:
        with open(config.history_path, 'r', encoding='utf-8') as f:
            return f.read()
            
    @staticmethod
    def write_history(content: str) -> None:
        with open(config.history_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    @staticmethod
    def has_separator(content=None) -> bool:
        if content is None:
            content = ChatHistory.read()
        lines = content.splitlines()
        return any(line.strip() == config.separator for line in lines)
    
    @staticmethod
    def remove_last_response() -> None:
        content = ChatHistory.read()
        content = content.strip()
        lines = content.splitlines()

        if not ChatHistory.has_separator(content):
            ChatHistory.write_history('')
            return

        # Remove last line if last line is a separator
        if lines and lines[-1] == config.separator:
            lines[-1] = ''
            content = '\n'.join(lines).strip()

        #Remove text after the last separator
        if (pos := content.rfind(config.separator)) != -1:
            ChatHistory.write_history(content[:pos + len(config.separator)] + '\n\n')
    
    @staticmethod
    def insert(text: str) -> None:
        text = text
        existing_content = ChatHistory.read()
        ChatHistory.write_history(existing_content + text + '\n\n')

    @staticmethod
    def parse_assistant_response(history_content) -> tuple[str, str]:
        lines = history_content.splitlines()

        has_separator = ChatHistory.has_separator(history_content)
        if not has_separator or lines[-1].strip() == config.separator:
            return history_content, None
        
        parts = history_content.split(f'\n{config.separator}\n')
        history_content = f'\n{config.separator}\n'.join(parts[:-1]).strip()
        assistant_response = parts[-1].strip()
        return history_content, assistant_response

    @staticmethod
    def remove_reasoning_header(history_content: str) -> str:
        return '\n'.join(
            line 
            for line in history_content.splitlines() 
            if line != config.reasoning_header).strip()
    
    @staticmethod
    def format_history(history_content: str) -> str:
        import re
    
        pattern = r'<think>.*?</think>'

        cleaned_content = re.sub(pattern, '', history_content, flags=re.DOTALL)
        cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)
        
        cleaned_content = '\n\n'.join(
            block.strip() 
            for block in cleaned_content.split(config.separator) 
            if block.strip()
        )

        return cleaned_content