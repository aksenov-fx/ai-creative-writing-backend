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