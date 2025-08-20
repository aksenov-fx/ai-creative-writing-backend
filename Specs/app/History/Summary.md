# Summary Module Specification

## Overview
Handles story and chat summarization for efficient context management with YAML-based storage and hash-based part matching.

## Dependencies
- `..Utility` - For YAML operations, file I/O, and hash calculations
- `.Mixins.ParserMixin` - For content parsing functionality
- `.Mixins.TrimMixin` - For content trimming operations
- `...config` - For configuration access (separator, folder_path, summary paths)

## Core Functions

### SummaryMixin Base Functions

#### `__init__(path: str) -> None`
Initializes summary object with YAML file path and loads data.

**Behavior:**
- Loads YAML summary data from file
- Initializes empty collections for keys, parts, parsed content
- Sets up trimming parameters
- Calls update_from_yaml() to populate data

**Example Usage:**
```python
summary = SummaryMixin("path/to/summary.yaml")
```

#### `join_parts(content: List[str]) -> str`
Joins summary parts into single content string.

**Behavior:**
- Joins parts with separator and newlines
- Returns formatted content string

**Example Usage:**
```python
content = summary.join_parts(parts_list)
```

#### `_extract_parts_from_yaml() -> List[str]`
Extracts part text from YAML data structure.

**Behavior:**
- Iterates through YAML values
- Extracts 'part_text' field from each entry
- Strips whitespace and returns list

**Example Usage:**
```python
parts = summary._extract_parts_from_yaml()
```

#### `update_from_yaml() -> None`
Updates internal state from loaded YAML data.

**Behavior:**
- Extracts keys from YAML data
- Updates parts list from YAML
- Regenerates parsed content and count

**Example Usage:**
```python
summary.update_from_yaml()
```

### SummaryChanger Functions

#### `write_summary() -> None`
Writes summary data to both YAML and markdown files.

**Behavior:**
- Writes YAML data to configured path
- Creates human-readable markdown version
- Uses configured folder and file paths

**Example Usage:**
```python
summary_changer.write_summary()
```

#### `update_from_story_parts(story) -> SummaryChanger`
Updates summary from story parts using hash matching.

**Behavior:**
- Creates new OrderedDict for updated data
- Preserves existing summaries with matching hashes
- Adds new parts with summarized=False flag
- Removes summaries without matching story parts
- Writes updated summary to files

**Example Usage:**
```python
changer = summary_changer.update_from_story_parts(story_obj)
```

#### `replace_history_part(new_part: str, hash_key: str) -> None`
Replaces specific summary part by hash key.

**Behavior:**
- Updates part_text for specified hash
- Strips whitespace from new content
- Updates internal state and writes to files

**Example Usage:**
```python
summary_changer.replace_history_part("New summary", "hash123")
```

## Configuration Usage

### Primary Configuration Sources:
- `config.separator`: Summary part separator string
- `config.folder_path`: Base folder for summary files
- `config.summary_yaml_path`: YAML summary file path
- `config.summary_md_path`: Markdown summary file path

## Usage Patterns

### Summary Creation Flow:
- Load existing YAML summary data
- Match story parts by calculated hash
- Preserve existing summaries for unchanged parts
- Add new parts with summarized=False flag
- Write both YAML and markdown versions

### Hash-Based Matching:
- Story parts generate unique hashes
- Summary entries keyed by these hashes
- Unchanged parts retain their summaries
- Changed parts reset to original text
- Orphaned summaries are removed

### Summarization State:
- Each entry has 'summarized' boolean flag
- False indicates original text (needs summarization)
- True indicates already summarized content
- Actual summarization handled by Summarizer module

## Integration Points

- **Story Module**: Provides story parts and hashes for updating
- **Summarizer Module**: Performs actual text summarization
- **ConfigManager**: Supplies file paths and separator settings
- **Utility Module**: Handles YAML/file operations and hash calculations
- **Factory Module**: Creates summary instances with proper paths
