# writers Module Specification

## Overview
File writing utilities for saving stories, logs, and configuration updates with retry mechanisms and timestamp management.

## Dependencies
None.
## Core Functions

`update_timestamp(path: str, config) -> None`
Updates the modification timestamp of a file after a configured delay.

**Behavior:**
- Waits for config.TIMESTAMP_UPDATE_DELAY before updating
- Sets both access and modification times to current time
- Used to ensure proper file ordering and change detection

**Example Usage:**
```python
update_timestamp("story.txt", config)
```

`write_file(path: str, content: str, config) -> None`
Writes text content to a file with automatic directory creation and retry logic.

**Behavior:**
- Creates parent directories if they don't exist
- Implements exponential backoff retry mechanism (3 attempts)
- Uses UTF-8 encoding for all text files
- Updates file timestamp after successful write
- Raises exception if all retries fail

**Example Usage:**
```python
write_file("stories/chapter1.txt", story_content, config)
```

`write_yaml(path: str, content: dict, config) -> None`
Writes dictionary content to a YAML file with proper formatting.

**Behavior:**
- Converts OrderedDict to regular dict to avoid Python-specific YAML tags
- Uses human-readable YAML formatting (no flow style)
- Preserves Unicode characters and key ordering
- Delegates to write_file() for actual file operations

**Example Usage:**
```python
write_yaml("config.yaml", settings_dict, config)
```

## Configuration Usage

### Required Configuration Parameters:
- `config.TIMESTAMP_UPDATE_DELAY`: Delay before timestamp updates
- `config.RETRY_BASE_DELAY`: Base delay for exponential backoff retries

## Usage Patterns

### Story Persistence:
- Used by History module for saving story content and metadata
- Automatic directory structure creation for organized storage
- Reliable writing with error recovery

### Configuration Management:
- YAML serialization for settings and configuration updates
- Maintains readable format for manual editing
- Preserves data structure integrity

### Error Handling:
- Exponential backoff for transient file system errors
- Graceful failure with exception propagation after retries

## Integration Points

- **History Module**: Uses write_file() and write_yaml() for story persistence
- **ConfigManager**: Uses write_yaml() for configuration updates
- **Chat Module**: Uses write_file() for saving conversation logs
- **Streaming Module**: Uses write_file() for response caching
