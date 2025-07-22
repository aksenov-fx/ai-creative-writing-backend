import shutil, os

from .ApiComposer import ApiComposer
from .Utility import Utility
from .Streamer import Streamer
from _includes import config, history, summary

### Chat

class StoryGenerator:

    @staticmethod
    def chat(history_object: str,
            endpoint: dict, 
            model: str, 
            first_prompt: str, 
            user_prompt: str, 
            part_number_content: str = "", 
            rewrite: bool = False) -> None:

        history_content = "\n\n" + config.history_prefix + "\n" + history_object.content if history_object.content else ""

        first_prompt = Utility.expand_abbreviations(first_prompt)
        user_prompt = Utility.expand_abbreviations(user_prompt)
        user_prompt = first_prompt + history_content + "\n\n" + user_prompt + "\n" + part_number_content.strip()

        messages = ApiComposer.compose_messages(user_prompt, history_object.assistant_response)
        history_object.reset()

        if not config.debug: 
            streamer = Streamer(history_object, endpoint['url'], endpoint['api_key'], rewrite)
            streamer.stream_response(messages, model['name'])

    ### Generator

    @staticmethod
    def generate(endpoint: dict, model: str, first_prompt: str, user_prompt: str) -> None:
        
        history.process_history(summary_object=summary)

        # Remove thinking tokens from assistant_response
        if history.assistant_response and not model['outputs_thinking']:
            history.remove_reasoning_tokens_from_assistance_reponse()

        StoryGenerator.chat(history, endpoint, model, first_prompt, user_prompt)

    ### Changer

    @staticmethod
    def change_part(endpoint: dict, model: str, first_prompt: str, user_prompt: str) -> None:
        
        history.insert_separator()

        if config.include_previous_part_when_rewriting: 
            history.process_history(no_summary=True, cut_history_to_part_number=True, return_last_part=True)
        else:
            history.clear_history()

        StoryGenerator.chat(history, endpoint, model, "", user_prompt, part_number_content=history.part_number_content, rewrite=True)

    @staticmethod
    def change_parts(endpoint: dict, model: str, first_prompt: str, user_prompt: str) -> None:
        
        history.insert_separator()
        number_of_parts = history.count_parts()
        print(number_of_parts)
        print(config.part_number)

        for part_number in range(config.part_number, number_of_parts+1):
            config.part_number = part_number
            StoryGenerator.change_part(endpoint, model, "", user_prompt)

    @staticmethod
    def regenerate(endpoint: dict, model: str, first_prompt: str, user_prompt: str) -> None:
        history.process_history(cut_history_to_part_number=True)
        StoryGenerator.chat(history, endpoint, model, first_prompt, user_prompt, rewrite=True)

    @staticmethod
    def add_part(endpoint: dict, model: str, first_prompt: str, user_prompt: str) -> None:

        history.add_part("")
        config.part_number += 1

        history.process_history(cut_history_to_part_number=True)

        StoryGenerator.chat(history, endpoint, model, first_prompt, user_prompt, rewrite=True)

    ### Summarizer

    @staticmethod
    def summarize_part(endpoint: dict, model: str, user_prompt: str, part_number: int) -> None:

        config.part_number = part_number + 1
        print(config.part_number)

        if config.include_previous_part_when_summarizing: 
            summary.process_history(no_summary=True, cut_history_to_part_number=True, return_last_part=True)
        else:
            summary.clear_history()

        StoryGenerator.chat(summary, endpoint, model, "", user_prompt, part_number_content=summary.part_number_content, rewrite=True)
        
    @staticmethod
    def summarize_all(endpoint: dict, model: str, user_prompt: str) -> None:

        if os.path.exists(summary.path):
            raise FileExistsError(f"Summary already exists. Please delete it before creating a new one.")
        shutil.copy(history.path, summary.path)

        summary.reset()
        summary.insert_separator()
        number_of_parts = summary.count_parts()

        for part_number in range(number_of_parts):
            StoryGenerator.summarize_part(endpoint, model, user_prompt, part_number)

    @staticmethod
    def update_summary(endpoint: dict, model: str, user_prompt: str) -> None:

        summary.insert_separator()
        history_split = history.split_history()
        number_of_story_parts = history.count_parts()

        number_of_summary_parts = summary.count_parts()
        missing_parts = history_split[number_of_summary_parts:-1]
        
        for part in missing_parts:
            summary.append_history(part.strip())
            summary.insert_separator()
        
        for part_number in range(number_of_summary_parts, number_of_story_parts):
            StoryGenerator.summarize_part(endpoint, model, user_prompt, part_number)