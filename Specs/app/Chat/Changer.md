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