import os, json, hashlib, time
from importlib import resources
from pathlib import Path
import yaml

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
    def write_file(path, content):
        # Create parent directories if they don't exist
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with open(path, 'w', encoding='utf-8') as f: 
                    f.write(content)
                break
            except (OSError, IOError) as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(0.1 * (2 ** attempt))  # Exponential backoff

    @staticmethod
    def write_yaml(path, content):
        # Convert OrderedDict to regular dict to avoid Python-specific YAML tags
        if hasattr(content, 'items'):
            content = dict(content)
        yaml_data = yaml.dump(content, default_flow_style=False, allow_unicode=True, sort_keys=False)
        Utility.write_file(path, yaml_data)

    @staticmethod
    def read_yaml(file_path, convert_keys_to_snake_case = False):
        if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
            return {}
        
        yaml_data = Utility.read_file(file_path)
        if file_path.endswith('.md'): yaml_data = yaml_data.split('---\n')[1]
        yaml_data = yaml.safe_load(yaml_data)
        
        if convert_keys_to_snake_case:
            yaml_data = {k.lower().replace(" ", "_"): v for k, v in yaml_data.items()}
        
        return yaml_data

    @staticmethod
    def calculate_hash(text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    @staticmethod
    def read_instructions(instructions: str):
        if not instructions.startswith("{"):
            return instructions
        
        instructions_file = instructions.replace('{', '').replace('}', '')
        instructions_file += '.md'

        with resources.files('_includes.settings._instructions').joinpath(instructions_file).open('r') as file:
            content = file.read()
            return content
        
    @staticmethod
    def print_with_newlines(obj):
        json_str = json.dumps(obj, indent=2, ensure_ascii=False)
        formatted_str = json_str.replace('\\n', '\n')
        print(formatted_str)