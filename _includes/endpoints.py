import yaml

def get_api_key(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

def load_models_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        models = yaml.safe_load(file)
    return models

endpoint = {
    'url': 'https://openrouter.ai/api/v1',
    'api_key': get_api_key("./_includes/api_key.txt")
}

models = load_models_from_file('_includes/endpoints.yaml')