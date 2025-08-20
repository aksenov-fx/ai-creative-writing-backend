## Changer.py
Handles story changing operations like rewriting parts of existing stories.

### Methods:

#### `change_part(part_number: int) -> None`
Sends an existing story part to the model for rewriting while maintaining context

- **Process**:
  - Retrieves story and parsed story objects
  - Cuts history to specified part with optional inclusion of previous part
  - Composes prompt for part changing
  - Streams rewritten content with rewrite flag enabled
- **Returns**: None (streams response directly)

#### `change_parts(part_number: int) -> None`
Rewrites all story parts from the specified part number onwards

- **Process**:
  - Iterates through all parts from specified number
  - Calls `change_part()` for each part sequentially
  - Prints progress information

- **Code flow**:

  Changer.change_parts(part_number)
    ├── Factory.get_story() → story
    ├── print(f"Rewriting part {part_number}/{story.count-1}")
    └── for part in range(part_number, story.count):
        └── Changer.change_part(part)
            ├── Factory.get_story() → story
            ├── Factory.get_story_parsed() → story_parsed
            ├── story_parsed.cut(part_number, include_previous_part=config.include_previous_part_when_rewriting)
            │
            ├── compose_prompt("Change part", story_parsed, include_introduction=False) → messages
            │   ├── validate(include_introduction=False)
            │   ├── expand_abbreviations(prompt_structure, config.variables)
            │   ├── story_parsed.trim_content() [if config.trim_history]
            │   └── ApiComposer.compose_messages(combined_prompt, story_parsed.assistant_response)
            │       ├── append_message(messages, "system", config.system_prompt)
            │       ├── append_message(messages, "user", user_prompt)
            │       └── append_message(messages, "assistant", assistant_response)
            │
            └── stream(story, messages, rewrite=True, part_number=part_number)
                ├── TokenHandler(story, rewrite=True, write_history=True, part_number=part_number)
                ├── Streamer(token_handler.get_token_callback())
                └── streamer.stream_response(messages)
                    ├── openai.OpenAI.chat.completions.create()
                    ├── for chunk in response:
                    │   └── token_handler.handle_token(delta.content)
                    └── token_handler.finalize()