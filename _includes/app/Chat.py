from _includes import config
from .Composers.PromptComposer import compose_prompt, compose_helper_prompt
from .Streaming.Streamer import Streamer
from .Streaming.TokenHandler import TokenHandler
from .History.Factory import Factory
from .History.History import HistoryChanger

### Chat

class Chat:

    @staticmethod
    def stream(history_object: HistoryChanger,
               messages,
               rewrite: bool = False,
               write_history: bool = True,
               part_number: int = 0) -> None:

        print(f"\nModel: {config.model}")
        if config.debug: print("\nDebug mode is on"); return "debug response"

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

        Chat.stream(story, messages)

    @staticmethod
    def custom_prompt() -> None:

        story, story_parsed, summary = Factory.get_objects()
        story_parsed.merge_with_summary(summary)
        story_parsed.parse_assistant_response()

        messages = compose_prompt("Custom prompt", story_parsed)

        Chat.stream(story, messages)

    @staticmethod
    def regenerate(part_number: int) -> None:
        story, story_parsed, summary = Factory.get_objects()
        story_parsed.merge_with_summary(summary)
        story_parsed.cut_history_to_part_number(part_number-1)

        messages = compose_prompt("Write scene", story_parsed)

        Chat.stream(story, messages, rewrite=True, part_number=part_number)

    @staticmethod
    def add_part(part_number: int) -> None:
        story, story_parsed, summary = Factory.get_objects()

        story.add_part("", part_number)

        story_parsed.merge_with_summary(summary)
        story_parsed.cut_history_to_part_number(part_number)
        part_number += 1

        messages = compose_prompt("Write scene", story_parsed)
        Chat.stream(story, messages, rewrite=True, part_number=part_number)

    ### Changer

    @staticmethod
    def change_part(part_number: int) -> None:

        story = Factory.get_story()
        story_parsed = Factory.get_story_parsed()
        story_parsed.cut(part_number, include_previous_part=config.include_previous_part_when_rewriting)

        messages = compose_prompt("Change part", story_parsed, include_introduction=False)

        Chat.stream(story, messages, rewrite=True, part_number=part_number)

    @staticmethod
    def change_parts(part_number: int) -> None:

        story = Factory.get_story()
        print(f"Rewriting part {part_number}/{story.count-1}")

        for part in range(part_number, story.count):
            Chat.change_part(part)

    ### Helpers

    @staticmethod
    def rewrite_selection(selected_text: str):
        messages = compose_helper_prompt('Rewrite selection', selected_text)
        result = Chat.stream(None, messages, write_history=False)
        return result
    
    @staticmethod
    def translate(selected_text: str):
        messages = compose_helper_prompt('Translate', selected_text)
        result = Chat.stream(None, messages, write_history=False)
        return result

    @staticmethod
    def explain(selected_text: str):
        messages = compose_helper_prompt('Explain', selected_text)
        result = Chat.stream(None, messages, write_history=False)
        return result

    ### Summarizer

    @staticmethod
    def summarize_parts() -> None:

        summary = Factory.get_summary()
        hash_keys = list(summary.yaml_data.keys())

        for part_index, hash_key in enumerate(hash_keys):
            
            summary_parsed = Factory.get_summary_parsed()
            if summary.yaml_data[hash_key]['summarized']: continue
            
            print(f"Summarizing part {part_index+1}/{summary.count}")
            
            summary_parsed.cut(part_index+1, config.include_previous_part_when_summarizing)
            messages = compose_prompt("Summarize part", summary_parsed, include_introduction=False)
            
            config.model = config.models[config.summary_model]['name']
            result = Chat.stream(None, messages, write_history=False)

            summary.yaml_data[hash_key]['summarized'] = True
            summary.replace_history_part(result, hash_key)

    @staticmethod
    def update_summary() -> None:
        story = Factory.get_story()
        Factory.get_summary().update_from_story_parts(story)

        Chat.summarize_parts()

# Chat
    @staticmethod
    def chat(file_path: str) -> None:
        from .Composers.ApiComposer import ApiComposer

        history, history_parsed = Factory.get_chat_objects(file_path)
        
        history_parsed.process()
        messages = ApiComposer.compose_chat_messages(history_parsed)

        history.fix_separator()
        Chat.stream(history, messages)