from ..Composers.PromptComposer import compose_prompt
from ..Composers.PromptComposer import validate_part_number
from ..History.Factory import Factory
from ..Streaming.stream import stream

class Generator:

    @staticmethod
    def write_scene(part_number = None) -> None:
        """Write next story part"""

        story, story_parsed, summary = Factory.get_objects()
        story_parsed.merge_with_summary(summary)
        story_parsed.parse_assistant_response()

        messages = compose_prompt("Write scene", story_parsed)

        stream(story, messages)

    @staticmethod
    def custom_prompt(part_number = None) -> None:
        """Same as write_scene but does not append writing instructions"""

        story, story_parsed, summary = Factory.get_objects()
        story_parsed.merge_with_summary(summary)
        story_parsed.parse_assistant_response()

        messages = compose_prompt("Custom prompt", story_parsed)

        stream(story, messages)

    @staticmethod
    def regenerate(part_number: int) -> None:
        """Same as write_scene but replaces the existing part instead of appending"""

        story, story_parsed, summary = Factory.get_objects()

        validate_part_number(story.count, part_number)
        story_parsed.merge_with_summary(summary)
        story_parsed.cut_history_to_part_number(part_number-1)

        messages = compose_prompt("Write scene", story_parsed)

        stream(story, messages, rewrite=True, part_number=part_number)

    @staticmethod
    def add_part(part_number: int) -> None:
        """Same as write_scene but adds a part after the specified part instead of appending"""

        story, story_parsed, summary = Factory.get_objects()

        validate_part_number(story.count, part_number)
        story.add_part("added part", part_number)

        story_parsed.merge_with_summary(summary)
        story_parsed.cut_history_to_part_number(part_number)
        part_number += 1

        messages = compose_prompt("Write scene", story_parsed)
        stream(story, messages, rewrite=True, part_number=part_number)