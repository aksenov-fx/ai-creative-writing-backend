# PromptComposer Module Specification

## Overview
Handles prompt validation, expansion of abbreviations, and composition of complete prompt structures for API consumption.

## Dependencies
- `_includes.config` - For configuration access (prompts_structure, introduction, variables, abbreviations)
- `.ApiComposer` - For final message composition
- `..History.Factory` - For retrieving prompts from history

## Core Functions

### Validation Functions

#### `validate(include_introduction: bool, validate_user_prompt: bool = True) -> None`
Validates required configuration values before prompt composition.

**Parameters:**
- `include_introduction` (bool): Whether to validate introduction configuration
- `validate_user_prompt` (bool): Whether to validate user prompt presence (default: True)

**Raises:**
- `ValueError`: If introduction is required but not set
- `ValueError`: If user prompt is required but not set

### Prompt Composition Functions

#### `compose_prompt(method: str, history_parsed, include_introduction=True)`
Composes a complete prompt structure for story generation.

**Process:**
1. Validates required configuration based on method
2. Retrieves prompt structure from config.prompts_structure[method]
3. Expands abbreviations in prompt structure using config.variables
4. Trims history content if config.trim_history is enabled
5. Combines introduction, history, and user prompt into final prompt
6. Returns composed messages via ApiComposer.compose_messages()

#### `compose_helper_prompt(prompt_key: str, selected_text: str) -> list`
Composes prompts for helper operations like translation or editing.

**Special Handling:**
- For "Translate" key: Appends translation language from config.translation_language

### Text Processing Functions

#### `expand_abbreviations(text: str, abbreviations: dict = None) -> str`
Replaces abbreviations in text with their corresponding values.

**Parameters:**
- `text` (str): The text to expand abbreviations in
- `abbreviations` (dict): The abbreviations to use (defaults to config.abbreviations)

**Returns:**
- `str`: The text with abbreviations expanded

**Pattern Matching:**
- Case-insensitive matching
- Matches text preceded by # or whitespace/newline
- Followed by delimiters: :, ., ?, !, ', ', \s, $ (end of string)

**Usage Patterns:**
- Expands abbreviations from config.abbreviations for user prompt and introduction
- Expands variables from config.variables in config.prompts_structure

## Configuration Usage

### Primary Configuration Sources:
- `config.prompts_structure`: YAML-defined prompt templates for different methods
- `config.introduction`: Story introduction text
- `config.variables`: Runtime variables including #user_prompt
- `config.abbreviations`: Abbreviation mappings for text expansion
- `config.trim_history`: Boolean flag for history trimming
- `config.history_prefix`: Prefix text for history sections
- `config.translation_language`: Target language for translation operations

## Usage Patterns

- All prompt composition flows through compose_prompt() for main story generation
- Helper operations use compose_helper_prompt() for text processing tasks
- Abbreviation expansion is applied consistently across all text processing
- Validation ensures required configuration is present before composition
- Prompts are constructed hierarchically: introduction → history → user prompt → part number content
