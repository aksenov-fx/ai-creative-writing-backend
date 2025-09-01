This is a Python backend for Obsidian Creative Writing plugin.  
For more details, please visit the [main repo](https://github.com/aksenov-fx/ai-creative-writing-obsidian-vault).  

## AI Story Writer - Python Backend

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

## Configuration
### Prompt variables
**system_prompt:** custom instructions  
**introduction:** story introduction  
**variables:** variables for composing prompts, like writing guidelines  
**prompts_structure:** A text for each prompt type that will be used to compose prompts, like Write scene or Custom prompt. Can use variables  
**abbreviations:** abbreviations used in user prompts, like #O -> Oliver  
**translation_language:** language to translate text into  
**history_prefix:** story text prefix in API request  

### Story parsing settings
**separator:** separator for story parts in md file  

### Endpoints settings
**endpoints:** endpoints from endpoints.yaml, like openrouter or openai  
**default_endpoint:** default endpoint  
**endpoint:** actual endpoint  

### Models settings
**models:** models from models.yaml 
**default_model:** default model for all methods except for summarize() 
**summary_model:** model used to summarize parts  
**model:** actual model used in API request  

### Context length settings
**max_tokens:** defines context length if trim_history is True  
**trim_history:** exclude first story parts if story exceeds max_tokens  
**use_summary:** Replace story parts with summaries in API request to reduce token usage. The last story part will remain original to preserve writing style.  
**include_previous_part_when_summarizing:** include previous story part in API request when summarizing part  
**include_previous_part_when_rewriting:** include previous story part in API request when rewriting part  

### API settings
**temperature:** temperature  

### Output settings
**print_messages:** print API request  
**include_reasoning:** include reasoning in API response  
**print_reasoning:** Print reasoning in terminal when using models that output reasoning tokens, like DeepSeek R1

### Paths
**history_path:** story or chat md file path  
**summary_yaml_path:** summary yaml path  
**summary_md_path:** path of a human readable summary file, generated from summary yaml  
**prompts_path:** prompts md file path  
**folder_path:** story folder path  
**settings_folder:** default settings folder path  

### Runtime flags
**interrupt_flag:** stops response generation if set to True  
**debug:** prints API request but does not send it to inference provider  

### Chat settings that are not used in story mode
**custom_instructions_folder:** folder with system prompts for chat mode  
**splitter:** text line used to exclude previous conversation history from API request  
**add_header:** make first line of user prompts into headers in md file for readability  
**chat_with_story:** append story text to the first user message in chat  
**use_summary:** Append summary text instead of full story to the first user message in chat to reduce token usage.  
**include_file:** actual file path to include in API request depending on chat_with_story and use_summary setting.  

### Constants
**PORT:** port for listener.py  
**BUFFER_SIZE:** buffer size for listener.py  
**TOKEN_ESTIMATION_DIVISOR:** token estimation divisor for trim_history setting.  
**WRITE_INTERVAL:** a pause to make between file writes when writing whole story content in rewrite mode instead of appending to it in write mode. Used to prevent high I/O with big stories. Does not slow down response generation.  
**TIMESTAMP_UPDATE_DELAY:** delay before updating time stamp after finishing writing to md file.    
**RETRY_BASE_DELAY:** retry delay when failing to write to md file.  

## Project structure

```
. 📂 python-backend
└── 📂 _includes/
│  └── 📂 settings/
│    └── 📂 _instructions/
│    ├── 📄 Abbreviations.yaml  
│    ├── 📄 Chat Settings.yaml  
│    ├── 📄 Endpoints.yaml
│    ├── 📄 Models.yaml
│    ├── 📄 Prompts Structure.yaml
│    ├── 📄 Settings.yaml
│    ├── 📄 Variables.yaml
│  ├── 📄 __init__.py
│  ├── 📄 config.py
│  ├── 📄 listener.py
│  └── 📂 app/
│    ├── 📄 dispatcher.py
│    └── 📂 Chat/
│      ├── 📄 __init__.py
│      ├── 📄 Changer.py
│      ├── 📄 Chatter.py
│      ├── 📄 Generator.py
│      ├── 📄 Helpers.py
│      ├── 📄 Summarizer.py
│      ├── 📄 Prompts.py
│    └── 📂 Composers/
│      ├── 📄 ApiComposer.py
│      ├── 📄 PromptComposer.py
│    └── 📂 ConfigManager/
│      ├── 📄 __init__.py
│      ├── 📄 ConfigDataClass.py
│      ├── 📄 chat_config.py
│      ├── 📄 story_config.py
│      ├── 📄 override_config.py
│      ├── 📄 commons.py
│    └── 📂 History/
│      └── 📂 Mixins/
│        ├── 📄 ChangerMixin.py
│        ├── 📄 ParserMixin.py
│        ├── 📄 TrimMixin.py
│      ├── 📄 ChatHistory.py
│      ├── 📄 Story.py
│      ├── 📄 Summary.py
│      ├── 📄 Factory.py
│    └── 📂 Streaming/
│      ├── 📄 Streamer.py
│      ├── 📄 TokenHandler.py
│      ├── 📄 stream.py
│    └── 📂 Utility/
│      ├── 📄 __init__.py
│      ├── 📄 readers.py
│      ├── 📄 writers.py
│      ├── 📄 other_utils.py
```

## Code flow example

```
  Generator.write_scene()
    ├── Factory.get_objects() → (story, story_parsed, summary)
    │   ├── Factory.get_story() → StoryChanger
    │   ├── Factory.get_story_parsed() → StoryParser
    │   └── Factory.get_summary() → SummaryChanger
    │
    ├── story_parsed.merge_with_summary(summary)
    │
    ├── compose_prompt("Write scene", story_parsed) → messages
    │   ├── validate(include_introduction=True)
    │   ├── expand_abbreviations(prompt_structure, config.variables)
    │   ├── history_parsed.trim_content() [if config.trim_history]
    │   ├── expand_abbreviations(config.introduction)
    │   └── ApiComposer.compose_messages(combined_prompt, history_parsed.assistant_response)
    │       ├── append_message(messages, "system", config.system_prompt)
    │       ├── append_message(messages, "user", user_prompt)
    │       └── append_message(messages, "assistant", assistant_response)
    │
    └── stream(story, messages)
        ├── TokenHandler(story, rewrite=False, write_history=True, part_number=0)
        ├── Streamer(token_handler.get_token_callback())
        └── streamer.stream_response(messages)
            ├── openai.OpenAI.chat.completions.create()
            ├── for chunk in response:
            │   └── token_handler.handle_token(delta.content)
            └── token_handler.finalize()
```