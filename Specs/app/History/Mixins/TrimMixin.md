# TrimMixin Module Specification

## Overview
Provides token estimation and content trimming functionality for history objects, managing content size to stay within API token limits.

## Dependencies
- `self.config` - For token estimation and limit configuration parameters

## Core Functions

`estimate_tokens() -> int`
Estimates the number of tokens in the current content using a simple character-based calculation.

**Behavior:**
- Divides content length by TOKEN_ESTIMATION_DIVISOR from configuration
- Returns integer estimate of token count
- Uses floor division for conservative estimation

**Example Usage:**
```python
token_count = history.estimate_tokens()
```

`trim_content() -> str`
Trims content by removing parts from the beginning until token count is within limits.

**Behavior:**
- Calculates current token estimate using estimate_tokens()
- Enters trimming loop while tokens exceed max_tokens and sufficient parts remain
- Removes parts_to_trim number of parts from the beginning of self.parts
- Updates object state after each trimming operation
- Tracks removed_parts count for reporting
- Prints removal notification if any parts were removed
- Returns self for method chaining

**Example Usage:**
```python
history.trim_content()
```

## Configuration Usage

### Primary Configuration Sources:
- `config.TOKEN_ESTIMATION_DIVISOR`: Character-to-token ratio for estimation
- `config.max_tokens`: Maximum allowed token count
- `self.parts_to_trim`: Number of parts to remove in each trimming iteration

## Usage Patterns
- **Token Management**: Ensures content stays within API limits
- **Automatic Trimming**: Removes oldest content when limits are exceeded
- **Progressive Removal**: Trims in configurable chunks rather than all at once
- **User Feedback**: Provides notification when content is trimmed

## Integration Points
- **History Objects**: Operates on self.parts, self.content, and self.count
- **Configuration System**: Uses token limits and estimation parameters
- **Content Updates**: Works with update() method to refresh object state after trimming
