import os

import pytest
from classyconf.configuration import Configuration, Value, getconf
from classyconf.exceptions import UnknownConfiguration
from classyconf.loaders import EnvFile, Environment, IniFile


class BasicClassyConf(Configuration):
    ENVVAR = Value(help="Just a test.")
    ENVVAR2 = Value()


class ChildClassyConf(BasicClassyConf):
    class Meta:
        loaders = []


def test_basic_config(env_config, ini_config):
    os.environ["ENVVAR"] = "Environment Variable Value"
    config = BasicClassyConf()
    assert repr(config).startswith("BasicClassyConf(loaders=[")
    assert config["ENVVAR"] == "Environment Variable Value"
    assert config.ENVVAR == "Environment Variable Value"
    assert len(config._loaders) == 1  # Environment
    del os.environ["ENVVAR"]


def test_child_instantiation_extends_loaders(env_config):
    os.environ["ENVVAR"] = "Environment Variable Value"
    config = ChildClassyConf(loaders=[EnvFile(env_config)])
    assert config.ENVVAR == "Must be overrided"
    assert len(config._loaders) == 1  # EnvFile
    del os.environ["ENVVAR"]


def test_value_repr():
    assert repr(BasicClassyConf.ENVVAR) == 'Value(key="ENVVAR", help="Just a test.")'


def test_child_meta_extends_loaders():
    config = ChildClassyConf()
    assert len(config._loaders) == 0


def test_get_value_no_instance():
    assert isinstance(BasicClassyConf.ENVVAR, Value)
    assert BasicClassyConf.ENVVAR.key == "ENVVAR"


def test_fail_missing_value():
    config = BasicClassyConf()

    with pytest.raises(UnknownConfiguration):
        config.ENVVAR

def test_iteration():
    config = BasicClassyConf()
    d = dict(config)
    assert len(d.keys()) == 2
    assert d['ENVVAR'] == BasicClassyConf.ENVVAR
    assert d['ENVVAR2'] == BasicClassyConf.ENVVAR2


def test_customized_loaders(env_config, ini_config):
    os.environ["ENVVAR"] = "Environment Variable Value"
    os.environ["ENVVAR2"] = "Foo"
    loaders = [EnvFile(env_config), Environment(), IniFile(ini_config)]
    assert getconf("ENVVAR", loaders=loaders) == "Must be overrided"
    assert getconf("ENVVAR2", loaders=loaders) == "Foo"
    assert getconf("ENVFILE", loaders=loaders) == "Environment File Value"
    assert getconf("INIFILE", loaders=loaders) == "INI File Value"
    del os.environ["ENVVAR"]
    del os.environ["ENVVAR2"]


def test_config_default_values():
    assert (
        getconf("DEFAULT", default="Default Value", loaders=[Environment()])
        == "Default Value"
    )


def test_config_cast_value():
    os.environ["INTEGER"] = "42"
    assert getconf("INTEGER", cast=int, loaders=[Environment()]) == 42


def test_fail_invalid_cast_type():
    os.environ["INTEGER"] = "42"
    with pytest.raises(TypeError):
        getconf("INTEGER", cast="not callable", loaders=[Environment()])


def test_fail_unknown_config_without_default_value():
    os.environ["ENVVAR"] = "Environment Variable Value"
    with pytest.raises(UnknownConfiguration):
        getconf("UNKNOWN", loaders=[Environment()])


def test_none_as_default_value():
    assert getconf("UNKNOWN", default=None, loaders=[Environment()]) is None


def test_none_default_value_identity_cast():
    os.environ["DEFAULT"] = "1"
    assert getconf("DEFAULT", default=None, loaders=[Environment()]) == "1"


def test_boolean_as_default_value():
    os.environ["BOOLEAN"] = "1"
    assert getconf("BOOLEAN", default=False, loaders=[Environment()]) == True


def test_int_as_default_value():
    os.environ["INT"] = "1"
    assert getconf("INT", default=0, loaders=[Environment()]) == 1


def test_str_as_default_value():
    os.environ["STR"] = "1"
    assert getconf("STR", default="foo", loaders=[Environment()]) == "1"
