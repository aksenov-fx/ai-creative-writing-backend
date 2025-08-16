from ..Composers.PromptComposer import compose_prompt
from ..History.Factory import Factory
from ..Streaming.stream import stream
from _includes import config

class Changer:

    @staticmethod
    def change_part(part_number: int) -> None:
        
        story = Factory.get_story()
        story_parsed = Factory.get_story_parsed()
        story_parsed.cut(part_number, include_previous_part=config.include_previous_part_when_rewriting)

        messages = compose_prompt("Change part", story_parsed, include_introduction=False)

        stream(story, messages, rewrite=True, part_number=part_number)

    @staticmethod
    def change_parts(part_number: int) -> None:
        story = Factory.get_story()
        print(f"Rewriting part {part_number}/{story.count-1}")

        for part in range(part_number, story.count):
            Changer.change_part(part)
