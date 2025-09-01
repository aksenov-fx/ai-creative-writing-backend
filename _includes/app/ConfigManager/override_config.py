from contextlib import contextmanager
from typing import Any

from .ConfigDataClass import ConfigDataClass


@contextmanager
def override_config(config: ConfigDataClass, **overrides: Any):
    """
    Changes config values temporarily and then sets them back.

    Used by dispatcher.
    """
    
    original_values = {}

    for key, value in overrides.items():
        if hasattr(config, key):
            original_values[key] = getattr(config, key)
            setattr(config, key, value)
    
    try:
        yield config
        
    finally:
        for key, value in original_values.items():
            setattr(config, key, value)
