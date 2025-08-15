import re

from _includes import config
from .ApiComposer import ApiComposer
from ..History.History import HistoryParser

def validate(include_introduction):

    introduction_error = "config.introduction is not set. Please set it before beginning a story."
    user_prompt_error = "User prompt is not set. Please set it before writing a scene."

    if include_introduction and not config.introduction:
        raise ValueError(introduction_error)

    if not config.variables['#user_prompt']:
        raise ValueError(user_prompt_error)
    
def compose_prompt(method: str, history_parsed: HistoryParser, include_introduction = True):

    validate(include_introduction)

    # Prepare user prompt
    prompt_structure = config.prompts_structure[method] # Get structure defined in prompts_structure.yaml
    prompt = expand_abbreviations(prompt_structure, config.variables) # Compose prompt according to structure

    # Prepare history
    if config.trim_history: history_parsed.trim_content()
    history = config.history_prefix + "\n" + history_parsed.parsed if history_parsed.parsed else ""

    # Prepare introduction
    introduction = expand_abbreviations(config.introduction)
    introduction += "\n\n" if include_introduction else ""

    # Combine introduction, history and user prompt
    combined_prompt = introduction + history + "\n\n" + prompt + "\n\n" + history_parsed.part_number_content
    combined_prompt = combined_prompt.replace("\n\n\n", "\n\n").strip()

    messages = ApiComposer.compose_messages(combined_prompt, history_parsed.assistant_response)
    
    return messages

def compose_helper_prompt(prompt_key: str, selected_text: str) -> list:
    prompt_structure = config.prompts_structure[prompt_key]
    prompt = expand_abbreviations(prompt_structure, config.variables)

    if prompt_key == 'Translate':
        prompt = prompt.strip() + " " + config.translation_language + ":"
    
    combined_prompt = prompt.strip() + "\n" + selected_text
    return ApiComposer.compose_messages(combined_prompt, None)

def set_prompt(part_value, abbreviations):
    from ..History.Factory import Factory

    prompts = Factory.get_prompts()

    prompt = prompts.return_part(part_value -1)
    prompt = expand_abbreviations(prompt, abbreviations)
    config.variables['#user_prompt'] = prompt
    print(prompt)

    prompts.fix_separator()

def expand_abbreviations(text, abbreviations=None):
    from _includes import config

    if not abbreviations: abbreviations = config.abbreviations
    if not abbreviations or not text: return text
    
    case_insensitive_mapping = {k.lower(): v for k, v in abbreviations.items()}
    # Match words with letters/underscores preceded by # or whitespace/start, followed by delimiters or end
    pattern = r"(^|\s|#)([a-zA-Z_]+)(?=[:, .?!''\s]|$)"
    
    def replace_match(match):
        prefix = match.group(1)
        abbreviation = match.group(2)
        
        # For # prefix, include it in the abbreviation lookup
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