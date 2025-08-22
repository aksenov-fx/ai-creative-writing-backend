import re

from _includes import config
from .ApiComposer import ApiComposer

def validate(include_introduction: bool, validate_user_prompt: bool = True) -> None:

    introduction_error = "config.introduction is not set. Please set it before beginning a story."
    user_prompt_error = "User prompt is not set. Please set it before writing a scene."

    if include_introduction and not config.introduction:
        raise ValueError(introduction_error)

    if validate_user_prompt and not config.variables['#user_prompt']:
        raise ValueError(user_prompt_error)
    
def validate_part_number(parts_count, part_number: int) -> None:
    if parts_count < part_number:
        raise ValueError("Story has less parts than the specified part number")

def compose_prompt(method: str, history_parsed, include_introduction = True):

    if method == "Summarize part":
        validate(include_introduction, validate_user_prompt=False)
    else:
        validate(include_introduction)

    # Prepare user prompt
    prompt_structure = config.prompts_structure[method] # Get structure defined in prompts_structure.yaml
    prompt = expand_abbreviations(prompt_structure, config.variables) # Compose prompt according to structure

    # Prepare history
    if config.trim_history: history_parsed.trim_content()
    history = f"{config.history_prefix}\n{history_parsed.parsed}" if history_parsed.parsed else ""

    # Prepare introduction
    introduction = expand_abbreviations(config.introduction)
    introduction = f"{introduction}\n\n" if include_introduction else ""

    # Combine introduction, history and user prompt
    combined_prompt = f"{introduction}{history.strip()}\n\n{prompt}\n\n{history_parsed.part_number_content}"
    combined_prompt = combined_prompt.replace("\n\n\n", "\n\n").strip()

    messages = ApiComposer.compose_messages(combined_prompt, history_parsed.assistant_response)
    
    return messages

def compose_helper_prompt(prompt_key: str, selected_text: str) -> list:
    prompt_structure = config.prompts_structure[prompt_key]
    prompt = expand_abbreviations(prompt_structure, config.variables)

    if prompt_key == 'Translate':
        prompt = f"{prompt.strip()} {config.translation_language}:"
    
    combined_prompt = f"{prompt.strip()}\n{selected_text}"
    return ApiComposer.compose_messages(combined_prompt, None)

def expand_abbreviations(text: str, abbreviations: dict = None) -> str:
    r"""
    Replaces abbreviations in the text with their corresponding values.

    This function is case-insensitive and matches text
    preceded by # or whitespace/newline, followed by delimiters or end.
    The delimiters are: :, ., ?, !, ', ', \s (whitespace), $ (end of string).

    The method is used in two ways:
    - to expand abbreviations from config.abbreviations for user prompt and introduction.
    - to expand variables from config.variables in config.prompts_structure.

    Args:
        text (str): The text to expand abbreviations in.
        abbreviations (dict, optional): The abbreviations to use. Defaults to None.

    Returns:
        str: The text with abbreviations expanded.
    """

    from _includes import config

    if not abbreviations: abbreviations = config.abbreviations
    if not abbreviations or not text: return text
    
    case_insensitive_mapping = {k.lower(): v for k, v in abbreviations.items()}
    pattern = r"(^|\s|#)([a-zA-Z_]+)(?=[:, .?!''\s]|$)"
    
    def replace_match(match):
        prefix = match.group(1)
        abbreviation = match.group(2)
        
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
    
    result = re.sub(pattern, replace_match, text)
    return result