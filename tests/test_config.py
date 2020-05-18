import os

import pytest

from classyconf.configuration import Configuration
from classyconf.exceptions import UnknownConfiguration
from classyconf.loaders import EnvFile, Environment, IniFile


def test_basic_config(env_config, ini_config):
    os.environ["ENVVAR"] = "Environment Variable Value"
    config = Configuration()
    assert repr(config).startswith("Configuration(loaders=[")
    assert config("ENVVAR") == "Environment Variable Value"
    assert len(config.loaders) == 1  # Environment
    del os.environ["ENVVAR"]


def test_customized_loaders(env_config, ini_config):
    os.environ["ENVVAR"] = "Environment Variable Value"
    os.environ["ENVVAR2"] = "Foo"
    loaders = [EnvFile(env_config), Environment(), IniFile(ini_config)]
    config = Configuration(loaders=loaders)
    assert config("ENVVAR") == "Must be overrided"
    assert config("ENVVAR2") == "Foo"
    assert config("ENVFILE") == "Environment File Value"
    assert config("INIFILE") == "INI File Value"
    assert len(config.loaders) == 3
    del os.environ["ENVVAR"]
    del os.environ["ENVVAR2"]


def test_from_import_basic_config():
    from classyconf import config

    assert isinstance(config, Configuration)


def test_config_default_values():
    config = Configuration()
    assert config("DEFAULT", default="Default Value") == "Default Value"


def test_config_cast_value():
    os.environ["INTEGER"] = "42"
    config = Configuration()
    assert config("INTEGER", cast=int) == 42


def test_fail_invalid_cast_type():
    os.environ["INTEGER"] = "42"
    config = Configuration()
    with pytest.raises(TypeError):
        config("INTEGER", cast="not callable")


def test_fail_unknown_config_without_default_value():
    os.environ["ENVVAR"] = "Environment Variable Value"
    config = Configuration()
    with pytest.raises(UnknownConfiguration):
        config("UNKNOWN")


def test_none_as_default_value():
    config = Configuration()
    assert config("UNKNOWN", default=None) is None


def test_none_default_value_identity_cast():
    os.environ["DEFAULT"] = "1"
    config = Configuration()
    assert config("DEFAULT", default=None) == "1"


def test_boolean_as_default_value():
    os.environ["BOOLEAN"] = "1"
    config = Configuration()
    assert config("BOOLEAN", default=False) == True


def test_int_as_default_value():
    os.environ["INT"] = "1"
    config = Configuration()
    assert config("INT", default=0) == 1


def test_str_as_default_value():
    os.environ["STR"] = "1"
    config = Configuration()
    assert config("STR", default="foo") == "1"
