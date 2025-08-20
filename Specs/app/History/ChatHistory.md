# ChatHistory Module Specification

## Overview
Manages conversational history and context retention for ongoing chat interactions with alternating user/assistant message structure.

## Dependencies
- `..Utility` - For file operations and instruction parsing
- `.Mixins.ChangerMixin` - For content modification operations
- `.Mixins.TrimMixin` - For content trimming operations
- `...config` - For configuration access (model, separator, splitter, add_header)

## Core Functions

### ChatHistoryMixin Base Functions

#### `__init__(path: str) -> None`
Initializes chat history object with file path and parses structure.

**Behavior:**
- Loads chat content from file
- Extracts custom instructions from markdown code block
- Splits content into parts, excluding first two parts
- Sets up alternating message structure tracking

**Example Usage:**
```python
chat = ChatHistoryMixin("path/to/chat.md")
```

#### `update(parts: List[str]) -> None`
Updates internal state with new parts list.

**Behavior:**
- Updates parts and even/odd tracking
- Reconstructs all_parts with header
- Recalculates count and content

**Example Usage:**
```python
chat.update(new_parts)
```

#### `split_parts(content: str = None) -> List[str]`
Splits content into individual parts using configured separator.

**Behavior:**
- Uses current content if none provided
- Splits by separator and strips whitespace
- Returns list of chat parts

**Example Usage:**
```python
parts = chat.split_parts()
```

#### `join_parts(content: List[str]) -> str`
Joins chat parts back into single content string.

**Behavior:**
- Joins parts with separator and newlines
- Returns formatted content string

**Example Usage:**
```python
content = chat.join_parts(parts_list)
```

### ChatHistoryChanger Functions

#### `fix_separator() -> ChatHistoryChanger`
Ensures chat ends with proper separator and optional header.

**Behavior:**
- Returns early if last part is empty or header
- Appends empty part and separator
- Adds "# " header if configured and on user turn
- Updates timestamp

**Example Usage:**
```python
changer = chat_changer.fix_separator()
```

#### `remove_last_response() -> ChatHistoryChanger`
Removes the last response(s) from chat history.

**Behavior:**
- Sets interrupt flag
- Removes one part if even count, two if odd
- Writes changes to file

**Example Usage:**
```python
changer = chat_changer.remove_last_response()
```

### ChatHistoryParser Functions

#### `split_conversation() -> None`
Splits conversation at configured splitter point.

**Behavior:**
- Returns early if splitter not found
- Takes content after last splitter occurrence
- Updates parts with split content

**Example Usage:**
```python
chat_parser.split_conversation()
```

#### `clean_header() -> None`
Removes "# " prefix from user messages.

**Behavior:**
- Processes even-indexed parts (user messages)
- Removes "# " prefix if present
- Updates internal state

**Example Usage:**
```python
chat_parser.clean_header()
```

#### `include_file() -> None`
Includes external file content in first user message.

**Behavior:**
- Returns early if no include_file configured
- Raises FileNotFoundError if file empty/missing
- Appends file content to first user message

**Example Usage:**
```python
chat_parser.include_file()
```

#### `parse_instructions() -> str`
Parses custom instructions from chat file.

**Behavior:**
- Uses Utility.read_instructions for parsing
- Returns processed instruction text

**Example Usage:**
```python
instructions = chat_parser.parse_instructions()
```

#### `process() -> None`
Executes full chat processing pipeline.

**Behavior:**
- Splits conversation at splitter
- Cleans headers from user messages
- Trims content if configured
- Includes external file content
- Parses custom instructions

**Example Usage:**
```python
chat_parser.process()
```

## Configuration Usage

### Primary Configuration Sources:
- `config.model`: AI model identifier
- `config.separator`: Message separator string
- `config.splitter`: Conversation split marker
- `config.add_header`: Boolean flag for "# " prefix
- `config.trim_history`: Boolean flag for content trimming
- `config.include_file`: Path to file for inclusion

## Usage Patterns

### Chat Processing Flow:
- Load chat file and extract custom instructions
- Split into alternating user/assistant messages
- Process conversation splits and headers
- Include external content if configured
- Apply trimming based on settings

### Message Structure:
- Even indices (0, 2, 4...) are user messages
- Odd indices (1, 3, 5...) are assistant messages
- First two parts contain metadata/instructions
- Remaining parts form the conversation

### Header Management:
- "# " prefix added to user messages if enabled
- Cleaned during parsing for API compatibility
- Helps visual identification in markdown

## Integration Points

- **Composers Module**: Uses parsed chat for API message composition
- **Chat Module**: Processes chat interactions through parser
- **ConfigManager**: Supplies chat-specific configuration
- **Utility Module**: Handles file I/O and instruction parsing
- **Factory Module**: Creates chat instances with proper paths
