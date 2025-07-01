import shutil, os

from .ApiComposer import ApiComposer
from .ChatHistory import ChatHistory
from .Streamer import Streamer
from .miscellaneous import expand_abbreviations

from ..chat_settings import config

def process_history():

    # Read history
    history_content = ChatHistory.read()

    # Remove '### Reasoning' headers
    history_content = ChatHistory.remove_reasoning_header(history_content)

    # Remove reasoning tokens
    history_content = ChatHistory.remove_reasoning_tokens(history_content)

    # Cut history
    history_split = history_content.split(config.separator)

    if config.part_number == 1:
        history_content = history_split[0]
    else:
        history_content = config.separator.join(history_split[:config.part_number-1])

    part_number_content = history_split[config.part_number-1]

    # Remove separators and extra empyty lines
    history_content = ChatHistory.format_history(history_content)

    # Exclude first paragraphs to match input length with max_tokens
    history_content = ApiComposer.trim_content(history_content, config.max_tokens)

    return history_content, part_number_content

def summarize_part(endpoint: dict, model: str, user_prompt: str, part_number: int) -> None:

    config.part_number = part_number + 1
    print(config.part_number)

    history_content, part_number_content = process_history()

    first_prompt = "Here's the story summary so far:"
    
    if config.part_number == 1:
        messages = ApiComposer.compose_messages(None, None, user_prompt + part_number_content, None)
    else:
        messages = ApiComposer.compose_messages(None, None, first_prompt + history_content + user_prompt + part_number_content, None)

    streamer = Streamer(endpoint['url'], endpoint['api_key'], True)    
    streamer.stream_response(messages, model['name'])
    
def summarize_all(endpoint: dict, model: str, user_prompt: str) -> None:

    dest_path = config.history_path.replace('.md', '_summary.md')
    if os.path.exists(dest_path):
        raise FileExistsError(f"Summary already exists. Please delete it before creating a new one.")

    shutil.copy(config.history_path, dest_path)
    ChatHistory.switch_to_summary()

    ChatHistory.insert_separator()
    number_of_parts = ChatHistory.count_parts()

    for part_number in range(number_of_parts):
        summarize_part(endpoint, model, user_prompt, part_number)

    ChatHistory.switch_to_story()

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
        summarize_part(endpoint, model, user_prompt, part_number)

    ChatHistory.switch_to_story()