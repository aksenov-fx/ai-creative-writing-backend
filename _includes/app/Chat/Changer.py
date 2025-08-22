from ..Composers.PromptComposer import compose_prompt
from ..Composers.PromptComposer import validate_part_number
from ..History.Factory import Factory
from ..Streaming.stream import stream
from _includes import config

class Changer:

    @staticmethod
    def change_part(part_number: int) -> None:
        """Sends the part text to model for rewriting"""

        story = Factory.get_story()
        story_parsed = Factory.get_story_parsed()

        validate_part_number(story.count, part_number)
        story_parsed.cut(part_number, include_previous_part=config.include_previous_part_when_rewriting)

        messages = compose_prompt("Change part", story_parsed, include_introduction=False)

        print(f"Rewriting part {part_number}/{story.count-1}")
        stream(story, messages, rewrite=True, part_number=part_number)

    @staticmethod
    def change_parts(part_number: int) -> None:
        """Same as change_part but rewrites all parts after the specified part"""
        
        story = Factory.get_story()
        for part in range(part_number, story.count):
            Changer.change_part(part)
