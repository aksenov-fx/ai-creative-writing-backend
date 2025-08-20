## Helpers.py
Utility functions for text manipulation and formatting without context or file operations.

### Methods:

#### `rewrite_selection(selected_text: str) -> str`
Rewrites selected text according to user prompt without any context

- **Process**:
  - Composes helper prompt for rewriting
  - Streams response without writing to history
  - Returns the rewritten text

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