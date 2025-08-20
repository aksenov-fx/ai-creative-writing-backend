# Streamer Module Specification

## Overview
Core streaming engine that manages the connection to AI APIs and handles real-time token delivery with support for reasoning models and interruption handling.

## Dependencies
- `_includes.config` - Configuration access for endpoint, model, and streaming settings

## Core Functions

`__init__(token_callback: Callable[[str], None]) -> None`
Initializes the Streamer with a token callback function and API configuration.

**Behavior:**
- Sets up the token callback for handling streamed tokens
- Configures API endpoint URL and key from config
- Prepares the streamer for API communication

**Example Usage:**
```python
def my_callback(token):
    print(token, end='')

streamer = Streamer(my_callback)
```

`stream_response(messages: List[Dict[str, str]]) -> None`
Streams AI responses from OpenAI-compatible APIs with real-time token delivery.

**Behavior:**
- Creates OpenAI client with configured endpoint and API key
- Sends chat completion request with streaming enabled
- Processes each token chunk and calls token_callback
- Handles reasoning content separately if enabled
- Supports interruption via config.interrupt_flag
- Manages keyboard interrupts and exceptions

**Example Usage:**
```python
messages = [{"role": "user", "content": "Hello"}]
streamer.stream_response(messages)
```

## Configuration Usage

### Primary Configuration Sources:
- `config.endpoint['url']`: API endpoint URL
- `config.endpoint['api_key']`: API authentication key
- `config.model`: AI model to use for generation
- `config.temperature`: Sampling temperature for responses
- `config.include_reasoning`: Enable reasoning content in responses
- `config.interrupt_flag`: Flag for interrupting streaming
- `config.print_reasoning`: Enable printing of reasoning content

## Usage Patterns

### Standard Streaming Flow:
- Initialize with token callback function
- Call stream_response() with formatted messages
- Tokens are delivered in real-time via callback
- Handles both regular content and reasoning content
- Supports graceful interruption and error handling

### Reasoning Model Support:
- Detects reasoning content in API responses
- Prints reasoning to stdout if enabled
- Separates reasoning from regular content delivery
- Configurable via config.print_reasoning flag

## Integration Points

- **TokenHandler**: Provides token callback functions for processing streamed content
- **Chat Module**: Uses streaming for real-time story generation and chat responses
- **ConfigManager**: Provides API configuration and streaming parameters
- **stream.py**: Orchestrates Streamer with TokenHandler for complete streaming workflow
