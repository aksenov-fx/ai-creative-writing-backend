import os
from dataclasses import dataclass

from tests._logic.utils import read_yaml

from _includes.app.Chat.Generator import Generator
from _includes.app.Chat.Changer import Changer
from _includes.app.Chat.Summarizer import Summarizer
from _includes.app.Chat.Helpers import Helpers

@dataclass
class TestsConfig:
    temp_dir: str
    originals_dir: str
    story_folder: str
    story_folder_path: str

def get_tests_config(path: str):
    yaml_data = read_yaml(path)
    tests_config = TestsConfig(**yaml_data)

    tests_config.story_folder_path = os.path.join(tests_config.temp_dir, tests_config.story_folder)

    return tests_config

generator_params = [

    ["Write scene",          "Story empty.md",     Generator.write_scene,       True],
    ["Write scene",          "Story.md",           Generator.write_scene,       True],

    ["Custom prompt",        "Story empty.md",     Generator.custom_prompt,     True],
    ["Custom prompt",        "Story.md",           Generator.custom_prompt,     True],
    
    ["Regenerate",           "Story.md",           Generator.regenerate,        True],
    ["Regenerate",           "Story empty.md",     Generator.regenerate,        False],

    ["Add part",             "Story.md",           Generator.add_part,          True],
    ["Add part",             "Story empty.md",     Generator.add_part,          False],

    ["Continue response",    "Story.md",           Generator.continue_response, True],
    ["Continue response",    "Story empty.md",     Generator.continue_response, False],

]

changer_params = [
    ["Change part",          "Story.md",           Changer.change_part,         True],
    ["Change part",          "Story empty.md",     Changer.change_part,         False],
]

summarizer_params = [
    ["Summarize part",       "Story.md",           Summarizer.summarize_part,   True],
]

helper_params = [
    ["Rewrite selection",    "Story empty.md",     Helpers.rewrite_selection,   True],
    ["Translate",            "Story empty.md",     Helpers.translate,           True],
    ["Explain",              "Story empty.md",     Helpers.explain,             True],
]
