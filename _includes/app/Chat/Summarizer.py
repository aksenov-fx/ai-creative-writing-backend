from ..Composers.PromptComposer import compose_prompt
from ..History.Factory import Factory
from ..Streaming.stream import stream
from _includes import config

class Summarizer:

    @staticmethod
    def summarize_part(part_number: int) -> None:

        summary_parsed = Factory.get_summary_parsed()
        print(f"Summarizing part {part_number}/{summary_parsed.count}")

        summary_parsed.cut(part_number, config.include_previous_part_when_summarizing)

        messages = compose_prompt("Summarize part", summary_parsed, include_introduction=False)
        return stream(None, messages, write_history=False)

    @staticmethod
    def update_summary() -> None:
        
        # Get story
        story = Factory.get_story()
        if not story.content: raise ValueError("Story file is empty or not found")

        # Update summary from story parts
        story.update_hashes()
        summary = Factory.get_summary().update_from_story_parts(story)

        config.model = config.models[config.summary_model]['name']

        for part_number, hash_key in enumerate(summary.keys):
            if config.interrupt_flag: break
            if summary.yaml_data[hash_key]['summarized']: continue
            
            result = Summarizer.summarize_part(part_number+1)
            summary.yaml_data[hash_key]['summarized'] = True
            summary.replace_history_part(result, hash_key)