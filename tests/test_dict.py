import pytest

from classyconf.loaders import Dict


def test_basic_config_object(inifile):
    config = Dict({"a": "b"})

    assert repr(config) == "Dict({'a': 'b'})"


def test_skip_missing_key(inifile):
    with pytest.raises(KeyError):
        return Dict({})['some_value']


def test_config_file_parsing(inifile):
    config = Dict({"KEY": "b", "KEY_EMPTY": "", "c": 123})

    assert config["KEY"] == "b"
    assert config["KEY_EMPTY"] == ""
    assert "KEY" in config
    assert "INVALID_KEY" not in config
