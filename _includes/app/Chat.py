from _includes import config
from .ApiComposer import ApiComposer
from .PromptComposer import PromptComposer
from .Streamer import Streamer
from .Factory import Factory
from .History import HistoryChanger, HistoryParser
from .Utility import Utility

### Chat

class Chat:

    @staticmethod
    def _get_objects():
        return Factory.get_story(), Factory.get_story_parsed(), Factory.get_summary()

    @staticmethod
    def chat(history_object: HistoryChanger,
             messages,
             rewrite: bool = False,
             part_number: int = 0) -> None:

        if not config.debug: 
            streamer = Streamer(history_object, rewrite, part_number)
            streamer.stream_response(messages)

    @staticmethod
    def post_process(first_prompt, user_prompt, history_parsed: HistoryParser):
        if config.trim_history: history_parsed.trim_content()

        print(f"Model: {config.model}\n")

        user_prompt = first_prompt + history_parsed.parsed + "\n\n" + user_prompt + "\n" + history_parsed.part_number_content
        messages = ApiComposer.compose_messages(user_prompt, history_parsed.assistant_response)

        return messages
    
    ### Generator

    @staticmethod
    def write_scene() -> None:
        user_prompt = PromptComposer.compose_prompt("write_scene")
        story, story_parsed, summary = Chat._get_objects()
        
        story_parsed.merge_with_summary(summary)
        story_parsed.parse_assistant_response()

        messages = Chat.post_process(config.first_prompt, user_prompt, story_parsed)
        Chat.chat(story, messages)

    @staticmethod
    def custom_prompt() -> None:
        user_prompt = PromptComposer.compose_prompt("custom_prompt")
        story, story_parsed, summary = Chat._get_objects()
        
        story_parsed.merge_with_summary(summary)
        story_parsed.parse_assistant_response()

        messages = Chat.post_process(config.first_prompt, user_prompt, story_parsed)
        Chat.chat(story, messages)

    @staticmethod
    def regenerate(part_number: int) -> None:
        user_prompt = PromptComposer.compose_prompt("regenerate")
        story, story_parsed, summary = Chat._get_objects()
        
        story_parsed.merge_with_summary(summary)
        story_parsed.cut_history_to_part_number(part_number-1)

        messages = Chat.post_process(config.first_prompt, user_prompt, story_parsed)
        Chat.chat(story, messages, rewrite=True, part_number=part_number)

    @staticmethod
    def add_part(part_number: int) -> None:
        user_prompt = PromptComposer.compose_prompt("add_part")
        story, story_parsed, summary = Chat._get_objects()
        
        story.add_part("", part_number)

        story_parsed.merge_with_summary(summary)
        story_parsed.cut_history_to_part_number(part_number)
        part_number += 1

        messages = Chat.post_process(config.first_prompt, user_prompt, story_parsed)
        Chat.chat(story, messages, rewrite=True, part_number=part_number)

    ### Changer

    @staticmethod
    def change_part(part_number: int) -> None:
        user_prompt = PromptComposer.compose_prompt("change_part")

        story = Factory.get_story()
        story_parsed = Factory.get_story_parsed()
        
        story_parsed.cut(part_number)

        messages = Chat.post_process("", user_prompt, story_parsed)
        Chat.chat(story, messages, rewrite=True, part_number=part_number)

    @staticmethod
    def change_parts(part_number: int) -> None:

        story = Factory.get_story()
        print(f"Rewriting part {part_number}/{story.count-1}")

        for part in range(part_number, story.count):
            Chat.change_part(part)

    ### Summarizer

    @staticmethod
    def summarize_part(part_number: int) -> None:
        user_prompt = PromptComposer.compose_prompt("summarize_part")

        story = Factory.get_story()
        summary = Factory.get_summary()
        summary_parsed = Factory.get_summary_parsed()        

        part_number += 1
        print(f"Summarizing part {part_number}/{story.count-1}")

        summary_parsed.cut(part_number)

        messages = Chat.post_process("", user_prompt, summary_parsed)
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
        story = Factory.get_story() # Get story here, as it's used later

        summary_count = summary.count
        summary.parts[summary.count-1:story.count+1] = story.parts[summary.count-1:story.count+1]
        summary.join_and_write()

        for part_number in range(summary_count, story.count):
            Chat.summarize_part(part_number-1)