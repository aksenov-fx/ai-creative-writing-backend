from pathlib import Path
import yaml
import time
import os


def update_timestamp(path: str, config) -> None:
    time.sleep(config.TIMESTAMP_UPDATE_DELAY)
    current_time = time.time()
    os.utime(path, (current_time, current_time))

def write_file(path: str, content: str, config, mode="a") -> None:
    # Create parent directories if they don't exist
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with open(path, mode, encoding='utf-8') as f: 
                f.write(content)
            break
        except (OSError, IOError) as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(config.RETRY_BASE_DELAY * (2 ** attempt))  # Exponential backoff
    
    if mode == "w": update_timestamp(path, config)

def write_yaml(path: str, content: dict, config) -> None:
    """
    Write a YAML file with the given content.
    
    Converts OrderedDict to regular dict to avoid Python-specific YAML tags.
    """

    if hasattr(content, 'items'):
        content = dict(content)
        
    yaml_data = yaml.dump(content, default_flow_style=False, allow_unicode=True, sort_keys=False)
    write_file(path, yaml_data, config)
