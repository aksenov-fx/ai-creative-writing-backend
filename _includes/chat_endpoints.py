# --- Endpoint and model --- #

# Multiple endpoints and models can be defined

def get_api_key(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

# ---                    --- #

endpoint = {
    'url': 'https://openrouter.ai/api/v1',
    'api_key': get_api_key("./_includes/api_key.txt")
}

model = 'deepseek/deepseek-r1:free'

# ---                    --- #

