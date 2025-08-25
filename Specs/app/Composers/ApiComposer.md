# ApiComposer Module Specification

## Overview
Constructs message arrays in the format expected by OpenAI-compatible APIs, handling system prompts and alternating user/assistant messages.

---

## Dependencies
- `_includes.config` - For configuration access (print_messages)
- `..Utility` - For message printing utilities

## Core Functions

### Message Composition Functions

#### `append_message(messages: List, role: str, content: str) -> None`
Appends a message to the messages list if content is provided.

**Behavior:**
- Only appends non-empty content
- Strips whitespace from content before adding
- Modifies the messages list in-place

**Example Usage:**
```python
append_message(messages, "user", "Hello")
```

#### `compose_messages(system_prompt, parts) -> List`
Composes API messages with a system prompt and alternating user/assistant conversation parts.

**Parameters:**
- `system_prompt`: The system message content
- `parts`: List of conversation parts that alternate between user and assistant messages

**Message Structure:**
1. System message with provided system_prompt
2. Alternating user/assistant messages from parts array
   - Even indices (0, 2, 4...) are user messages
   - Odd indices (1, 3, 5...) are assistant messages

**Debug Output:**
- If config.print_messages is True, prints formatted messages using Utility.print_with_newlines()

**Example Usage:**
```python
messages = compose_messages("You are a helpful assistant", ["Hello", "Hi there", "How are you?"])
```

## Configuration Usage

### Primary Configuration Sources:
- `config.print_messages`: Boolean flag to enable message debugging output

## Usage Patterns

### Message Flow:
- Used for composing API messages with alternating user/assistant conversation parts
- Creates dynamic message arrays based on provided parts
- Alternates roles based on message position in parts array
- Includes system prompt as first message

### Message Format:
All returned messages follow the OpenAI API format:
```python
[
    {"role": "system", "content": "system prompt"},
    {"role": "user", "content": "user message"},
    {"role": "assistant", "content": "assistant response"},
    {"role": "user", "content": "next user message"}
]
```

## Integration Points

- **PromptComposer**: Uses compose_messages() for final message formatting
- **Chat Module**: Uses compose_messages() for conversational interfaces
- **Streaming Module**: Receives composed messages for API transmission