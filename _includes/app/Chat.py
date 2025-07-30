import shutil, os

from _includes import config, story, summary, story_parsed, summary_parsed
from .ApiComposer import ApiComposer
from .PromptComposer import PromptComposer
from .Utility import Utility
from .Streamer import Streamer
from .History import HistoryChanger, HistoryParser

### Chat

class Chat:

    @staticmethod
    def chat(history_object: HistoryChanger,
             messages,
             rewrite: bool = False,
             part_number: int = 0) -> None:

        if not config.debug: 
            streamer = Streamer(history_object, rewrite, part_number)
            streamer.stream_response(messages)

    ### Generator

    @staticmethod
    def pre_process(mode):
        config.interrupt_flag = False
        Utility.reset_history()
        return PromptComposer.compose_prompt(mode)

    @staticmethod
    def post_process(first_prompt, user_prompt, history_parsed):
        if config.trim_history: history_parsed.trim_content()

        user_prompt = first_prompt + history_parsed.parsed + "\n\n" + user_prompt + "\n" + history_parsed.part_number_content
        messages = ApiComposer.compose_messages(user_prompt, history_parsed.assistant_response)

        history_parsed.refresh()

        return messages

    @staticmethod
    def write_scene() -> None:

        user_prompt = Chat.pre_process("write_scene")

        story_parsed.merge_with_summary(summary)
        story_parsed.parse_assistant_response()

        messages = Chat.post_process(config.first_prompt, user_prompt, story_parsed)

        Chat.chat(story, messages)

    @staticmethod
    def custom_prompt() -> None:

        user_prompt = Chat.pre_process("custom_prompt")

        story_parsed.merge_with_summary(summary)
        story_parsed.parse_assistant_response()

        messages = Chat.post_process(config.first_prompt, user_prompt, story_parsed)

        Chat.chat(story, messages)

    @staticmethod
    def regenerate(part_number: int) -> None:

        user_prompt = Chat.pre_process("regenerate")

        story_parsed.merge_with_summary(summary)
        story_parsed.cut_history_to_part_number(part_number-1)

        messages = Chat.post_process(config.first_prompt, user_prompt, story_parsed)

        Chat.chat(story, messages, rewrite=True, part_number=part_number)

    @staticmethod
    def add_part(part_number: int) -> None:

        user_prompt = Chat.pre_process("add_part")

        story.add_part("", part_number)

        story_parsed.merge_with_summary(summary)
        story_parsed.cut_history_to_part_number(part_number)
        part_number += 1

        messages = Chat.post_process(config.first_prompt, user_prompt, story_parsed)

        Chat.chat(story, messages, rewrite=True, part_number=part_number)

    ### Changer

    @staticmethod
    def change_part(part_number: int) -> None:

        user_prompt = Chat.pre_process("change_part")
        story_parsed.cut(part_number)
        messages = Chat.post_process("", user_prompt, story_parsed)

        Chat.chat(story, messages, rewrite=True, part_number=part_number)

    @staticmethod
    def change_parts(part_number: int) -> None:

        print(f"Rewriting part {part_number}/{story.count-1}")

        for part in range(part_number, story.count):
            Chat.change_part(part)

    ### Summarizer

    @staticmethod
    def summarize_part(part_number: int) -> None:

        user_prompt = Chat.pre_process("summarize_part")

        part_number += 1
        print(f"Summarizing part {part_number}/{story.count-1}")

        summary_parsed.cut(part_number)

        messages = Chat.post_process("", user_prompt, summary_parsed)

        Chat.chat(summary, messages, rewrite=True, part_number=part_number)
        
    @staticmethod
    def summarize_all() -> None:

        if os.path.exists(summary.path):
            raise FileExistsError(f"Summary already exists. Please delete it before creating a new one.")
        shutil.copy(story.path, summary.path)

        summary.refresh()

        for part_number in range(summary.count-1):
            Chat.summarize_part(part_number)

    @staticmethod
    def update_summary() -> None:
    
        summary_count = summary.count
        summary.parts[summary.count-1:story.count+1] = story.parts[summary.count-1:story.count+1]
        summary.join_and_write()

        for part_number in range(summary_count, story.count):
            Chat.summarize_part(part_number-1)