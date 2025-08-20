## Generator.py
Handles story writing operations including scene generation, regeneration, and custom prompts.

### Methods:

#### `write_scene() -> None`
Writes the next story part by generating new content based on existing story context and summary  

- **Process**: 
  - Retrieves story objects from Factory
  - Merges story with summary for context
  - Parses assistant response
  - Composes prompt for scene writing
  - Streams the generated content

#### `custom_prompt() -> None`
Similar to `write_scene()` but without automatic writing instructions appended to the prompt  

- **Process**:  
Same as `write_scene()` but uses "Custom prompt" prompt type

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
