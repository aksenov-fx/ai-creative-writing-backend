import os, time
from .Utility import Utility

class HistoryMixin:
    
    def __init__(self, path):
        from ..config import config

        self.path = path
        self.config = config
        self.separator = self.config.separator

        self.content = Utility.read_file(self.path)
        self.parts = self.split_history()
        self.parsed = "\n\n".join(self.parts)
        self.count = len(self.parts)
        self.assistant_response = ""
        self.part_number_content = ""
        self.removed_parts = 0

    def update_timestamp(self):
        time.sleep(0.3)
        current_time = time.time()
        os.utime(self.path, (current_time, current_time))

    def update(self, parts):
        self.parts = parts
        self.content = self.join_parts(self.parts)
        self.parsed = "\n\n".join(self.parts)
        self.count = len(self.parts)

# Return

    def split_history(self):
        parts = self.content.split(self.separator)
        parts = [part.strip() for part in parts]
        return parts
    
    def join_parts(self, content):
        return f"\n{self.separator}\n".join(content)

    def has_separator(self) -> bool:
        return self.separator in self.content

    def return_part(self, part_number):
        return self.parts[part_number].strip()

class HistoryChanger(HistoryMixin):

# Write

    def join_and_write(self):
        self.update(self.parts)
        with open(self.path, 'w', encoding='utf-8') as f: f.write(self.content)
        self.update_timestamp()

    # The method is not used yet
    def join_and_write_diff(self):
        from .Utility import Utility
        original_content = self.content
        self.update(self.parts)
        Utility.write_diff(self.path, original_content, self.content)

    def append_history(self, content: str, update: bool = False) -> None:
        self.parts[-1] += content
        if update: self.update(self.parts)
        with open(self.path, 'a', encoding='utf-8') as f: f.write(content)
        
# Change

    def fix_separator(self):
        if self.parts[-1] != "":
            self.parts.append("")
            self.join_and_write()

    def remove_last_response(self) -> None:
        self.config.interrupt_flag = True

        if self.parts[-1] == '': self.parts.pop(-2)
        else: self.parts[-1] = ""

        self.join_and_write()

    def replace_history_part(self, new_part, part_number) -> None:
        self.parts[part_number-1] = new_part.strip()
        self.join_and_write()

    def add_part(self, new_part, part_number) -> None:
        self.parts.insert(part_number, new_part.strip())
        self.join_and_write()

    def strip_lines(self):
        lines = self.parts[-1].split("\n")
        self.parts[-1] = "\n".join([line.strip() for line in lines])

class HistoryParser(HistoryMixin):

    def clear_history(self):
        self.content = ""

# Split

    def parse_assistant_response(self) -> None:

        if self.parts[-1] == '': return
        self.assistant_response = self.parts.pop()
        self.update(self.parts)

        return self

    def merge_with_summary(self, summary):

        if not summary or not summary.content: return
        if not self.config.use_summary: return

        # Keep the last part unsummarized
        if self.count == summary.count:
            self.parts[:-2] = summary.parts[:-2]
        else:
            self.parts[:len(summary.parts) - 1] = summary.parts
            
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
        return len(self.parsed) // 4
        
    def trim_content(self) -> str:
        current_tokens = self.estimate_tokens()
        
        while current_tokens > self.config.max_tokens and self.count > 0:
            self.parts.pop(0)
            self.update(self.parts)
            self.removed_parts += 1
            current_tokens = self.estimate_tokens()

        if self.removed_parts: print(f"\nRemoved {self.removed_parts} text parts to fit the token limit.")
        return self

# Process 

# Order of operations

# self.merge_with_summary(summary_object)
# self.parse_assistant_response()
# set_part_number_content
# cut_history_to_part_number
# return_last_part
# self.trim_content() 