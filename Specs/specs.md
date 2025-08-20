## AI Story Writer Project - Python Backend Specification

### Technical Overview

The AI Story Writer is a Python-based backend system designed for AI-assisted creative writing and interactive storytelling.  
The system uses OpenAI-compatible APIs for text generation and implements real-time streaming responses with support for reasoning models.

### Core Architecture

- **Chat**: Core business logic for story generation and chat
- **Composers**: Prompt and API request composition
- **Streaming**: Real-time token streaming and response handling
- **History**: Persistent storage and retrieval of story/chat history
- **ConfigManager**: Centralized settings and runtime configuration
- **Utility**: Common functionality and helper methods

### Configuration Sources

- **YAML Files**: Primary configuration through YAML files in settings folder
- **Runtime Overrides**: Dynamic configuration changes during execution using cascading config pattern and direct config value changes

### Module Descriptions

### Chat Module
Core story generation and chat interaction logic  

**Files**:
- **Generator**: Handles story writing operations including scene generation, regeneration, and custom prompts
- **Changer**: Handles story changing operations like rewriting parts
- **Chatter**: Manages conversational interactions separate from story writing
- **Summarizer**: Creates story summaries for context management
- **Helpers**: Utility functions for story manipulation and formatting

### Streaming Module
Real-time streaming of AI responses with token-by-token delivery  

**Files**:
- **Streamer**: Core streaming engine that manages the connection to AI APIs and handles real-time token delivery
- **TokenHandler**: Processes individual tokens and manages streaming state, buffering, and output formatting
- **stream**: Low-level streaming utilities and connection management for API endpoints

### History Module
Persistent storage and management of story and chat history  

**Files**:
- **Story**: Core story data structure and persistence layer for managing complete story narratives
- **ChatHistory**: Manages conversational history and context retention for ongoing interactions
- **Summary**: Handles story and chat summarization for efficient context management
- **Factory**: Factory pattern implementation for creating and loading history instances

### ConfigManager Module
Centralized configuration management with runtime overrides  

**Files**:
- **ConfigDataClass**: Core configuration data structures and validation schemas
- **chat_config**: Chat-specific configuration management including model settings and prompt templates
- **story_config**: Story generation configuration including genre settings and writing parameters
- **override_config**: Runtime configuration override system for dynamic settings changes
- **commons**: Shared configuration utilities and common configuration patterns

### Composers Module
Message composition and API request preparation  

**Files**:
- **PromptComposer**: Constructs and formats prompts for story generation and chat interactions
- **ApiComposer**: Prepares and structures API requests with proper formatting and parameter handling

### Utility Module
Common utility functions and helper methods  

**Files**:
- **readers**: File reading utilities for configuration, prompts, and story content
- **writers**: File writing utilities for saving stories, logs, and configuration updates
- **other_utils**: Miscellaneous helper functions including text processing, validation, and common operations
