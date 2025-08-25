from dataclasses import dataclass

@dataclass
class TestsConfig:
    temp_dir:          str
    originals_dir:     str
    params_dir:        str

    story_folder:      str
    story_folder_path: str