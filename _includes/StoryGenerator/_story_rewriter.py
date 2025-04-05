from .ApiComposer import ApiComposer
from .ChatHistory import ChatHistory
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

    if config.part_to_rewrite == 1:
        history_content = history_split[0]
    else:
        history_content = config.separator.join(history_split[:config.part_to_rewrite-1])
    
    part_to_rewrite_content = history_split[config.part_to_rewrite-1]

    # Remove separators and extra empyty lines
    history_content = ChatHistory.format_history(history_content)

    return history_content, part_to_rewrite_content

def rewrite_part(endpoint: dict, model: str, first_prompt: str, user_prompt: str) -> None:
    
    # Compose request
    history_content, part_to_rewrite_content = process_history()
    user_prompt = user_prompt + part_to_rewrite_content
    messages = ApiComposer.compose_messages(history_content, None, first_prompt, user_prompt)

    # Get rewritten part
    streamer = Streamer(endpoint['url'], endpoint['api_key'])    
    complete_response = streamer.stream_response(messages, model['name'], True)

    # Replace old part with rewritten part
    ChatHistory.replace_history_part(complete_response)