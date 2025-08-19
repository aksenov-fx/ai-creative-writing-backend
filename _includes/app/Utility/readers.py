import os
from pathlib import Path
import yaml
from importlib import resources

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

def read_yaml(file_path: str, convert_keys_to_snake_case: bool = False) -> dict:
    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        return {}
    
    yaml_data = read_file(file_path)
    if file_path.endswith('.md'): yaml_data = yaml_data.split('---\n')[1]
    yaml_data = yaml.safe_load(yaml_data)
    
    if convert_keys_to_snake_case:
        yaml_data = {k.lower().replace(" ", "_"): v for k, v in yaml_data.items()}
    
    return yaml_data

def read_instructions(instructions: str):
    """
    Read custom instructions from a file.
    
    If the custom instructions section in md file has text like {Questions},
    it will look for a file named Questions.md in the _instructions directory.
    Otherwise - return the original section text.
    """
    if not instructions.startswith("{"):
        return instructions
    
    instructions_file = instructions.replace('{', '').replace('}', '')
    instructions_file += '.md'

    with resources.files('_includes.settings._instructions').joinpath(instructions_file).open('r') as file:
        content = file.read()
        return content
    