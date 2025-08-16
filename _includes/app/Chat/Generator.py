from ..Composers.PromptComposer import compose_prompt
from ..History.Factory import Factory
from ..Streaming.stream import stream

class Generator:

    @staticmethod
    def write_scene() -> None:
        
        story, story_parsed, summary = Factory.get_objects()
        story_parsed.merge_with_summary(summary)
        story_parsed.parse_assistant_response()

        messages = compose_prompt("Write scene", story_parsed)

        stream(story, messages)

    @staticmethod
    def custom_prompt() -> None:
        
        story, story_parsed, summary = Factory.get_objects()
        story_parsed.merge_with_summary(summary)
        story_parsed.parse_assistant_response()

        messages = compose_prompt("Custom prompt", story_parsed)

        stream(story, messages)

    @staticmethod
    def regenerate(part_number: int) -> None:
        
        story, story_parsed, summary = Factory.get_objects()
        story_parsed.merge_with_summary(summary)
        story_parsed.cut_history_to_part_number(part_number-1)

        messages = compose_prompt("Write scene", story_parsed)

        stream(story, messages, rewrite=True, part_number=part_number)

    @staticmethod
    def add_part(part_number: int) -> None:
        
        story, story_parsed, summary = Factory.get_objects()

        story.add_part("", part_number)

        story_parsed.merge_with_summary(summary)
        story_parsed.cut_history_to_part_number(part_number)
        part_number += 1

        messages = compose_prompt("Write scene", story_parsed)
        stream(story, messages, rewrite=True, part_number=part_number)