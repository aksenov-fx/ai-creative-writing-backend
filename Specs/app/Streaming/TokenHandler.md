# TokenHandler Module Specification

## Overview
Processes individual tokens and manages streaming state, buffering, and output formatting with support for both appending and rewriting operations.

## Dependencies
- `_includes.config` - Configuration access for write interval settings

## Core Functions

`__init__(history_object, rewriting: bool = False, write_history: bool = True, part_number: int = 0) -> None`
Initializes the TokenHandler with history management and buffering configuration.

**Behavior:**
- Sets up history object reference for content persistence
- Configures rewriting mode and write settings
- Initializes token buffer and response tracking
- Sets up thread lock for buffer synchronization

**Example Usage:**
```python
handler = TokenHandler(history_obj, rewriting=True, part_number=2)
```

`write_file(content: str) -> None`
Writes content to history using appropriate method based on operation mode.

**Behavior:**
- Skips writing if write_history is False
- Uses replace_history_part() for rewriting operations
- Uses append_history() for standard appending operations
- Handles content persistence through history object

**Example Usage:**
```python
handler.write_file("Generated content")
```

`handle_token(content: str) -> None`
Handles individual tokens from the stream with buffering optimization.

**Behavior:**
- Accumulates tokens in complete_response for final output
- Writes immediately for append operations
- Buffers tokens for rewrite operations to reduce I/O
- Uses time-based buffering with configurable write interval
- Thread-safe token processing with buffer lock

**Example Usage:**
```python
handler.handle_token("Hello")
handler.handle_token(" world")
```

`flush_buffer() -> None`
Flushes any remaining buffered content to storage.

**Behavior:**
- Thread-safe buffer flushing with lock
- Writes buffered content if present
- Resets buffer and updates write time
- Ensures no content is lost during finalization

**Example Usage:**
```python
handler.flush_buffer()
```

`finalize() -> str`
Completes the token handling process and returns the complete response.

**Behavior:**
- Flushes any remaining buffered content
- Fixes history separators if writing to history
- Returns the complete accumulated response
- Finalizes the streaming session

**Example Usage:**
```python
complete_text = handler.finalize()
```

`get_token_callback() -> Callable[[str], None]`
Returns a callback function for token handling integration.

**Behavior:**
- Provides handle_token method as callback function
- Enables integration with streaming components
- Maintains proper method binding for token processing

**Example Usage:**
```python
callback = handler.get_token_callback()
streamer = Streamer(callback)
```

## Configuration Usage

### Primary Configuration Sources:
- `config.WRITE_INTERVAL`: Time interval for buffered write operations

## Usage Patterns

### Append Mode (Default):
- Tokens are written immediately to history
- No buffering overhead for real-time output
- Used for new content generation

### Rewrite Mode:
- Tokens are buffered to reduce I/O operations
- Periodic writes based on time interval
- Complete response replaces existing history part
- Used for content modification and regeneration

### Buffer Management:
- Thread-safe operations with locking
- Time-based flushing for optimal performance
- Automatic finalization ensures no data loss

## Integration Points

- **Streamer**: Receives token callback for real-time processing
- **History Module**: Uses history objects for content persistence
- **Chat Module**: Integrates for story generation and modification workflows
- **stream.py**: Orchestrates TokenHandler with Streamer for complete streaming pipeline
