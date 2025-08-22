## Generator.py
Handles story writing operations including scene generation, regeneration, and custom prompts.

### Methods:

#### `write_scene() -> None`
Writes the next story part by generating new content based on existing story context and summary  

- **Process**: 
  - Retrieves story objects from Factory
  - Merges story with summary for context
  - Composes prompt for scene writing
  - Streams the generated content

- **Code flow**:

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

#### `custom_prompt() -> None`
Similar to `write_scene()` but without automatic writing instructions appended to the prompt  

- **Process**:  
Same as `write_scene()` but uses "Custom prompt" prompt type

#### `continue_response(part_number: int) -> None`
Similar to `write_scene()` but puts the specified part number as assistant response

- **Process**:  
  - Retrieves story objects from Factory
  - Validates part number
  - Sets specified part as assistant response and removes it from parts
  - Merges story with summary for context
  - Composes prompt using "Custom prompt" type
  - Streams the generated content

#### `regenerate(part_number: int) -> None`
Regenerates an existing story part by replacing it with new content

- **Process**:
  - Retrieves story objects
  - Cuts history to specified part number minus 1
  - Composes prompt for scene writing
  - Streams new content with rewrite flag enabled

#### `add_part(part_number: int) -> None`
Adds a new story part after the specified part number instead of appending to the end

- **Process**:
  - Adds empty part at specified position
  - Cuts history to include parts up to insertion point
  - Streams new content for the inserted part
