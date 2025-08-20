from .. import Utility
from .Mixins.ChangerMixin import ChangerMixin

class PromptChanger(ChangerMixin):
    def __init__(self, path):
        from ...config import config
        
        self.path = path
        self.config = config
        self.separator = self.config.separator

        self.content = Utility.read_file(self.path)
        self.parts = self.split_history()

    def split_history(self):
        parts = self.content.split(self.separator)
        parts = [part.strip() for part in parts]
        return parts
    
    def return_part(self, part_number):
        return self.parts[part_number].strip()
    
    def fix_separator(self):
        if self.parts[-1] != "":
            self.append_history(f"\n{self.separator}\n")
            Utility.update_timestamp(self.path)

    def get_user_prompt(self, part_value: int, abbreviations: dict) -> str:
        from ..Composers.PromptComposer import expand_abbreviations
        
        prompt = self.return_part(part_value - 1)
        prompt = expand_abbreviations(prompt, abbreviations)
        print(prompt)
        
        self.fix_separator()
        return prompt