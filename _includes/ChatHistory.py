class ChatHistory:
    def __init__(self, config):
        self.separator = config.separator
        self.filepath = config.history_path

    def read(self) -> str:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return f.read().strip()
    
    def remove_last_response(self) -> None:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if (pos := content.rfind(self.separator)) != -1:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                f.write(content[:pos + len(self.separator)] + '\n\n')
    
    def insert(self, text: str) -> None:
        text = text.strip()
        with open(self.filepath, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        with open(self.filepath, 'w', encoding='utf-8') as f:
            f.write(existing_content + text + '\n\n')

    def parse_assistant_response(self) -> tuple[str, str]:
        history_content = self.read()
        lines = history_content.splitlines()
        has_separator = any(line.strip() == self.separator for line in lines)
        
        if not has_separator:
            return '', history_content
            
        if lines[-1].strip() == self.separator:
            return history_content, None
        
        parts = history_content.split(f'\n{self.separator}\n')
        history_content = f'\n{self.separator}\n'.join(parts[:-1]).strip()
        assistant_response = parts[-1].strip()
        return history_content, assistant_response
    
    def format_history(self, history_content: str) -> str:
        return '\n\n'.join(
            block.strip() 
            for block in history_content.split(self.separator) 
            if block.strip()
        )