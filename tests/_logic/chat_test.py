import pytest
from unittest.mock import patch

from tests._logic.utils import read_expected_file
from tests._logic.utils import setup_temp_folder
from tests._logic.TestsConfig import get_tests_config

from _includes.app.ConfigManager import override_config
from _includes.app.ConfigManager import get_story_config
from _includes import config

def run_setup():
    tests_conf = get_tests_config("tests/_settings/Settings.yaml")
    setup_temp_folder(tests_conf)
    return tests_conf

def chat_test(prompt_type, story_file, callback, module, should_pass):

    setup = run_setup()

    expected_content = read_expected_file(setup.story_folder_path, prompt_type, story_file)
    expected_messages = [{"role": "user", "content": expected_content}]

    new_config = get_story_config(setup.story_folder_path, config)
    new_config['history_path'] = story_file
    argument = 4
    
    if not should_pass:

        with pytest.raises(ValueError) as exc_info:
            with patch(f'_includes.app.Chat.{module}.stream') as mock_stream:
                with override_config(config, **new_config):
                    callback(argument)

        assert str(exc_info.value) == expected_content.strip()

    if should_pass:

        with patch(f'_includes.app.Chat.{module}.stream') as mock_stream:
            with override_config(config, **new_config):
                callback(argument)
    
        args, kwargs = mock_stream.call_args
        story_obj, messages = args
        
        mock_stream.assert_called_once()
        assert messages == expected_messages