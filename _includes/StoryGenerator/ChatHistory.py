import os, re
from .ApiComposer import ApiComposer
from _includes import config

class ChatHistory:
    
    @staticmethod
    # Code like def read(path=config.history_path) works incorrectly,
    # because path value will not change if history_path changes,
    # hence this method
    def get_path(path) -> str: 
        return path or config.history_path

    @staticmethod
    def read(path=None) -> str:
        path = ChatHistory.get_path(path)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            return content or ""
    
    @staticmethod
    def write_history(content: str, path=None) -> None:
        path = ChatHistory.get_path(path)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def append_history(content: str, path=None) -> None:
        path = ChatHistory.get_path(path)
        with open(path, 'a', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def has_separator(content=None, path=None) -> bool:
        if content is None:
            content = ChatHistory.read(path)
        lines = content.splitlines()
        return any(line.strip() == config.separator for line in lines)
    
    @staticmethod
    def insert_separator(path=None):
        history_content = ChatHistory.read(path)
        lines = history_content.strip().splitlines()
        if lines[-1] != config.separator:
            ChatHistory.append_history(f"\n\n{config.separator}\n\n", path)

    @staticmethod
    def count_parts(content=None, path=None) -> int:
        if content is None:
            content = ChatHistory.read(path)
        lines = content.splitlines()
        return sum(1 for line in lines if line.strip() == config.separator)

    @staticmethod
    def merge_story_with_summary():

        history_content = ChatHistory.read(config.history_path)

        if not os.path.exists(config.summary_path):
            return history_content
        
        summary_content = ChatHistory.read(config.summary_path)

        history_split = history_content.split(config.separator)
        summary_split = summary_content.split(config.separator)
        
        number_of_history_parts = ChatHistory.count_parts(history_content)
        number_of_summary_parts = ChatHistory.count_parts(summary_content)

        # Keep the last part unsummarized
        if number_of_history_parts == number_of_summary_parts:
            summary_content = config.separator.join(summary_split[:-2])
            number_of_summary_parts = ChatHistory.count_parts(summary_content)
        
        history_content = config.separator.join(history_split[number_of_summary_parts:])
        history_content = summary_content + history_content

        return history_content

    @staticmethod
    def remove_last_response() -> None:
        config.interrupt_flag = True

        content = ChatHistory.read().strip()
        lines = content.splitlines()

        # Remove last line if last line is a separator
        if lines and lines[-1] == config.separator:
            lines[-1] = ''
            content = '\n'.join(lines).strip()

        if not ChatHistory.has_separator(content):
            ChatHistory.write_history('')
            return

        #Remove text after the last separator
        if (pos := content.rfind(config.separator)) != -1:
            ChatHistory.write_history(content[:pos + len(config.separator)] + '\n\n')

    @staticmethod
    def parse_assistant_response(history_content) -> tuple[str, str]:
        lines = history_content.splitlines()

        has_separator = ChatHistory.has_separator(history_content)
        if not has_separator or lines[-1].strip() == config.separator:
            return history_content, None
        
        parts = history_content.split(f'\n{config.separator}\n')
        history_content = f'\n{config.separator}\n'.join(parts[:-1]).strip()
        assistant_response = parts[-1].strip()
        return history_content, assistant_response

    @staticmethod
    def remove_reasoning_header(history_content: str) -> str:
        return '\n'.join(
            line 
            for line in history_content.splitlines() 
            if line != config.reasoning_header).strip()
    
    @staticmethod
    def remove_reasoning_tokens(history_content: str) -> str:
        import re
    
        pattern = r'<think>.*?</think>'

        cleaned_content = re.sub(pattern, '', history_content, flags=re.DOTALL)
        cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)
        
        return cleaned_content

    @staticmethod
    def format_history(history_content: str) -> str:

        cleaned_content = '\n\n'.join(
            block.strip() 
            for block in history_content.split(config.separator) 
            if block.strip()
        )

        return cleaned_content
    
    @staticmethod
    def replace_history_part(new_part, path=None) -> str:
        history_content = ChatHistory.read(path)
        history_split = history_content.split(config.separator)
        new_part = '\n\n' + new_part + '\n\n'

        splitter = '</think>'
        if splitter in history_split[config.part_number-1]:
            think_part, _ = history_split[config.part_number-1].split(splitter, 1)
            history_split[config.part_number-1] = think_part + splitter + new_part
        else:
            history_split[config.part_number-1] = new_part
            
        history_content = config.separator.join(history_split)

        ChatHistory.write_history(history_content, path)

    @staticmethod
    def add_part(new_part, path=None) -> str:
        history_content = ChatHistory.read(path)
        history_split = history_content.split(config.separator)
        new_part = '\n\n' + new_part + '\n\n'

        history_split.insert(config.part_number, new_part)
        history_content = config.separator.join(history_split)

        ChatHistory.write_history(history_content, path)
        
    @staticmethod
    def remove_reasoning():
        history_content = ChatHistory.read()
        history_content = ChatHistory.remove_reasoning_header(history_content)
        history_content = ChatHistory.remove_reasoning_tokens(history_content)
        history_content = history_content + '\n\n'
        ChatHistory.write_history(history_content)

    @staticmethod
    def expand_abbreviations(user_prompt):
        
        if config.abbreviations is None:
            return user_prompt

        case_insensitive_mapping = {k.lower(): v for k, v in config.abbreviations.items()}
        # Match words with letters/underscores preceded by @ or whitespace/start, followed by delimiters or end
        pattern = r"(^|\s|#)([a-zA-Z_]+)(?=[:, .?!''\s]|$)"
        
        def replace_match(match):
            prefix = match.group(1)
            abbreviation = match.group(2)
            # For @ prefix, include it in the abbreviation lookup
            if prefix == "#":
                lookup_key = ("#" + abbreviation).lower()
            else:
                lookup_key = abbreviation.lower()
                
            if lookup_key in case_insensitive_mapping:
                if prefix == "#":
                    return case_insensitive_mapping[lookup_key]
                else:
                    return prefix + case_insensitive_mapping[lookup_key]
            return match.group(0)
        
        result = re.sub(pattern, replace_match, user_prompt)
        return result

    @staticmethod
    def set_prompt(path, part_number):
        path = path + '/prompts.md'
        promts = ChatHistory.read(path)
        promts_split = promts.split(config.separator)
        config.user_prompt = promts_split[part_number].strip()
        ChatHistory.insert_separator(path)
    
    @staticmethod
    def process_history(path=None, no_summary: bool = False, cut_history_to_part_number: bool = False, return_previous_part: bool = False):

        part_number_content = ""

        # Read history
        if config.use_summary and not no_summary:
            history_content = ChatHistory.merge_story_with_summary()
        else:
            history_content = ChatHistory.read(path)

        # Remove '### Reasoning' headers
        history_content = ChatHistory.remove_reasoning_header(history_content)

        # Parse assistant response to continue last response
        history_content, assistant_response = ChatHistory.parse_assistant_response(history_content)

        # Remove reasoning tokens
        history_content = ChatHistory.remove_reasoning_tokens(history_content)

        # Cut history
        if cut_history_to_part_number:
            history_split = history_content.split(config.separator)
            history_content = config.separator.join(history_split[:config.part_number-1])
            part_number_content = history_split[config.part_number-1]

        if return_previous_part: history_content = history_split[config.part_number-2]

        # Remove separators and extra empyty lines
        history_content = ChatHistory.format_history(history_content)

        # Exclude first paragraphs to match input length with max_tokens
        history_content = ApiComposer.trim_content(history_content, config.max_tokens)

        return history_content, part_number_content, assistant_response