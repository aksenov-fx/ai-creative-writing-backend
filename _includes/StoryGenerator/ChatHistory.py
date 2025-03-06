from ..chat_settings import config

class ChatHistory:

    @staticmethod
    def read() -> str:
        with open(config.history_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    
    @staticmethod
    def remove_last_response() -> None:
        with open(config.history_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if (pos := content.rfind(config.separator)) != -1:
            with open(config.history_path, 'w', encoding='utf-8') as f:
                f.write(content[:pos + len(config.separator)] + '\n\n')
    
    @staticmethod
    def insert(text: str) -> None:
        text = text.strip()
        with open(config.history_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        with open(config.history_path, 'w', encoding='utf-8') as f:
            f.write(existing_content + text + '\n\n')

    @staticmethod
    def parse_assistant_response(history_content) -> tuple[str, str]:
        lines = history_content.splitlines()
        has_separator = any(line.strip() == config.separator for line in lines)
        
        if not has_separator:
            return '', history_content
            
        if lines[-1].strip() == config.separator:
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