## Helpers.py
Utility functions for text manipulation and formatting without context or file operations.

### Methods:

#### `rewrite_selection(selected_text: str) -> str`
Rewrites selected text according to user prompt without any context

- **Process**:
  - Composes helper prompt for rewriting
  - Streams response without writing to history
  - Returns the rewritten text

- **Code flow**:

  Helpers.rewrite_selection(selected_text)
    ├── compose_helper_prompt('Rewrite selection', selected_text) → messages
    │   ├── expand_abbreviations(prompt_structure, config.variables)
    │   └── ApiComposer.compose_messages(combined_prompt, None)
    │       ├── append_message(messages, "system", config.system_prompt)
    │       └── append_message(messages, "user", user_prompt)
    │
    └── stream(None, messages, write_history=False) → result
        ├── TokenHandler(None, rewrite=False, write_history=False, part_number=0)
        ├── Streamer(token_handler.get_token_callback())
        └── streamer.stream_response(messages)
            ├── openai.OpenAI.chat.completions.create()
            ├── for chunk in response:
            │   └── token_handler.handle_token(delta.content)
            └── token_handler.finalize() → result

#### `translate(selected_text: str) -> str`
Translates selected text to the language specified in configuration

- **Process**:
  - Composes helper prompt for translation
  - Streams response without writing to history
  - Returns the translated text

#### `explain(selected_text: str) -> str`
Explains the meaning of unknown words or concepts in the selected text

- **Process**:
  - Composes helper prompt for explanation
  - Streams response without writing to history
  - Returns the explanation