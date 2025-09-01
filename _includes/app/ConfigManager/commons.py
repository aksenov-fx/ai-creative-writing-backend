from .. import Utility


def get_model(config_dict):
    """
    Gets the model name from config by number.
    If input is not a number, returns the model name as is.

    1 -> First model
    "deepseek" -> "deepseek"

    Used by get_chat_config() and story_config.load_config()
    """

    model = config_dict['model']
    
    if not model:
        return config_dict['models'][config_dict['default_model']]['name']
    
    try:
        model_number = int(model)
        return list(config_dict['models'].values())[model_number - 1]['name']
    except ValueError:
        return model


def get_endpoint(config_dict):
    endpoint = config_dict['endpoints'][config_dict['default_endpoint']]
    endpoint['api_key'] = Utility.read_file(endpoint['api_key_file']).strip()
    return endpoint
