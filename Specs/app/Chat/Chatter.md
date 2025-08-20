## Chatter.py
Manages conversational interactions separate from story writing operations.

### Methods:

#### `chat(file_path: str) -> None`
Handles general chat conversations that are not related to story writing

- **Arguments**:
  - `file_path: str` - Path to the chat history file

- **Process**:
  - Retrieves chat history objects from Factory
  - Processes chat history
  - Composes chat messages using ApiComposer
  - Insert seaprator to chat history
  - Streams chat response

- **Workflow**:

  Chatter.chat(file_path)
    ├── Factory.get_chat_objects(file_path)
    │   ├── Factory.get_chat_history(file_path) → ChatHistoryChanger
    │   └── Factory.get_chat_history_parsed(file_path) → ChatHistoryParser
    │
    ├── ChatHistoryParser.process()
    │   ├── split_conversation()
    │   ├── clean_header()
    │   ├── trim_content() [if config.trim_history]
    │   ├── include_file() [if config.include_file]
    │   └── parse_instructions()
    │
    ├── ApiComposer.compose_chat_messages(history_parsed)
    │   ├── append_message(messages, "system", history.custom_instructions)
    │   └── for each part in history.parts:
    │       ├── append_message(messages, "user", part[i]) [i % 2 == 0]
    │       └── append_message(messages, "assistant", part[i]) [i % 2 == 1]
    │
    ├── ChatHistoryChanger.fix_separator()
    │
    └── stream(history, messages)
        ├── TokenHandler(history, rewrite=False, write_history=True, part_number=0)
        ├── Streamer(token_handler.get_token_callback())
        └── streamer.stream_response(messages)
            └── token_handler.finalize()
