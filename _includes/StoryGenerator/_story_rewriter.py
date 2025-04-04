from .ApiComposer import ApiComposer
from .ChatHistory import ChatHistory
from .Streamer import Streamer

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

    if config.part_to_rewrite == 1:
        history_content = history_split[0]
    else:
        history_content = config.separator.join(history_split[:config.part_to_rewrite-1])
    
    part_to_rewrite_content = history_split[config.part_to_rewrite-1]

    # Remove separators and extra empyty lines
    history_content = ChatHistory.format_history(history_content)

    return history_content, part_to_rewrite_content

def compose_api_request(history_content, assistant_response, first_prompt, user_prompt):

    messages = ApiComposer.compose_messages(
        history_content, assistant_response, first_prompt, user_prompt
    )
    
    if config.print_messages:
        for message in messages: print(message)

    return messages

def rewrite_part(endpoint: dict, model: str, first_prompt: str, user_prompt: str) -> None:
    
    history_content, part_to_rewrite_content = process_history()
    user_prompt = user_prompt + part_to_rewrite_content

    messages = compose_api_request(history_content, None, first_prompt, user_prompt)

    streamer = Streamer(endpoint['url'], endpoint['api_key'])    
    complete_response = streamer.stream_response(messages, model['name'], True)
    complete_response = '\n\n' + complete_response + '\n\n'

    history_content = ChatHistory.read()
    history_split = history_content.split(config.separator)
    history_split[config.part_to_rewrite-1] = complete_response
    history_content = config.separator.join(history_split)

    ChatHistory.write_history(history_content)