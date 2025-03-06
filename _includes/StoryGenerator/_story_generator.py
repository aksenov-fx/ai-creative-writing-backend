from _includes.StoryGenerator.ApiComposer import ApiComposer
from _includes.StoryGenerator.ChatHistory import ChatHistory
from _includes.StoryGenerator.Streamer import Streamer

from _includes.chat_settings import config

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

    if not assistant_response:
        assistant_response = config.assistant_response

    if assistant_response and not config.user_prompt:
        raise ValueError("Set user_prompt or remove assistant response")

    # Remove reasoning, separators and extra empyty lines
    history_content = ChatHistory.format_history(history_content)

    return history_content, assistant_response

# Compose/print api request
def compose_api_request(history_content, assistant_response):

    messages = ApiComposer.compose_messages(
        history_content, assistant_response
    )
    
    if config.print_messages:
        for message in messages: print(message)

    return messages

# Chat
def chat(endpoint: dict, model: str) -> None:
    
    history_content, assistant_response = process_history()
    if not model['outputs_thinking']:
        assistant_response = ChatHistory.format_history(assistant_response)

    messages = compose_api_request(history_content, assistant_response)

    streamer = Streamer(endpoint['url'], endpoint['api_key'])    
    streamer.stream_response(messages, model['name'])