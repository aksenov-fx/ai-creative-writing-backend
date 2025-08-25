from dataclasses import dataclass
from pathlib import Path


@dataclass
class ConfigDataClass:
    # Prompt variables
    system_prompt: str
    introduction: str
    variables: dict
    prompts_structure: dict
    abbreviations: str
    translation_language: str
    history_prefix: str

    # Story parsing settings
    separator: str

    # Endpoints settings
    endpoints: dict
    default_endpoint: str
    endpoint: dict

    # Models settings
    models: dict
    default_model: str
    summary_model: str
    model: dict

    # Context length settings
    max_tokens: int
    trim_history: bool
    use_summary: bool
    include_previous_part_when_summarizing: bool
    include_previous_part_when_rewriting: bool

    # API settings
    temperature: float

    # Output settings
    print_messages: bool
    include_reasoning: bool
    print_reasoning: bool

    # Paths
    history_path: Path
    summary_yaml_path: Path
    summary_md_path: Path
    prompts_path: Path
    folder_path: Path
    settings_folder: Path

    # Runtime flags
    interrupt_flag: bool
    debug: bool

    # Chat settings that are not used in story mode
    custom_instructions_folder: Path
    splitter: str
    add_header: bool
    chat_with_story: bool
    include_file: str

    # Constants
    WRITE_INTERVAL: float
    PORT: int
    TOKEN_ESTIMATION_DIVISOR: int
    BUFFER_SIZE: int
    TIMESTAMP_UPDATE_DELAY: float
    RETRY_BASE_DELAY: float