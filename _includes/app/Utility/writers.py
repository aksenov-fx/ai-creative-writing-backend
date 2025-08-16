from pathlib import Path
import yaml
import time

def write_file(path: str, content: str) -> None:
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

def write_yaml(path: str, content: dict) -> None:
    # Convert OrderedDict to regular dict to avoid Python-specific YAML tags
    if hasattr(content, 'items'):
        content = dict(content)
    yaml_data = yaml.dump(content, default_flow_style=False, allow_unicode=True, sort_keys=False)
    write_file(path, yaml_data)
