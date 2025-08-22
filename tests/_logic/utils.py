import os
import shutil
import stat
from pathlib import Path
import yaml

def read_file(file_path: str) -> str:
    path = Path(file_path)
    
    try:
        return path.read_text(encoding='utf-8')
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

def read_yaml(file_path: str) -> dict:

    try:
        yaml_data = read_file(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    
    yaml_data = yaml.safe_load(yaml_data)
    
    return yaml_data

def setup_temp_folder(tests_config):
    if os.path.exists(tests_config.temp_dir): 
        shutil.rmtree(tests_config.temp_dir, onerror=handle_remove_readonly)
    shutil.copytree(tests_config.originals_dir, tests_config.temp_dir)

def handle_remove_readonly(func, path, exc):
    if os.path.exists(path):
        os.chmod(path, stat.S_IWRITE)
        func(path)

def read_expected_file(story_folder_path: str, prompt_type: str, file_name: str) -> str:

    file_path = os.path.join(story_folder_path, "Expected", prompt_type, file_name)

    try:
        return read_file(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
