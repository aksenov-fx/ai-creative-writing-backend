from _includes import config
from .PromptComposer import *
from .Streamer import Streamer
from .TokenHandler import TokenHandler
from .Factory import Factory
from .History import HistoryChanger
from .Utility import Utility

### Chat

class Chat:

    @staticmethod
    def chat(history_object: HistoryChanger,
             messages,
             rewrite: bool = False,
             write_history: bool = True,
             part_number: int = 0) -> None:

        print(f"\nModel: {config.model}")

        if config.debug: print("\nDebug mode is on"); return

        token_handler = TokenHandler(history_object, rewrite, write_history, part_number)
        streamer = Streamer(token_handler.get_token_callback())

        streamer.stream_response(messages)
        result = token_handler.finalize()
        return result
    
    ### Generator

    @staticmethod
    def write_scene() -> None:

        story, story_parsed, summary = Factory.get_objects()
        story_parsed.merge_with_summary(summary)
        story_parsed.parse_assistant_response()

        messages = compose_prompt("Write scene", story_parsed)

        Chat.chat(story, messages)

    @staticmethod
    def custom_prompt() -> None:

        story, story_parsed, summary = Factory.get_objects()
        story_parsed.merge_with_summary(summary)
        story_parsed.parse_assistant_response()

        messages = compose_prompt("Custom prompt", story_parsed)

        Chat.chat(story, messages)

    @staticmethod
    def regenerate(part_number: int) -> None:
        story, story_parsed, summary = Factory.get_objects()
        story_parsed.merge_with_summary(summary)
        story_parsed.cut_history_to_part_number(part_number-1)

        messages = compose_prompt("Write scene", story_parsed)

        Chat.chat(story, messages, rewrite=True, part_number=part_number)

    @staticmethod
    def add_part(part_number: int) -> None:
        story, story_parsed, summary = Factory.get_objects()

        story.add_part("", part_number)

        story_parsed.merge_with_summary(summary)
        story_parsed.cut_history_to_part_number(part_number)
        part_number += 1

        messages = compose_prompt("Write scene", story_parsed)
        Chat.chat(story, messages, rewrite=True, part_number=part_number)

    ### Changer

    @staticmethod
    def change_part(part_number: int) -> None:

        story = Factory.get_story()
        story_parsed = Factory.get_story_parsed()
        story_parsed.cut(part_number)

        messages = compose_prompt("Change part", story_parsed, include_introduction=False)

        Chat.chat(story, messages, rewrite=True, part_number=part_number)

    @staticmethod
    def change_parts(part_number: int) -> None:

        story = Factory.get_story()
        print(f"Rewriting part {part_number}/{story.count-1}")

        for part in range(part_number, story.count):
            Chat.change_part(part)

    @staticmethod
    def rewrite_selection(selected_text: str):
        messages = compose_prompt_to_rewrite_selection(selected_text)
        result = Chat.chat(None, messages, write_history=False)
        return result
    
    ### Other
    @staticmethod
    def translate(selected_text: str):
        messages = compose_prompt_to_translate(selected_text)
        result = Chat.chat(None, messages, write_history=False)
        return result

    ### Summarizer

    @staticmethod
    def summarize_part(part_number: int) -> None:

        story = Factory.get_story()
        summary = Factory.get_summary()
        summary_parsed = Factory.get_summary_parsed()        

        part_number += 1
        print(f"Summarizing part {part_number}/{story.count-1}")

        summary_parsed.cut(part_number)

        config.model = config.models[config.summary_model]['name']
        messages = compose_prompt("Summarize part", summary_parsed, include_introduction=False)

        Chat.chat(summary, messages, rewrite=True, part_number=part_number)
        
    @staticmethod
    def summarize_all() -> None:

        story_path = config.folder_path + config.history_path
        summary_path = config.folder_path + config.summary_path
        Utility.copy_file(story_path, summary_path)

        summary = Factory.get_summary()

        for part_number in range(summary.count-1):
            Chat.summarize_part(part_number)

    @staticmethod
    def update_summary() -> None:
        summary = Factory.get_summary()
        story = Factory.get_story()

        summary_count = summary.count
        summary.parts[summary.count-1:story.count+1] = story.parts[summary.count-1:story.count+1]
        summary.join_and_write()

        for part_number in range(summary_count, story.count):
            Chat.summarize_part(part_number-1)
