import pytest

from tests._logic.chat_test import chat_test
from tests._logic.TestsConfig import summarizer_params

@pytest.mark.parametrize("prompt_type,story_file,callback,should_pass", summarizer_params)
def test_module(prompt_type, story_file, callback, should_pass):
    chat_test(prompt_type, story_file, callback, "Summarizer", should_pass)