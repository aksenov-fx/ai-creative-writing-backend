from _includes.StreamerMethods.stream_response_with_openrouter_api import stream_response_with_openrouter_api
from _includes.StreamerMethods.stream_response_with_openai_client import stream_response_with_openai_client

class Streamer:

    def __init__(self, endpoint: str,
                 api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key
    
    def write_file(self, filepath, content, mode='a'):
        with open(filepath, mode, encoding='utf-8') as f:
            f.write(content)

    def stream_response(self, messages, config, model):
        if config.client_type == "openai":
            stream_response_with_openai_client(self, messages, config, model)
        elif config.client_type == "http":
            stream_response_with_openrouter_api(self, messages, config, model)