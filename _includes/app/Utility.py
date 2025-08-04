import os, re, json, shutil
from pathlib import Path

class Utility:

    @staticmethod
    def read_file(file_path):
        path = Path(file_path)
        
        # If the exact file exists, use it
        if path.exists():
            return path.read_text(encoding='utf-8')
        
        # Case-insensitive search
        directory = path.parent if path.parent != Path('.') else Path.cwd()
        target_name = path.name.lower()
        
        for existing_file in directory.iterdir():
            if existing_file.is_file() and existing_file.name.lower() == target_name:
                return existing_file.read_text(encoding='utf-8')
        
        return ""

    @staticmethod
    def print_with_newlines(obj):
        json_str = json.dumps(obj, indent=2, ensure_ascii=False)
        formatted_str = json_str.replace('\\n', '\n')
        print(formatted_str)

    @staticmethod
    def process_tcp_data(data):
        folder_path, method_name, part_value_str = data.split(',')
        part_value = int(part_value_str)
        posix_folder_path = os.path.normpath(folder_path).replace('\\', '/')

        return posix_folder_path, method_name, part_value

    @staticmethod
    def clear_screen():
        os.system('clear' if os.name == 'posix' else 'cls')

    @staticmethod
    def copy_file(path, new_path):
        if os.path.exists(new_path):
            raise FileExistsError(f"Summary already exists. Please delete it before creating a new one.")
        shutil.copy(path, new_path)

    @staticmethod
    def set_prompt(part_value, abbreviations):
        from _includes import config
        from .Factory import Factory

        prompts = Factory.get_prompts()

        part_value -= 1
        prompts.fix_separator()
        config.variables['#user_prompt'] = prompts.return_part(part_value)

        prompt_to_print = Utility.expand_abbreviations(config.variables['#user_prompt'], abbreviations)
        print(prompt_to_print)

    @staticmethod
    def expand_abbreviations(text, abbreviations=None):
        from _includes import config

        if not abbreviations: abbreviations = config.abbreviations
        if not abbreviations or not text: return text
            
        case_insensitive_mapping = {k.lower(): v for k, v in abbreviations.items()}
        # Match words with letters/underscores preceded by # or whitespace/start, followed by delimiters or end
        pattern = r"(^|\s|#)([a-zA-Z_]+)(?=[:, .?!''\s]|$)"
        
        def replace_match(match):
            prefix = match.group(1)
            abbreviation = match.group(2)
            # For # prefix, include it in the abbreviation lookup
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
        
        result = re.sub(pattern, replace_match, text)
        return result

    # The method is not used yet
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
