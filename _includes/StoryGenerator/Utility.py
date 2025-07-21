import yaml, os, re

class Utility:

    @staticmethod
    def read_yaml(file_path):
        if os.path.getsize(file_path) == 0 or not os.path.isfile(file_path):
            return {}
        
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    @staticmethod
    def update_config_from_yaml(config_instance, file_path):
        yaml_data = Utility.read_yaml(file_path)
        
        for key, value in yaml_data.items():
            if hasattr(config_instance, key):
                setattr(config_instance, key, value)

    @staticmethod
    def process_tcp_data(data):
        folder_path, method_name, part_value_str, model_number = data.split(',')
        part_value = int(part_value_str)
        model_number = int(model_number)
        posix_folder_path = os.path.normpath(folder_path).replace('\\', '/')

        return posix_folder_path, method_name, part_value, model_number

    @staticmethod
    def update_config(folder_path):
        from _includes import config

        settings_folder = f'{folder_path}/Settings'
        Utility.update_config_from_yaml(config, f'{settings_folder}/settings.yaml')
        config.folder_path = folder_path + '/'
        config.interrupt_flag = False

        new_abbreviations = Utility.read_yaml(f'{settings_folder}/abbreviations.yaml')
        config.abbreviations.update(new_abbreviations)

        first_prompt = open(f'{settings_folder}/introduction.md', 'r').read()
        config.first_prompt = first_prompt

    @staticmethod
    def reset_history():
        from _includes import config, history, summary, prompts

        history.reset(new_path=config.folder_path + config.history_path)
        summary.reset(new_path=config.folder_path + config.summary_path)
        prompts.reset(new_path=config.folder_path + config.prompts_path)
        
    @staticmethod
    def expand_abbreviations(user_prompt):
        from _includes import config
        
        if config.abbreviations is None:
            return user_prompt

        case_insensitive_mapping = {k.lower(): v for k, v in config.abbreviations.items()}
        # Match words with letters/underscores preceded by @ or whitespace/start, followed by delimiters or end
        pattern = r"(^|\s|#)([a-zA-Z_]+)(?=[:, .?!''\s]|$)"
        
        def replace_match(match):
            prefix = match.group(1)
            abbreviation = match.group(2)
            # For @ prefix, include it in the abbreviation lookup
            if prefix == "#":
                lookup_key = ("#" + abbreviation).lower()
            else:
                lookup_key = abbreviation.lower()
                
            if lookup_key in case_insensitive_mapping:
                if prefix == "#":
                    return case_insensitive_mapping[lookup_key]
                else:
                    return prefix + case_insensitive_mapping[lookup_key]
            return match.group(0)
        
        result = re.sub(pattern, replace_match, user_prompt)
        return result
        