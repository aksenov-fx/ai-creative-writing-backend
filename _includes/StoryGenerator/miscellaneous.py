from ..chat_settings import config

def expand_abbreviations(user_prompt):
    import re
    
    if config.abbreviations is None:
        return user_prompt

    case_insensitive_mapping = {k.lower(): v for k, v in config.abbreviations.items()}
    pattern = r"\b([a-zA-Z]+)(?=[:, .?!'])"
    
    def replace_match(match):
        abbreviation = match.group(1)
        if abbreviation.lower() in case_insensitive_mapping:
            return case_insensitive_mapping[abbreviation.lower()]
        return abbreviation
    
    result = re.sub(pattern, replace_match, user_prompt)
    return result
