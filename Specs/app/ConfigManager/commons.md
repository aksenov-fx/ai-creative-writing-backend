# commons Module Specification

## Overview
Provides shared configuration utilities for model and endpoint resolution, centralizing common configuration operations across the application.

## Dependencies
- `..Utility` - For file reading utilities (read_file)

## Core Functions

`get_model(config_dict) -> str`
Resolves model names from configuration, supporting both direct model names and numeric indices.

**Behavior:**
- Returns default model name if no model is specified
- Handles numeric model selection (1-based indexing)
- Falls back to direct model name for non-numeric values
- Uses model configuration from config_dict['models']

**Model Resolution Logic:**
- If model is empty/None: uses default_model from configuration
- If model is numeric: uses 1-based index into models dictionary
- If model is string: returns the string directly as model name

`get_endpoint(config_dict) -> dict`
Resolves complete endpoint configuration including API key loading.

**Behavior:**
- Retrieves endpoint configuration from endpoints dictionary
- Loads API key from file specified in api_key_file field
- Returns complete endpoint configuration with populated API key
- Uses default_endpoint to select which endpoint configuration to use

## Usage Patterns

### Model Selection:
- Supports flexible model specification via name or index
- Enables runtime model switching without configuration file changes
- Provides fallback to default model for robust operation

### Endpoint Configuration:
- Centralizes API endpoint management
- Separates sensitive API keys from configuration files
- Enables easy switching between different AI service providers

## Integration Points
- **story_config**: Uses get_model() and get_endpoint() for story configuration
- **chat_config**: Uses get_model() for chat model resolution
- **Utility**: Uses read_file() for secure API key loading
- **All modules**: Provides consistent model and endpoint resolution
