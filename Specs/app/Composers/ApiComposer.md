# ApiComposer Module Specification

## Overview
Constructs message arrays in the format expected by OpenAI-compatible APIs, handling system prompts, user messages, and assistant responses.

---

## Dependencies
- `_includes.config` - For configuration access (system_prompt, print_messages)
- `..Utility` - For message printing utilities

## Core Functions

### Message Composition Functions

#### `append_message(messages: List[Dict[str, str]], role: str, content: Optional[str]) -> None`
Appends a message to the messages list if content is provided.

**Behavior:**
- Only appends non-empty content
- Strips whitespace from content before adding
- Modifies the messages list in-place

#### `compose_messages(user_prompt, assistant_response) -> List[Dict[str, str]]`
Composes standard API messages for story generation and chat interactions.

**Message Structure:**
1. System message with config.system_prompt
2. User message with provided user_prompt
3. Assistant message with provided assistant_response (if any)

**Debug Output:**
- If config.print_messages is True, prints formatted messages using Utility.print_with_newlines()

#### `compose_chat_messages(history) -> List[Dict[str, str]]`
Composes API messages for chat-style conversations with alternating roles.

**Message Structure:**
1. System message with history.custom_instructions
2. Alternating user/assistant messages from history.parts
   - Even indices (0, 2, 4...) are user messages
   - Odd indices (1, 3, 5...) are assistant messages

**Debug Output:**
- If config.print_messages is True, prints formatted messages using Utility.print_with_newlines()

## Configuration Usage

### Primary Configuration Sources:
- `config.system_prompt`: Default system prompt for story generation
- `config.print_messages`: Boolean flag to enable message debugging output

## Usage Patterns

### Standard Message Flow:
- Used by PromptComposer.compose_prompt() for story generation
- Creates 3-message structure: system → user → assistant
- Assistant response is optional (None for new generations)

### Chat Message Flow:
- Used for conversational interactions
- Creates dynamic message arrays based on conversation history
- Alternates roles based on message position in history
- Includes custom system instructions per conversation

### Message Format:
All returned messages follow the OpenAI API format:
```python
[
    {"role": "system", "content": "system prompt"},
    {"role": "user", "content": "user message"},
    {"role": "assistant", "content": "assistant response"}
]
```

## Integration Points

- **PromptComposer**: Uses compose_messages() for final message formatting
- **Chat Module**: Uses compose_chat_messages() for conversational interfaces
- **Streaming Module**: Receives composed messages for API transmission
- **History Module**: Provides history objects for chat message composition
