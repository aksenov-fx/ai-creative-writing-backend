# Prompts Module Specification

## Overview
Manages prompt storage and retrieval with abbreviation expansion for user prompt customization and reuse.

## Dependencies
- `..Utility` - For file operations and timestamp updates
- `.Mixins.ChangerMixin` - For content modification operations
- `...config` - For configuration access (separator)
- `..Composers.PromptComposer` - For abbreviation expansion functionality

## Core Functions

### PromptChanger Functions

#### `__init__(path: str) -> None`
Initializes prompt manager with file path and loads content.

**Behavior:**
- Loads prompt content from file
- Splits content into parts using separator
- Sets up configuration and separator

**Example Usage:**
```python
prompts = PromptChanger("path/to/prompts.md")
```

#### `split_history() -> List[str]`
Splits prompt content into individual parts using configured separator.

**Behavior:**
- Splits content by separator
- Strips whitespace from each part
- Returns list of prompt parts

**Example Usage:**
```python
parts = prompts.split_history()
```

#### `return_part(part_number: int) -> str`
Returns specific prompt part by number.

**Behavior:**
- Returns stripped content of specified part
- Uses zero-based indexing

**Example Usage:**
```python
prompt = prompts.return_part(0)
```

#### `fix_separator() -> None`
Ensures prompts file ends with proper separator formatting.

**Behavior:**
- Appends separator if last part is not empty
- Updates file timestamp

**Example Usage:**
```python
prompts.fix_separator()
```

#### `get_user_prompt(part_value: int, abbreviations: dict) -> str`
Retrieves and processes user prompt with abbreviation expansion.

**Behavior:**
- Gets prompt part using 1-based indexing
- Expands abbreviations using PromptComposer
- Prints processed prompt for user feedback
- Fixes separator formatting
- Returns expanded prompt text

**Example Usage:**
```python
prompt = prompts.get_user_prompt(1, abbrev_dict)
```

## Configuration Usage

### Primary Configuration Sources:
- `config.separator`: Prompt part separator string

## Usage Patterns

### Prompt Management Flow:
- Load prompts file and split into numbered parts
- Retrieve specific prompt by part number
- Expand abbreviations for customization
- Ensure proper file formatting with separators

### Abbreviation System:
- Prompts can contain abbreviation placeholders
- Abbreviations expanded using PromptComposer
- Allows for dynamic prompt customization
- Supports reusable prompt templates

### Part-Based Organization:
- Prompts stored as numbered parts in single file
- Each part separated by configured separator
- 1-based indexing for user-friendly numbering
- Easy addition and modification of prompts

## Integration Points

- **PromptComposer**: Uses expand_abbreviations for prompt processing
- **ConfigManager**: Supplies separator configuration
- **Utility Module**: Handles file I/O and timestamp operations
- **Factory Module**: Creates prompt instances with proper paths
- **Chat Module**: Uses processed prompts for user interactions
