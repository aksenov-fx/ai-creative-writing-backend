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

    # Parse assistant response to continue last response
    if history_content:
        history_content, assistant_response = ChatHistory.parse_assistant_response(history_content)
    else:
        assistant_response = None

    # Remove reasoning, separators and extra empyty lines
    history_content = ChatHistory.format_history(history_content)

    return history_content, assistant_response

def compose_api_request(history_content, assistant_response, first_prompt, user_prompt):

    messages = ApiComposer.compose_messages(
        history_content, assistant_response, first_prompt, user_prompt
    )
    
    if config.print_messages:
        for message in messages: print(message)

    return messages

def chat(endpoint: dict, model: str, first_prompt: str, user_prompt: str) -> None:
    
    history_content, assistant_response = process_history()

    # Remove thinking tokens from assistant_response
    if assistant_response and not model['outputs_thinking']:
        assistant_response = ChatHistory.format_history(assistant_response)

    messages = compose_api_request(history_content, assistant_response, first_prompt, user_prompt)

    streamer = Streamer(endpoint['url'], endpoint['api_key'])    
    streamer.stream_response(messages, model['name'])