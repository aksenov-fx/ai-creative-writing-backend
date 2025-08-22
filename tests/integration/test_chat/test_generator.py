import pytest

from tests._logic.chat_test import chat_test
from tests._logic.TestsConfig import generator_params

@pytest.mark.parametrize("prompt_type,story_file,callback,should_pass,arg", generator_params)
def test_module(prompt_type, story_file, callback, should_pass, arg):
    chat_test(prompt_type, story_file, callback, "Generator", should_pass, arg)