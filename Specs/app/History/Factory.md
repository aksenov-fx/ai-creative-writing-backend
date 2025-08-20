# Factory Module Specification

## Overview
Factory pattern implementation for creating and loading history instances with proper configuration and file paths.

## Dependencies
- `_includes.config` - For file paths access
- `.Story` - StoryChanger and StoryParser classes
- `.ChatHistory` - ChatHistoryChanger and ChatHistoryParser classes
- `.Summary` - SummaryChanger and SummaryParser classes
- `.Prompts` - PromptChanger class

## Core Functions

### Story Factory Methods

#### `get_story() -> StoryChanger`
Creates StoryChanger instance for story modification operations.

**Behavior:**
- Constructs path using config.folder_path and config.history_path
- Returns StoryChanger instance for content modification

**Example Usage:**
```python
story = Factory.get_story()
```

#### `get_story_parsed() -> StoryParser`
Creates StoryParser instance for story parsing operations.

**Behavior:**
- Constructs path using config.folder_path and config.history_path
- Returns StoryParser instance for content parsing

**Example Usage:**
```python
parser = Factory.get_story_parsed()
```

#### `get_objects() -> Tuple[StoryChanger, StoryParser, SummaryChanger]`
Creates complete set of story and summary objects.

**Behavior:**
- Returns tuple of story changer, parser, and summary changer
- Convenient method for getting all story-related objects

**Example Usage:**
```python
story, parser, summary = Factory.get_objects()
```

### Prompt Factory Methods

#### `get_prompts() -> PromptChanger`
Creates PromptChanger instance for prompt management.

**Behavior:**
- Constructs path using config.folder_path and config.prompts_path
- Returns PromptChanger instance for prompt operations

**Example Usage:**
```python
prompts = Factory.get_prompts()
```

### Summary Factory Methods

#### `get_summary() -> SummaryChanger`
Creates SummaryChanger instance for summary modification operations.

**Behavior:**
- Constructs path using config.folder_path and config.summary_yaml_path
- Returns SummaryChanger instance for summary management

**Example Usage:**
```python
summary = Factory.get_summary()
```

#### `get_summary_parsed() -> SummaryParser`
Creates SummaryParser instance for summary parsing operations.

**Behavior:**
- Constructs path using config.folder_path and config.summary_yaml_path
- Returns SummaryParser instance for summary parsing

**Example Usage:**
```python
parser = Factory.get_summary_parsed()
```

### Chat Factory Methods

#### `get_chat_history(file_path: str) -> ChatHistoryChanger`
Creates ChatHistoryChanger instance for chat modification operations.

**Behavior:**
- Uses provided file_path directly
- Returns ChatHistoryChanger instance for chat management

**Example Usage:**
```python
chat = Factory.get_chat_history("path/to/chat.md")
```

#### `get_chat_history_parsed(file_path: str) -> ChatHistoryParser`
Creates ChatHistoryParser instance for chat parsing operations.

**Behavior:**
- Uses provided file_path directly
- Returns ChatHistoryParser instance for chat parsing

**Example Usage:**
```python
parser = Factory.get_chat_history_parsed("path/to/chat.md")
```

#### `get_chat_objects(file_path: str) -> Tuple[ChatHistoryChanger, ChatHistoryParser]`
Creates complete set of chat history objects.

**Behavior:**
- Returns tuple of chat changer and parser
- Convenient method for getting both chat objects

**Example Usage:**
```python
chat, parser = Factory.get_chat_objects("path/to/chat.md")
```

## Configuration Usage

### Primary Configuration Sources:
- `config.folder_path`: Base folder for all history files
- `config.history_path`: Story file path relative to folder_path
- `config.prompts_path`: Prompts file path relative to folder_path
- `config.summary_yaml_path`: Summary YAML file path relative to folder_path

## Usage Patterns

### Centralized Object Creation:
- Single point for creating all history-related objects
- Consistent path construction using configuration
- Separation of changer and parser instances

### Path Management:
- Story, prompts, and summary use config-based paths
- Chat objects use explicit file paths for flexibility
- All paths properly constructed with os.path.join

### Object Grouping:
- get_objects() for story workflow
- get_chat_objects() for chat workflow
- Separate methods for individual components

## Integration Points

- **All History Modules**: Primary creation point for all history objects
- **ConfigManager**: Uses configuration for path construction
- **Chat Module**: Uses factory for chat object creation
- **Story Generation**: Uses factory for story object creation
- **Summary Management**: Uses factory for summary object creation
