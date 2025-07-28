import yaml, os, re, json

class Utility:

    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def read_yaml(file_path):
        if os.path.getsize(file_path) == 0 or not os.path.isfile(file_path):
            return {}
        
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    def parse_frontmatter(file_path):
        content = Utility.read_file(file_path)
        content = content.split('---\n')[1]
        return yaml.safe_load(content)

    @staticmethod
    def print_with_newlines(obj):
        json_str = json.dumps(obj, indent=2, ensure_ascii=False)
        formatted_str = json_str.replace('\\n', '\n')
        print(formatted_str)

    @staticmethod
    def process_tcp_data(data):
        folder_path, method_name, part_value_str, model_number = data.split(',')
        part_value = int(part_value_str)
        model_number = int(model_number)
        posix_folder_path = os.path.normpath(folder_path).replace('\\', '/')

        return posix_folder_path, method_name, part_value, model_number

    @staticmethod
    def update_config(folder_path):
        from ..config import config, default_config, abbreviations

        settings_folder = folder_path + '/Settings/'

        # Read values
        default_values =    default_config.copy()
        new_values =        Utility.parse_frontmatter(settings_folder + 'settings.md')
        new_abbreviations = Utility.parse_frontmatter(settings_folder + 'abbreviations.md')
        first_prompt =      Utility.read_file(settings_folder + 'introduction.md')

        # Preserve values
        keys_to_preserve = ['debug', 'user_prompt', 'model', 'endpoint']
        for key in keys_to_preserve: default_values.pop(key)

        default_values.update(new_values)

        # Update values
        for key, value in default_values.items():
            if hasattr(config, key):
                setattr(config, key, value)

        config.abbreviations = abbreviations
        config.abbreviations.update(new_abbreviations)
        config.folder_path = folder_path + '/'
        config.interrupt_flag = False
        config.first_prompt = first_prompt

    @staticmethod
    def reset_history():
        from _includes import config, story, summary, prompts, story_parsed, summary_parsed

        folder = config.folder_path

        story.refresh          (folder + config.history_path)
        summary.refresh        (folder + config.summary_path)
        prompts.refresh        (folder + config.prompts_path)

        story_parsed.refresh   (folder + config.history_path)
        summary_parsed.refresh (folder + config.summary_path)
        
    @staticmethod
    def set_prompt(part_value):
        from _includes import config, prompts
        prompts.refresh()

        part_value -= 1
        prompts.fix_separator()
        config.user_prompt = prompts.return_part(part_value)

        prompt_to_print = Utility.expand_abbreviations(config.user_prompt)
        print(prompt_to_print)

    @staticmethod
    def remove_last_response():
        from _includes import story
        story.refresh()
        story.remove_last_response()

    @staticmethod
    def expand_abbreviations(user_prompt):
        from _includes import config
        
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

    def write_diff(path, old_content, new_content):
        import mmap
        
        # Update content in memory
        original_bytes = old_content.encode()
        new_bytes = new_content.encode()
        
        # Get file size for mapping
        file_size = os.path.getsize(path)
        if len(new_bytes) > file_size:
            # Resize file if new content is larger
            with open(path, "ab") as f:
                f.write(b'\0' * (len(new_bytes) - file_size))
        
        # Memory-map the file and update changed portions only
        with open(path, "r+b") as f:
            # Create memory mapping
            mm = mmap.mmap(f.fileno(), len(new_bytes))
            
            # Find and update changed regions
            pos = 0
            while pos < len(new_bytes):
                # Find next difference
                chunk_size = 4096  # Process in chunks
                end = min(pos + chunk_size, len(new_bytes))
                
                if pos >= len(original_bytes) or original_bytes[pos:end] != new_bytes[pos:end]:
                    # Write only the changed chunk
                    mm[pos:end] = new_bytes[pos:end]
                
                pos = end
                
            # Resize if new content is smaller
            if len(new_bytes) < file_size:
                mm.resize(len(new_bytes))
            
            mm.flush()
            mm.close()
