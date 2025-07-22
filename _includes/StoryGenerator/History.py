import re

class History:
    
    def __init__(self, path, config):
        self.config = config
        self.separator = self.config.separator
        self.path = path
        self.content = self._read_file()
        self.assistant_response = None
        self.part_number_content = ""
    
    def _read_file(self) -> str:
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                return f.read() or ""
        except FileNotFoundError:
            return ""
    
    def reset(self, new_path=None):
        if new_path:
            self.path = new_path
        self.content = self._read_file()
        self.assistant_response = None
        self.part_number_content = None
    
    def clear_history(self):
        self.content = ""

# Write

    def write_history(self, content: str = None) -> None:
        self.content = content
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(content)

    def append_history(self, content: str) -> None:
        self.content += content
        with open(self.path, 'a', encoding='utf-8') as f:
            f.write(content)

# Change

    def insert_separator(self):
        lines = self.content.strip().splitlines()
        if lines and lines[-1] != self.separator:
            self.append_history(f"\n\n{self.separator}\n\n")

    def remove_last_response(self) -> None:
        self.config.interrupt_flag = True

        if not self.has_separator():
            self.write_history('')
            return
        
        self.insert_separator()
        history_split = self.split_history()
        history_split.pop(-2)

        history_content = self.join_history(history_split)
        self.write_history(history_content)

    def replace_history_part(self, new_part) -> None:
        history_split = self.split_history()
        new_part = '\n\n' + new_part + '\n\n'

        splitter = '</think>'
        if splitter in history_split[self.config.part_number-1]:
            think_part, _ = history_split[self.config.part_number-1].split(splitter, 1)
            history_split[self.config.part_number-1] = think_part + splitter + new_part
        else:
            history_split[self.config.part_number-1] = new_part
            
        history_content = self.join_history(history_split)

        self.write_history(history_content)

    def add_part(self, new_part) -> None:
        history_split = self.split_history()
        new_part = '\n\n' + new_part.strip() + '\n\n'

        history_split.insert(self.config.part_number, new_part)
        history_content = self.join_history(history_split)
        self.write_history(history_content)
        
    def remove_reasoning(self):
        self.remove_reasoning_header()
        self.remove_reasoning_tokens()
        self.content += '\n\n'
        self.write_history(self.content)

# Return

    def split_history(self):
        return self.content.split(self.separator)
    
    def join_history(self, content):
        return self.separator.join(content)

    def lines(self):
        return self.content.splitlines()

    def read(self) -> str:
        return self.content
    
    def has_separator(self) -> bool:
        return any(line.strip() == self.separator for line in self.lines())

    def count_parts(self) -> int:
        return sum(1 for line in self.lines() if line.strip() == self.separator)

    def return_part(self, part_number):
        return self.split_history()[part_number].strip()

# Split

    def parse_assistant_response(self) -> None:

        if not self.has_separator() or self.lines()[-1].strip() == self.separator:
            self.assistant_response = None
            return
        
        parts = self.content.split(f'\n{self.separator}\n')
        self.content = f'\n{self.separator}\n'.join(parts[:-1]).strip()
        self.assistant_response = parts[-1].strip()

    def merge_with_summary(self, summary):

        if not summary or not summary.content: return
        
        history_split = self.split_history()
        summary_split = summary.content.split(self.separator)
        
        number_of_history_parts = self.count_parts()
        number_of_summary_parts = summary.count_parts()

        # Keep the last part unsummarized
        if number_of_history_parts == number_of_summary_parts:
            summary_content = self.join_history(summary_split[:-2])
            number_of_summary_parts -= 1
        else:
            summary_content = summary.content
        
        history_content = self.join_history(history_split[number_of_summary_parts:])
        merged_history = summary_content + history_content

        self.content = merged_history

    def cut_history_to_part_number(self):
        history_split = self.split_history()
        self.content = self.join_history(history_split[:self.config.part_number-1])
        self.part_number_content = history_split[self.config.part_number-1]

    def return_last_part(self):
        history_split = self.split_history()
        self.content = history_split[-1]

# Parse
    def remove_reasoning_header(self) -> None:
        self.content = '\n'.join(
            line 
            for line in self.lines() 
            if line != self.config.reasoning_header).strip()
    
    def clean_reasoning_tokens(self, text: str) -> str:
        pattern = r'<think>.*?</think>'
        cleaned_content = re.sub(pattern, '', text, flags=re.DOTALL)
        cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)
        return cleaned_content

    def remove_reasoning_tokens(self) -> None:
        self.content = self.clean_reasoning_tokens(self.content)

    def remove_reasoning_tokens_from_assistance_reponse(self) -> None:
        self.assistant_response = self.clean_reasoning_tokens(self.assistant_response)

    def format_history(self) -> None:
        cleaned_content = '\n\n'.join(
            block.strip() 
            for block in self.content.split(self.separator) 
            if block.strip()
        )

        self.content = cleaned_content

    def estimate_tokens(self) -> int:
        return len(self.content) // 4
        
    def trim_content(self) -> str:
        content = self.content
        paragraphs = self.content.split('\n\n')
        current_tokens = self.estimate_tokens()
        
        while current_tokens > self.config.max_tokens and len(paragraphs) > 1:
            paragraphs.pop(0)
            content = '\n\n'.join(paragraphs)
            current_tokens = self.estimate_tokens(content)

        self.content = content

# Process
    def process_history(self, summary_object=None, no_summary: bool = False, cut_history_to_part_number: bool = False, return_last_part: bool = False):

        if self.config.use_summary and not no_summary: self.merge_with_summary(summary_object)
        self.remove_reasoning_header()
        self.parse_assistant_response()
        self.remove_reasoning_tokens()
        if cut_history_to_part_number: self.cut_history_to_part_number()
        if return_last_part: self.return_last_part()
        self.format_history() # Remove separators and extra empyty lines
        self.trim_content() # Exclude first paragraphs to match input length with max_tokens