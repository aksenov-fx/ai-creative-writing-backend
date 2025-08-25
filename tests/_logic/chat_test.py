import pytest
from unittest.mock import patch

from _includes import config

from _includes.app.ConfigManager import override_config

def chat_test(app_config, expected_content, callback, module, should_pass, argument, overrides):

    if not should_pass:

        with pytest.raises(ValueError) as exc_info:
            with patch(f'_includes.app.Chat.{module}.stream') as mock_stream:
                with override_config(config, **app_config, **overrides):
                    callback(argument)

        assert str(exc_info.value) == expected_content

    if should_pass:

        if isinstance(expected_content, str):
            expected_content = [{"role": "user", "content": expected_content}]

        with patch(f'_includes.app.Chat.{module}.stream') as mock_stream:
            with override_config(config, **app_config, **overrides):
                callback(argument)
    
        args, kwargs = mock_stream.call_args
        story_obj, messages = args
        
        mock_stream.assert_called_once()
        assert messages == expected_content