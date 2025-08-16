from ..Utility.Utility import Utility


def get_model(config_dict):

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
