class HistoryMixin:
    
    def __init__(self, path):
        from ..config import config

        self.path = path
        self.config = config
        self.separator = self.config.separator

        self.content = self._read_file().strip()
        self.parts = self.split_history()
        self.lines = self.content.splitlines()
        self.count = len(self.parts)
        self.assistant_response = ""
        self.part_number_content = ""

    def _read_file(self) -> str:
        try: 
            with open(self.path, 'r', encoding='utf-8') as f: return f.read() or ""
        except FileNotFoundError: 
            return ""
    
    def refresh(self, new_path=None):
        if new_path: self.path = new_path
        self.__init__(self.path)
    
# Return

    def split_history(self):
        parts = self.content.split(self.separator)
        parts = [part.strip() for part in parts]
        return parts
    
    def join_parts(self, content):
        return f"\n\n{self.separator}\n\n".join(content)

    def has_separator(self) -> bool:
        return self.separator in self.lines

    def return_part(self, part_number):
        return self.parts[part_number].strip()

class HistoryChanger(HistoryMixin):

# Write

    def write_history(self, content: str = None) -> None:
        open(self.path, 'w', encoding='utf-8').write(content)
        self.refresh()

    def append_history(self, content: str) -> None:
        open(self.path, 'a', encoding='utf-8').write(content)
        self.refresh()
        
    def join_and_write(self):
        self.write_history(self.join_parts(self.parts))
        self.refresh()

# Change

    def fix_separator(self):
        if self.lines[-1] != self.separator:
            self.parts.append("")
            self.join_and_write()

    def remove_last_response(self) -> None:
        self.config.interrupt_flag = True

        if self.lines[-1] == self.separator: self.parts.pop(-2)
        else: self.parts[-1] = ""

        self.join_and_write()

    def replace_history_part(self, new_part, part_number) -> None:
        self.parts[part_number-1] = new_part.strip()
        self.join_and_write()

    def add_part(self, new_part, part_number) -> None:
        self.parts.insert(part_number, new_part.strip())
        self.join_and_write()

class HistoryParser(HistoryMixin):

    def update(self, parts):
        self.parts = parts
        self.content = self.join_parts(self.parts).strip()
        self.parsed = "\n\n".join(self.parts).strip()
        self.lines = self.content.splitlines()
        self.count = len(self.parts)

    def clear_history(self):
        self.content = ""

# Split

    def parse_assistant_response(self) -> None:

        if self.lines[-1].strip() == self.separator: return
        
        self.assistant_response = self.parts[-1]
        self.parts = self.parts[:-1]

        self.update(self.parts)
        return self

    def merge_with_summary(self, summary):

        if not summary or not summary.content: return
        if not self.config.use_summary: return

        # Keep the last part unsummarized
        if self.count == summary.count:
            self.parts[:-2] = summary.parts[:-2]
        else:
            self.parts[:len(summary.parts)] = summary.parts
            
        self.update(self.parts)
        return self

    def cut_history_to_part_number(self, part_number):
        self.update(self.parts[:part_number])
        return self

    def set_part_number_content(self, part_number):
        self.part_number_content = self.parts[part_number-1]
        return self

    def set_to_previous_part(self):
        self.update(self.parts[-2:-1])
        return self

    def cut(self, part_number):
        if self.config.include_previous_part_when_rewriting: 
            (self
            .cut_history_to_part_number(part_number)
            .set_part_number_content(part_number)
            .set_to_previous_part())
        else:
            self.clear_history()

# Trim

    def estimate_tokens(self) -> int:
        return len(self.content) // 4
        
    def trim_content(self) -> str:
        paragraphs = self.content.split('\n\n')
        current_tokens = self.estimate_tokens()
        
        while current_tokens > self.config.max_tokens and len(paragraphs) > 1:
            paragraphs.pop(0)
            self.content = '\n\n'.join(paragraphs)
            current_tokens = self.estimate_tokens(self.content)
            
        return self

# Process 

# Order of operations

# self.merge_with_summary(summary_object)
# self.parse_assistant_response()
# set_part_number_content
# cut_history_to_part_number
# return_last_part
# self.trim_content() 