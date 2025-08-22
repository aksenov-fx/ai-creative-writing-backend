from collections import OrderedDict
from .. import Utility

from .Mixins.ParserMixin import ParserMixin
from .Mixins.TrimMixin import TrimMixin
from .Mixins.CommonMixin import CommonMixin

class SummaryMixin(CommonMixin):
    
    def __init__(self, path):
        from ...config import config

        self.path = path
        self.config = config
        self.separator = self.config.separator

        self.yaml_data = Utility.read_yaml(self.path)
        self.keys = []
        self.parts = []
        self.parsed = ""
        self.count = 0

        self.part_number_content = ""
        self.assistant_response = ""

        self.parts_to_trim = 1
        self.removed_parts = 0

        self.update_from_yaml()

    def _extract_parts_from_yaml(self):
        return [part['part_text'].strip() for part in self.yaml_data.values()]

    def update_from_yaml(self):
        self.keys = list(self.yaml_data.keys())
        self.parts = self._extract_parts_from_yaml()
        self.parsed = self.join_parts(self.parts)
        self.count = len(self.parts)
        
    def update_hashes(self):
        return #dummy method

class SummaryChanger(SummaryMixin):

    def write_summary(self):
        Utility.write_yaml(self.path, self.yaml_data, self.config)

        # Write human readable summary
        summary_md_path = self.config.folder_path + self.config.summary_md_path
        Utility.write_file(summary_md_path, self.parsed, self.config)

    def update_from_story_parts(self, story):
        """
        Update the summary from the story parts.
        
        On first run, the summary for each part will have the same text as the story part.
        Each part will get a calculated hash and summarized flag set to False.
        On subsequent runs, the method will find parts without matching hash and copy them to summary.
        The summarized flag will be set to false.
        Summaries without matching hashes in the story will be removed from summary.
        
        Note: The actual summarization happens in Summarizer.py
        """
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
        self.update_from_yaml()
        self.write_summary()

        return self

    def replace_history_part(self, new_part, hash_key) -> None:
        self.yaml_data[hash_key]['part_text'] = new_part.strip()
        self.update_from_yaml()
        self.write_summary()

class SummaryParser(SummaryMixin, ParserMixin, TrimMixin):
    pass