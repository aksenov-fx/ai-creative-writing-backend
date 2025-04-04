from ..StoryGenerator.StreamerMethods.stream_response_with_openrouter_api import stream_response_with_openrouter_api
from ..StoryGenerator.StreamerMethods.stream_response_with_openai_client import stream_response_with_openai_client
from ..chat_settings import config

class Streamer:

    def __init__(self, endpoint: str,
                 api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key
    
    def write_file(self, filepath, content, rewriting=False):
        if rewriting:
            return

        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(content)

    def stream_response(self, messages, model, rewriting=False):
        if config.client_type == "openai":
            return stream_response_with_openai_client(self, messages, config, model, rewriting)
        elif config.client_type == "http":
            return stream_response_with_openrouter_api(self, messages, config, model)