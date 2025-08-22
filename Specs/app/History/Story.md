# Story Module Specification

## Overview
Core story data structure and persistence layer for managing complete story narratives with parsing, modification, and trimming capabilities.

## Dependencies
- `..Utility` - For file operations, hash calculations, and timestamp updates
- `.Mixins.ParserMixin` - For content parsing functionality
- `.Mixins.ChangerMixin` - For content modification operations
- `.Mixins.TrimMixin` - For content trimming operations
- `...config` - For configuration access (separator, use_summary)

## Core Functions

### StoryMixin Base Functions

#### `__init__(path: str) -> None`
Initializes story object with file path and loads content.

**Behavior:**
- Loads story content from file
- Splits content into parts using separator
- Initializes counters and state variables
- Sets up trimming parameters

**Example Usage:**
```python
story = StoryMixin("path/to/story.md")
```

#### `split_history() -> List[str]`
Splits story content into individual parts using configured separator.

**Behavior:**
- Splits content by separator
- Strips whitespace from each part
- Returns list of story parts

**Example Usage:**
```python
parts = story.split_history()
```

#### `join_parts(content: List[str]) -> str`
Joins story parts back into single content string.

**Behavior:**
- Joins parts with separator and newlines
- Returns formatted content string

**Example Usage:**
```python
content = story.join_parts(parts_list)
```

#### `return_part(part_number: int) -> str`
Returns specific story part by number.

**Behavior:**
- Returns stripped content of specified part
- Uses zero-based indexing

**Example Usage:**
```python
part = story.return_part(0)
```

#### `update_hashes() -> None`
Calculates and stores hash values for all story parts.

**Behavior:**
- Creates hash for each non-empty part
- Stores hash-to-content mapping
- Used for summary matching

**Example Usage:**
```python
story.update_hashes()
```

### StoryChanger Functions

#### `fix_separator() -> None`
Ensures story ends with proper separator formatting.

**Behavior:**
- Appends separator if last part is not empty
- Updates file timestamp

**Example Usage:**
```python
story_changer.fix_separator()
```

#### `remove_last_response() -> None`
Removes the last AI response from story.

**Behavior:**
- Sets interrupt flag
- Removes last part or empties it
- Writes changes to file

**Example Usage:**
```python
story_changer.remove_last_response()
```

#### `change_history_part(content: str, part_number: int, append: bool = False) -> None`
Changes specific story part with new content.

**Behavior:**
If not append:
    - Replaces part at specified position (1-based)
    - Strips whitespace from new content
    - Writes changes to file

If append:
    - Appends content to part text
    - Write changes to file

**Example Usage:**
```python
story_changer.change_history_part("New content", 1)
story_changer.change_history_part("Additional text", 1, append=True)
```

#### `add_part(new_part: str, part_number: int) -> None`
Inserts new part at specified position.

**Behavior:**
- Inserts stripped content at position
- Shifts existing parts
- Writes changes to file

**Example Usage:**
```python
story_changer.add_part("New part", 2)
```

### StoryParser Functions

#### `set_assistant_response() -> StoryParser`
Extracts and removes the last assistant response.

**Behavior:**
- Pops last part as assistant response
- Updates internal state

**Example Usage:**
```python
story_parsed.set_assistant_response()
```

#### `merge_with_summary(summary) -> StoryParser`
Replaces story parts with summarized versions when available.

**Behavior:**
- Matches parts by hash with summary data
- Preserves last part to maintain writing style
- Only processes if use_summary is enabled

**Example Usage:**
```python
parser = story_parser.merge_with_summary(summary_obj)
```

## Configuration Usage

### Primary Configuration Sources:
- `config.separator`: Story part separator string
- `config.use_summary`: Boolean flag to enable summary merging
- `config.summary_yaml_path`: Path to summary data file

## Usage Patterns

### Story Processing Flow:
- Load story content and split into parts
- Optionally merge with summary for context efficiency
- Parse assistant response for separate handling
- Apply trimming based on configuration
- Modify content through changer methods

### Hash-Based Summary Integration:
- Calculate hashes for story parts
- Match with summary data by hash
- Replace full content with summaries
- Preserve recent parts for style consistency

## Integration Points

- **Chat Module**: Uses StoryParser for content preparation
- **Summary Module**: Provides summary data for merging
- **ConfigManager**: Supplies separator and summary settings
- **Utility Module**: Handles file I/O and hash calculations
- **Factory Module**: Creates story instances with proper paths
