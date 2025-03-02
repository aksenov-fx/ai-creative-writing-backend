from pathlib import Path
from dataclasses import dataclass

from _includes.ApiComposer import ApiComposer
from _includes.ChatHistory import ChatHistory
from _includes.Streamer import Streamer

@dataclass
class ChatConfig:
    system_prompt: str
    first_prompt: str
    user_preprompt: str 
    user_postprompt: str 
    user_prompt: str
    assistant_response: str
    temperature: float
    max_tokens: int
    history_path: Path
    print_messages: bool
    client_type: "str"
    include_reasoning: bool
    separator: str

def chat(config: ChatConfig, endpoint: dict, model: str) -> None:
    
    # Initialize
    api_composer = ApiComposer()
    history_object = ChatHistory(config)
    streamer = Streamer(endpoint['url'], endpoint['api_key'])

    # Get history
    history_content = history_object.read()

    # Parse assistant response to continue last response
    if history_content:
        history_content, assistant_response = history_object.parse_assistant_response()
    else:
        assistant_response = None

    if not assistant_response:
        assistant_response = config.assistant_response

    # Remove separators and extra empyty lines
    history_content = history_object.format_history(history_content)

    # Exclude first paragraphs to match input length with max_tokens
    history_content = api_composer.trim_content(history_content, config.max_tokens)
    
    # Compose api request
    messages = api_composer.compose_messages(
        config, history_content, assistant_response
    )
    
    # Print conversation history
    if config.print_messages:
        for message in messages: print(message)

    # Stream
    streamer.stream_response(messages, config, model)