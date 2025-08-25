import pytest


from tests._logic.chat_test import chat_test
from tests._logic.ConfigManager.ParamManager import load_params

params = load_params('Chat', 'Chatter')

@pytest.mark.parametrize("app_config,expected_content,callback,class_name,should_pass,arg,overrides", params)
def test_module(app_config, expected_content, callback, class_name, should_pass, arg, overrides):
    chat_test(app_config, expected_content, callback, class_name, should_pass, arg, overrides)