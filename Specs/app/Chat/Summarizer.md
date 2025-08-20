## Summarizer.py
Creates and manages story summaries for context management and efficient storage.

### Methods:

#### `summarize_parts(part_number: int) -> str`
Summarizes a specific story part for inclusion in the summary
- **Process**:
  - Retrieves summary parsed object
  - Cuts history to specified part with optional inclusion of previous part
  - Composes prompt for summarization
  - Streams summary without writing to history
  - Returns summary text

#### `update_summary() -> None`
Updates the complete story summary by processing all unsummarized parts
- **Process**:
  - Validates story content exists
  - Updates story hashes
  - Updates summary from story parts
  - Configures model for summarization
  - Calls summarize_parts on each part to get part summary
  - Updates summary with new content

- **Code flow**:

  Summarizer.update_summary()
    ├── Factory.get_story() → story
    ├── story.update_hashes()
    ├── Factory.get_summary().update_from_story_parts(story) → summary
    ├── config.model = config.models[config.summary_model]['name']
    └── for part_number, hash_key in enumerate(summary.keys):
        ├── Summarizer.summarize_parts(part_number+1) → result
        │   ├── Factory.get_summary_parsed() → summary_parsed
        │   ├── summary_parsed.cut(part_number, config.include_previous_part_when_summarizing)
        │   ├── compose_prompt("Summarize part", summary_parsed, include_introduction=False) → messages
        │   │   ├── validate(include_introduction=False, validate_user_prompt=False)
        │   │   ├── expand_abbreviations(prompt_structure, config.variables)
        │   │   ├── summary_parsed.trim_content() [if config.trim_history]
        │   │   └── ApiComposer.compose_messages(combined_prompt, summary_parsed.assistant_response)
        │   │       ├── append_message(messages, "system", config.system_prompt)
        │   │       ├── append_message(messages, "user", user_prompt)
        │   │       └── append_message(messages, "assistant", assistant_response)
        │   │
        │   └── stream(None, messages, write_history=False) → result
        │       ├── TokenHandler(None, rewrite=False, write_history=False, part_number=0)
        │       ├── Streamer(token_handler.get_token_callback())
        │       └── streamer.stream_response(messages)
        │           ├── openai.OpenAI.chat.completions.create()
        │           ├── for chunk in response:
        │           │   └── token_handler.handle_token(delta.content)
        │           └── token_handler.finalize() → result
        │
        ├── summary.yaml_data[hash_key]['summarized'] = True
        └── summary.replace_history_part(result, hash_key)