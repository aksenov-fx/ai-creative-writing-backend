from .. import Utility
from .Mixins.ChangerMixin import ChangerMixin
from .Mixins.TrimMixin import TrimMixin

class ChatHistoryMixin:
    
    def __init__(self, path):
        from ...config import config

        self.path = path

        self.content = Utility.read_file(self.path)
        self.custom_instructions = self.content.split("```")[1].partition(":")[2].strip()

        self.model = config.model
        self.config = config
        self.separator = self.config.separator
        self.splitter = self.config.splitter

        self.all_parts = self.split_parts()
        self.parts = self.all_parts[2:]
        self.parts_even = False
        self.count = 0

        self.parts_to_trim = 2
        self.removed_parts = 0

        self.update(self.parts)

    def update(self, parts):
        self.parts = parts
        self.parts_even = len(self.parts) % 2 == 0
        self.all_parts = self.all_parts[:2] + self.parts
        self.count = len(self.parts)
        self.content = self.join_parts(self.all_parts)

# Return

    def split_parts(self, content=None):
        if not content: content = self.content
        parts = content.split(self.separator)
        parts = [part.strip() for part in parts]
        return parts
    
    def join_parts(self, content):
        return f"\n{self.separator}\n".join(content)

class ChatHistoryChanger(ChatHistoryMixin, ChangerMixin):
    """
    A class that represents a chat md file.
    Handles file changes.
    """


# Change

    def fix_separator(self):
        if self.parts[-1] == "" or self.parts[-1].strip() == "#": return

        self.append_separator()
        if self.config.add_header and not self.parts_even: self.append_history("# ")
        Utility.update_timestamp(self.path, self.config)

        return self

    def remove_last_response(self) -> None:
        self.config.interrupt_flag = True

        if self.parts_even: self.parts = self.parts[:-1]
        else: self.parts = self.parts[:-2]

        self.join_and_write()
        return self

class ChatHistoryParser(ChatHistoryMixin, TrimMixin):
    """
    A class that represents a chat md file.
    Handles file parsing for composing API request.
    Can not change the file.
    """

    def split_conversation(self):   
        if not self.splitter in self.content: return

        content = self.join_parts(self.parts)
        content = content.split(self.splitter)[-1]
        parts = self.split_parts(content)
        self.update(parts)

    def clean_header(self):
        """
        Remove the "# " prefix from the user messages.

        This prefix is added if config.add_header is True.
        The purpose of header is to make it easier to identify user messages.
        """
        for i, part in enumerate(self.parts):
            if i % 2 == 0 and part.startswith("# "): self.parts[i] = part[2:]
        self.update(self.parts)

    def include_file(self):
        """
        Include the content of the file specified in config.include_file.
        
        The content is appended to the first user message.
        config.include_file is set in get_chat_config method, 
        if chat_with_story or chat_with_summary is True.
        """

        if not self.config.include_file: return

        if not Utility.read_file(self.config.include_file): 
            raise FileNotFoundError(f"File is empty or not found: {self.config.include_file}")

        included_content = Utility.read_file(self.config.include_file)
        included_parts = self.split_parts(included_content)
        included_content = "\n\n".join(included_parts)

        self.parts[0] = f"{self.parts[0]}\n\n{included_content}" 
        self.update(self.parts)

    def parse_instructions(self):
        """
        Parse the instructions from the custom instructions section of md file.
        """
        return Utility.read_instructions(self.custom_instructions, self.config.custom_instructions_folder)

# Process
    def process(self):
        self.split_conversation()
        self.clean_header()
        if self.config.trim_history: self.trim_content()
        self.include_file()
        self.custom_instructions = self.parse_instructions()