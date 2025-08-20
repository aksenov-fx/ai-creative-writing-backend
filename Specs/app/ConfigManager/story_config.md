# story_config Module Specification

## Overview
Manages story-specific configuration by loading and merging multiple configuration files, providing complete story environment setup.

## Dependencies
- `..Utility` - For YAML file reading and file utilities
- `.commons` - For model and endpoint resolution via get_model() and get_endpoint()

## Core Functions

`load_config(folder_path, config_dict, extension='.yaml') -> dict`
Loads and merges multiple configuration files into a unified configuration dictionary.

**Behavior:**
- Loads configuration from specified files with given extension
- Merges Variables, Abbreviations, Prompts Structure, Models, and Endpoints
- Resolves model and endpoint configurations using commons utilities
- Returns complete merged configuration dictionary

**Configuration Files Loaded:**
- **Variables**: Contains story-specific variable definitions
- **Abbreviations**: Defines abbreviation mappings for story processing
- **Prompts Structure**: Defines prompt templates and structure
- **Models**: Contains model configurations and parameters
- **Endpoints**: Defines API endpoints and authentication

`get_story_config(folder_path, extension='.yaml') -> dict`
Composes complete story configuration by loading all necessary configuration files.

**Behavior:**
- Loads default configuration from ConfigDataClass
- Merges story-specific configuration files using load_config()
- Resolves model name using get_model() from commons
- Resolves endpoint configuration using get_endpoint() from commons
- Returns complete configuration dictionary ready for story operations

## Usage Patterns

### Story Configuration Flow:
- Used by story interfaces to load story-specific settings
- Merges default configuration with story-specific overrides
- Provides complete configuration for story generation and processing
- Handles model and endpoint resolution

## Integration Points
- **Story Module**: Uses get_story_config() to load story-specific settings
- **commons**: Uses get_model() and get_endpoint() for resolution
- **Utility**: Uses read_yaml() and file utilities for configuration loading
- **All story operations**: Provides complete configuration for story generation
