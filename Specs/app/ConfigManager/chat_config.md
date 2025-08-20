# chat_config Module Specification

## Overview
Manages chat-specific configuration by merging default settings with runtime overrides, handling story integration for chat contexts.

## Dependencies
- `..Utility` - For YAML file reading utilities
- `.commons` - For model resolution via get_model()

## Core Functions

`get_story_path(file, current_config, default_config) -> str`
Determines the appropriate story file path for chat integration based on configuration.

**Behavior:**
- Returns empty string if chat_with_story is False
- Resolves parent directory from the provided file path
- Loads story configuration to determine history and summary paths
- Returns summary path if use_summary is True, otherwise returns story path

`get_chat_config(file, config, default_config) -> dict`
Composes complete chat configuration by merging multiple configuration sources.

**Behavior:**
- Loads default chat settings from Chat Settings.yaml
- Applies runtime overrides from the provided file
- Resolves model name using get_model() from commons
- Determines story file path for integration when chat_with_story is enabled
- Returns merged configuration dictionary ready for chat operations

## Configuration Usage

### Primary Configuration Sources:
- **Default Chat Settings**: Chat Settings.yaml in settings folder
- **Runtime Overrides**: YAML files provided at runtime
- **Story Integration**: Settings.md from parent story directories
- **Model Resolution**: Uses commons.get_model() for model name resolution

## Usage Patterns

### Chat Configuration Flow:
- Used by chat interfaces to load conversation-specific settings
- Merges default chat behavior with story-specific overrides
- Handles story context integration for chat-with-story mode
- Provides complete configuration dictionary for chat operations

### Story Integration:
- Automatically detects parent story directories
- Loads story configuration to determine file paths
- Enables seamless switching between standalone chat and story-integrated chat

## Integration Points
- **Chat Module**: Uses get_chat_config() to load conversation settings
- **commons**: Uses get_model() for model name resolution
- **Utility**: Uses read_yaml() for configuration file loading
- **Story directories**: Reads Settings.md files from parent directories
