# ParserMixin Module Specification

## Overview
Common parsing methods for History and Summary parsers, providing content manipulation and navigation functionality for story parts.

## Dependencies
- No external dependencies - operates on instance attributes

## Core Functions

`update(parts) -> None`
Updates the object state with new parts array and recalculates derived properties.

**Behavior:**
- Sets self.parts to the provided parts array
- Joins parts using join_parts() method to update self.content
- Creates self.parsed by joining parts with double newlines
- Updates self.count with the length of parts array

**Example Usage:**
```python
parser.update(new_parts_list)
```

`cut_history_to_part_number(part_number) -> self`
Cuts the history to include only parts up to the specified part number.

**Behavior:**
- Slices self.parts array from start to part_number
- Calls update() to refresh object state
- Returns self for method chaining

**Example Usage:**
```python
parser.cut_history_to_part_number(5)
```

`set_part_number_content(part_number) -> self`
Sets the content of a specific part number to part_number_content attribute.

**Behavior:**
- Accesses parts array using 1-based indexing (part_number-1)
- Sets self.part_number_content to the specified part content
- Returns self for method chaining

**Example Usage:**
```python
parser.set_part_number_content(3)
```

`set_to_previous_part() -> self`
Updates the object to contain only the second-to-last part.

**Behavior:**
- Slices self.parts to get only the second-to-last element
- Calls update() to refresh object state
- Returns self for method chaining

**Example Usage:**
```python
parser.set_to_previous_part()
```

`cut(part_number, include_previous_part) -> self`
Comprehensive cutting operation that can either clear content or cut to a specific part.

**Behavior:**
- If include_previous_part is False: clears all content, parts, and parsed data
- If include_previous_part is True: performs sequential operations to cut to part_number, set content, and move to previous part
- Returns self for method chaining

**Example Usage:**
```python
parser.cut(4, True)
```

## Configuration Usage
- No direct configuration usage - operates on object state

## Usage Patterns
- **Content Navigation**: Moving between different parts of story history
- **State Management**: Updating object state when content changes
- **Method Chaining**: All methods return self for fluent interface
- **History Manipulation**: Cutting and trimming story content

## Integration Points
- **History Module**: Provides core parsing functionality for history objects
- **Summary Module**: Used for summary content manipulation
- **Content Management**: Works with self.parts, self.content, and self.parsed attributes
