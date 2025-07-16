import yaml

def load_vars(file_path='_includes/vars.yaml'):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

vars = load_vars()