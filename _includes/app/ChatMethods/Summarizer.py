from _includes import config
from ..Composers.PromptComposer import compose_prompt
from ..History.Factory import Factory


class Summarizer:

    @staticmethod
    def summarize_parts() -> None:
        from ..Chat import Chat
        
        summary = Factory.get_summary()
        hash_keys = list(summary.yaml_data.keys())

        for part_index, hash_key in enumerate(hash_keys):
            
            summary_parsed = Factory.get_summary_parsed()
            if summary.yaml_data[hash_key]['summarized']: continue
            
            print(f"Summarizing part {part_index+1}/{summary.count}")
            
            summary_parsed.cut(part_index+1, config.include_previous_part_when_summarizing)
            messages = compose_prompt("Summarize part", summary_parsed, include_introduction=False)
            
            config.model = config.models[config.summary_model]['name']
            result = Chat.stream(None, messages, write_history=False)

            summary.yaml_data[hash_key]['summarized'] = True
            summary.replace_history_part(result, hash_key)

    @staticmethod
    def update_summary() -> None:
        story = Factory.get_story()
        Factory.get_summary().update_from_story_parts(story)

        Summarizer.summarize_parts()
