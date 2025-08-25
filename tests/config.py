from ._logic.ConfigManager.commons import get_tests_config
from ._logic.utils import setup_temp_folder

tests_config = get_tests_config("tests/_settings/Settings.yaml")
setup_temp_folder(tests_config)