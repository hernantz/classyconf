import os
import pytest
from classyconf.loaders import Environment, env_prefix


def test_env_prefix():
    keyfmt = env_prefix()
    assert keyfmt("test") == "TEST"


def test_env_prefix_with_prefix():
    keyfmt = env_prefix("prefix_")
    assert keyfmt("test") == "prefix_TEST"


def test_basic_config():
    os.environ["TEST"] = "test"
    config = Environment()

    assert "TEST" in config
    assert "test" == config["TEST"]
    assert repr(config).startswith("Environment(keyfmt=")

    del os.environ["TEST"]


def test_fail_missing_config():
    config = Environment()

    assert "UNKNOWN" not in config
    with pytest.raises(KeyError):
        _ = config["UNKNOWN"]


def test_default_keyfmt():
    os.environ["TEST"] = "test"
    config = Environment()

    assert "test" in config
    assert "test" == config["test"]

    del os.environ["TEST"]


def test_custom_keyfmt():
    def formatter(x):
        return "_{}".format(x)

    os.environ["_TEST"] = "test"
    config = Environment(keyfmt=formatter)

    assert "TEST" in config
    assert "test" == config["TEST"]

    del os.environ["_TEST"]
