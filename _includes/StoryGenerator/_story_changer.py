from .ApiComposer import ApiComposer
from .ChatHistory import ChatHistory
from .miscellaneous import expand_abbreviations
from .Streamer import Streamer

from ..chat_settings import config

def process_history():

    # Read history
    history_content = ChatHistory.read()

    # Exclude first paragraphs to match input length with max_tokens
    history_content = ApiComposer.trim_content(history_content, config.max_tokens)

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

    return history_content, part_number_content

def change_part(endpoint: dict, model: str, first_prompt: str, user_prompt: str, rewrite: bool) -> None:
    
    # Get history
    history_content, part_number_content = process_history()

    # Compose request
    if rewrite:
        user_prompt = user_prompt + part_number_content
    
    if config.part_number == 1:
        messages = ApiComposer.compose_messages(None, None, first_prompt, user_prompt)
    else:
        messages = ApiComposer.compose_messages(history_content, None, first_prompt, user_prompt)

    # Get changed part
    streamer = Streamer(endpoint['url'], endpoint['api_key'], True)    
    complete_response = streamer.stream_response(messages, model['name'])

    # Replace old part with changed part
    ChatHistory.replace_history_part(complete_response)

def add_part(endpoint: dict, model: str, first_prompt: str, user_prompt: str) -> None:
    
    # Get history
    history_content, _ = process_history()

    user_prompt = expand_abbreviations(user_prompt)
    messages = ApiComposer.compose_messages(history_content, None, first_prompt, user_prompt)

    # Get new part
    streamer = Streamer(endpoint['url'], endpoint['api_key'], True)    
    complete_response = streamer.stream_response(messages, model['name'])

    # Add new part
    ChatHistory.add_part(complete_response)