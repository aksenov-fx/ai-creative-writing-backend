# ConfigDataClass Module Specification

## Overview
Defines the core configuration data structure using Python dataclasses to provide type-safe configuration management with centralized settings validation.

## Dependencies
None.

## Core Functions
Centralized configuration schema with type annotations for all system settings.

**Behavior:**
- Serves as the single source of truth for configuration structure
- Enables IDE autocompletion and type checking
- Supports dataclass operations like asdict() for serialization

**Configuration Fields:**
- **Prompt Settings**: system_prompt, history_prefix, introduction, variables, prompts_structure, abbreviations, translation_language, trim_history, use_summary, include_previous_part_when_summarizing, include_previous_part_when_rewriting
- **API Configuration**: temperature, max_tokens, endpoints, default_endpoint, endpoint, models, default_model, summary_model, model, include_reasoning
- **Parsing Parameters**: separator
- **Output Settings**: print_messages, print_reasoning
- **File Paths**: history_path, summary_yaml_path, summary_md_path, prompts_path, folder_path, settings_folder
- **Runtime Flags**: interrupt_flag, debug
- **Chat Settings**: splitter, add_header, chat_with_story, include_file
- **Constants**: WRITE_INTERVAL, PORT, TOKEN_ESTIMATION_DIVISOR, BUFFER_SIZE, TIMESTAMP_UPDATE_DELAY, RETRY_BASE_DELAY

## Configuration Usage
- Used as the primary configuration container throughout the application
- Instantiated by story_config.get_story_config() and chat_config.get_chat_config()
- Passed to override_config.override_config() for temporary modifications

## Usage Patterns
- **Initialization**: Created with default values from YAML configuration files
- **Serialization**: Converted to dictionaries for configuration merging operations

## Integration Points
- **story_config**: Uses ConfigDataClass as return type for get_story_config()
- **chat_config**: Uses ConfigDataClass as input parameter for get_chat_config()
- **override_config**: Accepts ConfigDataClass instances for temporary overrides
- **All modules**: Receives ConfigDataClass instances for runtime configuration access
