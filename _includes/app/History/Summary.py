import os, time
from collections import OrderedDict
from ..Utility import Utility

class SummaryMixin:
    
    def __init__(self, path):
        from ...config import config

        self.path = path
        self.config = config
        self.separator = self.config.separator

        self.yaml_data = Utility.read_yaml(self.path)
        self.parts = self._extract_parts_from_yaml()
        self.parsed = self.join_parts(self.parts)
        self.count = len(self.parts)
        self.part_number_content = ""
        self.assistant_response = ""

    def _extract_parts_from_yaml(self):
        return [part['part_text'].strip() for part in self.yaml_data.values()]

    def _save_yaml(self):
        Utility.write_yaml(self.path, self.yaml_data)

    def update(self, parts):
        self.parts = parts
        self.parsed = self.join_parts(self.parts)
        self.count = len(self.parts)

# Return

    def join_parts(self, content):
        return f"\n{self.separator}\n".join(content)

class SummaryChanger(SummaryMixin):

# Write

    def join_and_write(self):
        self.update(self.parts)
        self._save_yaml()
        self.update_timestamp()

        summary_md_path = self.config.folder_path + self.config.summary_md_path
        Utility.write_file(summary_md_path, self.parsed)

    def update_timestamp(self):
        time.sleep(0.3)
        current_time = time.time()
        os.utime(self.path, (current_time, current_time))

    def update_from_story_parts(self, story):
        current_hashes = list(story.hashes.keys())
        new_yaml_data = OrderedDict()
        
        for part_hash in current_hashes:
            if part_hash in self.yaml_data:
                new_yaml_data[part_hash] = self.yaml_data[part_hash]
            else:
                new_yaml_data[part_hash] = {
                    'summarized': False,
                    'part_text': story.hashes[part_hash]
                }
        
        self.yaml_data = new_yaml_data
        self.parts = self._extract_parts_from_yaml()
        self.join_and_write()
    
# Change

    def replace_history_part(self, new_part, hash_key) -> None:
        self.yaml_data[hash_key]['part_text'] = new_part.strip()
        self.parts = self._extract_parts_from_yaml()
        self.join_and_write()

class SummaryParser(SummaryMixin):

# Split

    def cut_history_to_part_number(self, part_number):
        self.update(self.parts[:part_number])
        return self

    def set_part_number_content(self, part_number):
        self.part_number_content = self.parts[part_number-1]
        return self

    def set_to_previous_part(self):
        self.update(self.parts[-2:-1])
        return self

    def cut(self, part_number, include_previous_part):
        if include_previous_part: 
            (self
            .cut_history_to_part_number(part_number)
            .set_part_number_content(part_number)
            .set_to_previous_part())
        else:
            self.parts = []
            self.parsed = ""

    def trim_content(self):
        return self