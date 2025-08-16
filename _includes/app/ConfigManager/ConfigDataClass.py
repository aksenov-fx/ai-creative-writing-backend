from dataclasses import dataclass
from pathlib import Path


@dataclass
class ConfigDataClass:
    system_prompt: str
    introduction: str
    variables: dict
    prompts_structure: dict
    abbreviations: str
    translation_language: str

    endpoints: dict
    default_endpoint: str
    endpoint: dict

    models: dict
    default_model: str
    summary_model: str
    model: dict

    temperature: float
    max_tokens: int
    trim_history: bool
    history_prefix: str
    use_summary: bool

    print_messages: bool
    include_reasoning: bool
    print_reasoning: bool
    separator: str
    write_interval: float

    history_path: Path
    summary_yaml_path: Path
    summary_md_path: Path
    prompts_path: Path
    folder_path: Path

    include_previous_part_when_summarizing: bool
    include_previous_part_when_rewriting: bool

    port: int
    interrupt_flag: bool
    debug: bool

    # Chat settings
    splitter: str
    add_header: bool
    chat_with_story: bool
    include_file: str
