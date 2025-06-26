from .ApiComposer import ApiComposer
from .ChatHistory import ChatHistory
from .Streamer import Streamer
from .miscellaneous import expand_abbreviations

from ..chat_settings import config

def process_history():

    # Read history
    history_content = ChatHistory.read()

    # Exclude first paragraphs to match input length with max_tokens
    history_content = ApiComposer.trim_content(history_content, config.max_tokens)

    # Remove '### Reasoning' headers
    history_content = ChatHistory.remove_reasoning_header(history_content)

    # Parse assistant response to continue last response
    if history_content:
        history_content, assistant_response = ChatHistory.parse_assistant_response(history_content)
    else:
        assistant_response = None

    # Remove reasoning tokens
    if ChatHistory.has_separator():
        history_content = ChatHistory.remove_reasoning_tokens(history_content)

    # Remove separators and extra empyty lines
    history_content = ChatHistory.format_history(history_content)

    return history_content, assistant_response

def chat(endpoint: dict, model: str, first_prompt: str, user_prompt: str) -> None:
    
    history_content, assistant_response = process_history()

    # Remove thinking tokens from assistant_response
    if assistant_response and not model['outputs_thinking']:
        assistant_response = ChatHistory.remove_reasoning_tokens(assistant_response)

    user_prompt = expand_abbreviations(user_prompt)
    messages = ApiComposer.compose_messages(history_content, assistant_response, first_prompt, user_prompt)

    streamer = Streamer(endpoint['url'], endpoint['api_key'])    
    streamer.stream_response(messages, model['name'])