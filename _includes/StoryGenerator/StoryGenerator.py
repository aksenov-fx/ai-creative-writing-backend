import shutil, os

from .ApiComposer import ApiComposer
from .ChatHistory import ChatHistory
from .Streamer import Streamer
from _includes import config

### Chat

class StoryGenerator:

    @staticmethod
    def chat(endpoint: dict, 
            model: str, 
            first_prompt: str, 
            history_content: str, 
            user_prompt: str, 
            assistant_response: str = None, 
            part_number_content: str = "", 
            rewrite: bool = False) -> None:

        summary_prefix = "\n\nHere are the events so far:\n"
        history_content = summary_prefix + history_content if history_content else ""

        first_prompt = ChatHistory.expand_abbreviations(first_prompt)
        user_prompt = ChatHistory.expand_abbreviations(user_prompt)
        user_prompt = first_prompt + history_content + "\n\n" + user_prompt + "\n" + part_number_content.strip()

        messages = ApiComposer.compose_messages(user_prompt, assistant_response)

        streamer = Streamer(endpoint['url'], endpoint['api_key'], rewrite)

        if not config.debug:
            streamer.stream_response(messages, model['name'])

    ### Generator

    @staticmethod
    def generate(endpoint: dict, model: str, first_prompt: str, user_prompt: str) -> None:
        
        history_content, _, assistant_response = ChatHistory.process_history()

        # Remove thinking tokens from assistant_response
        if assistant_response and not model['outputs_thinking']:
            assistant_response = ChatHistory.remove_reasoning_tokens(assistant_response)

        StoryGenerator.chat(endpoint, model, first_prompt, history_content, user_prompt, assistant_response)

    ### Changer

    @staticmethod
    def rewrite(endpoint: dict, model: str, first_prompt: str, user_prompt: str) -> None:
        history_content, part_number_content, _ = ChatHistory.process_history(rewrite=True)
        StoryGenerator.chat(endpoint, model, first_prompt, history_content, user_prompt, part_number_content=part_number_content, rewrite=True)

    @staticmethod
    def regenerate(endpoint: dict, model: str, first_prompt: str, user_prompt: str) -> None:
        history_content, _, _ = ChatHistory.process_history(rewrite=True)
        StoryGenerator.chat(endpoint, model, first_prompt, history_content, user_prompt, rewrite=True)

    @staticmethod
    def add_part(endpoint: dict, model: str, first_prompt: str, user_prompt: str) -> None:

        history_content, _, _ = ChatHistory.process_history(rewrite=True)

        ChatHistory.add_part("")
        config.part_number += 1

        StoryGenerator.chat(endpoint, model, first_prompt, history_content, user_prompt, rewrite=True)

    ### Summarizer

    @staticmethod
    def summarize_part(endpoint: dict, model: str, user_prompt: str, part_number: int) -> None:

        config.part_number = part_number + 1
        print(config.part_number)

        history_content, part_number_content, _ = ChatHistory.process_history(rewrite=True)
        ChatHistory.switch_to_summary()
        StoryGenerator.chat(endpoint, model, "", history_content, user_prompt, part_number_content=part_number_content, rewrite=True)
        
    @staticmethod
    def summarize_all(endpoint: dict, model: str, user_prompt: str) -> None:

        dest_path = config.history_path.replace('.md', '_summary.md')
        if os.path.exists(dest_path):
            raise FileExistsError(f"Summary already exists. Please delete it before creating a new one.")

        shutil.copy(config.history_path, dest_path)
        ChatHistory.switch_to_summary()

        ChatHistory.insert_separator()
        number_of_parts = ChatHistory.count_parts()

        for part_number in range(number_of_parts):
            StoryGenerator.summarize_part(endpoint, model, user_prompt, part_number)

        ChatHistory.switch_to_story()

    @staticmethod
    def update_summary(endpoint: dict, model: str, user_prompt: str) -> None:

        ChatHistory.insert_separator()
        history_content = ChatHistory.read()
        history_split = history_content.split(config.separator)
        number_of_story_parts = ChatHistory.count_parts()

        ChatHistory.switch_to_summary()
        number_of_summary_parts = ChatHistory.count_parts()
        missing_parts = history_split[number_of_summary_parts:-1]

        for part in missing_parts:
            ChatHistory.append_history(part.strip())
            ChatHistory.insert_separator()
        
        for part_number in range(number_of_summary_parts, number_of_story_parts):
            StoryGenerator.summarize_part(endpoint, model, user_prompt, part_number)

        ChatHistory.switch_to_story()