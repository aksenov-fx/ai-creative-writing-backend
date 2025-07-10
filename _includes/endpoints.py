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

models = {
    'Deepseek R1': {
        'name': 'deepseek/deepseek-r1:free',
        'outputs_thinking': True
    },

    'Qwen 72b': {
        'name': 'qwen/qwen-2.5-72b-instruct',
        'outputs_thinking': False
    },

    'Deepseek V3': {
        'name': 'deepseek/deepseek-chat-v3-0324:free',
        'outputs_thinking': False
    }
}

# ---                    --- #

