from .ApiComposer import ApiComposer
from .ChatHistory import ChatHistory
from .Streamer import Streamer
from .miscellaneous import expand_abbreviations

from ..chat_settings import config

def process_history():

    # Read history
    if config.use_summary:
        history_content = ChatHistory.merge_story_with_summary()
    else:
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

def change_part(endpoint: dict, model: str, first_prompt: str, user_prompt: str, rewrite: bool) -> None:
    
    history_content, part_number_content = process_history()
    history_content = "\nHere's the story so far:\n\n" + history_content
    user_prompt = expand_abbreviations(user_prompt)

    if rewrite:
        user_prompt = user_prompt + part_number_content
    
    user_prompt = first_prompt + history_content + user_prompt
    messages = ApiComposer.compose_messages(user_prompt, None, None, None)

    streamer = Streamer(endpoint['url'], endpoint['api_key'], True)    
    streamer.stream_response(messages, model['name'])

def add_part(endpoint: dict, model: str, first_prompt: str, user_prompt: str) -> None:
    
    ChatHistory.add_part("")
    config.part_number += 1

    history_content, _ = process_history()
    history_content = "\nHere's the story so far:\n\n" + history_content
    user_prompt = expand_abbreviations(user_prompt)

    user_prompt = first_prompt + history_content + user_prompt
    messages = ApiComposer.compose_messages(user_prompt, None, None, None)

    streamer = Streamer(endpoint['url'], endpoint['api_key'], True)    
    streamer.stream_response(messages, model['name'])