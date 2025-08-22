from .. import Utility

from .Mixins.ParserMixin import ParserMixin
from .Mixins.ChangerMixin import ChangerMixin
from .Mixins.TrimMixin import TrimMixin
from .Mixins.CommonMixin import CommonMixin

class StoryMixin(CommonMixin):
    
    def __init__(self, path):
        from ...config import config

        self.path = path
        self.config = config
        self.separator = self.config.separator

        self.content = Utility.read_file(self.path)
        self.parts = self.split_history()
        self.parsed = "\n\n".join(self.parts)
        self.count = len(self.parts)
        self.assistant_response = ""
        self.part_number_content = ""
        self.hashes = {}

        self.parts_to_trim = 1
        self.removed_parts = 0

# Return

    def split_history(self):
        parts = self.content.split(self.separator)
        parts = [part.strip() for part in parts]
        return parts
    
    def join_parts(self, content):
        return f"\n{self.separator}\n".join(content)

    def return_part(self, part_number):
        return self.parts[part_number].strip()
    
    def update_hashes(self):
        hashes = {}
        for part_text in self.parts:
            if not part_text or not part_text.strip(): continue
            part_hash = Utility.calculate_hash(part_text)
            hashes[part_hash] = part_text.strip()

        self.hashes = hashes

class StoryChanger(StoryMixin, ChangerMixin, TrimMixin):

# Change

    def fix_separator(self):
        if self.parts[-1] != "":
            self.append_history(f"\n{self.separator}\n")
            Utility.update_timestamp(self.path, self.config)

    def remove_last_response(self) -> None:
        self.config.interrupt_flag = True

        if self.parts[-1] == '': self.parts.pop(-2)
        else: self.parts[-1] = ""

        self.join_and_write()

    def change_history_part(self, content, part_number, append=False) -> None:
        if append:
            self.parts[part_number-1] += content
        else:
            self.parts[part_number-1] = content.strip()
        self.join_and_write()

    def add_part(self, new_part, part_number) -> None:
        self.parts.insert(part_number, new_part.strip())
        self.join_and_write()

class StoryParser(StoryMixin, ParserMixin, TrimMixin):

# Split

    def set_assistant_response(self, part_number: int) -> None:
        self.assistant_response = self.parts.pop()
        self.update(self.parts)
        return self

    def merge_with_summary(self, summary):
        """
        Replace full story parts with summarized parts.
        
        The summarized versions are read from the config.summary_yaml_path file.
        The parts are matched by hash.
        If some part of the story changed - it will not be replaced with summary.

        If the number of story parts is equal to the number of summarized parts,
        the last part is not summarized to preserve writing style.

        For details on how summary is created, see update_from_story_parts method in Summary.py
        And update_summary in Summarizer.py
        """

        if not self.config.use_summary: return
        if not summary or not summary.yaml_data: return

        self.update_hashes()
        if not self.hashes: return

        hash_keys = list(self.hashes.keys())
        hashes_to_process = hash_keys[:-1] if len(self.hashes) <= len(summary.yaml_data) else hash_keys
        
        for i, part_hash in enumerate(hashes_to_process):
            if part_hash in summary.yaml_data:
                self.parts[i] = summary.yaml_data[part_hash]['part_text']
            
        self.update(self.parts)
        return self
