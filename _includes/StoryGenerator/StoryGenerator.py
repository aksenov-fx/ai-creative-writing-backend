import shutil, os

from .ApiComposer import ApiComposer
from .Utility import Utility
from .Streamer import Streamer
from _includes import config, story, summary, story_parsed, summary_parsed
from .History import HistoryChanger, HistoryParser

### Chat

class StoryGenerator:

    @staticmethod
    def chat(history_object: HistoryChanger,
             history_parsed: HistoryParser,
             first_prompt: str, 
             user_prompt: str, 
             rewrite: bool = False,
             part_number: int = 0) -> None:

        story_parsed.trim_content()
        history_content = "\n\n" + config.history_prefix + "\n" + history_parsed.parsed if history_parsed.content else ""

        first_prompt = Utility.expand_abbreviations(first_prompt)
        user_prompt = Utility.expand_abbreviations(user_prompt)
        user_prompt = first_prompt + history_content + "\n\n" + user_prompt + "\n" + history_parsed.part_number_content

        messages = ApiComposer.compose_messages(user_prompt, history_parsed.assistant_response)
        story_parsed.refresh()

        if not config.debug: 
            streamer = Streamer(history_object, rewrite, part_number)
            streamer.stream_response(messages)

    ### Generator

    @staticmethod
    def generate(first_prompt: str, user_prompt: str) -> None:

        story_parsed.merge_with_summary(summary)
        story_parsed.parse_assistant_response()

        StoryGenerator.chat(story, story_parsed, first_prompt, user_prompt)

    @staticmethod
    def regenerate(first_prompt: str, user_prompt: str, part_number: int) -> None:

        story_parsed.merge_with_summary(summary)
        story_parsed.cut_history_to_part_number(part_number-1)

        StoryGenerator.chat(story, story_parsed, first_prompt, user_prompt, rewrite=True, part_number=part_number)

    @staticmethod
    def add_part(first_prompt: str, user_prompt: str, part_number: int) -> None:

        story.add_part("", part_number)

        story_parsed.merge_with_summary(summary)
        story_parsed.cut_history_to_part_number(part_number)
        part_number += 1

        StoryGenerator.chat(story, story_parsed, first_prompt, user_prompt, rewrite=True, part_number=part_number)

    ### Changer

    @staticmethod
    def change_part(first_prompt: str, user_prompt: str, part_number: int) -> None:

        story_parsed.cut(part_number)
        StoryGenerator.chat(story, story_parsed, "", user_prompt, rewrite=True, part_number=part_number)

    @staticmethod
    def change_parts(first_prompt: str, user_prompt: str, part_number: int) -> None:
        
        print(f"Rewriting part {part_number}/{story.count-1}")

        for part in range(part_number, story.count):
            StoryGenerator.change_part("", user_prompt, part)

    ### Summarizer

    @staticmethod
    def summarize_part(user_prompt: str, part_number: int) -> None:

        part_number += 1
        print(f"Summarizing part {part_number}/{story.count-1}")

        summary_parsed.refresh()
        summary_parsed.cut(part_number)

        StoryGenerator.chat(summary, summary_parsed,  "", user_prompt, rewrite=True)
        
    @staticmethod
    def summarize_all(user_prompt: str) -> None:

        if os.path.exists(summary.path):
            raise FileExistsError(f"Summary already exists. Please delete it before creating a new one.")
        shutil.copy(story.path, summary.path)

        summary.refresh()

        for part_number in range(summary.count-1):
            StoryGenerator.summarize_part(user_prompt, part_number)

    @staticmethod
    def update_summary(user_prompt: str) -> None:
    
        summary.parts[summary.count-1:story.count+1] = story.parts[summary.count-1:story.count+1]
        summary.join_and_write()

        for part_number in range(summary.count-1, story.count):
            StoryGenerator.summarize_part(user_prompt, part_number-1)