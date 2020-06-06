# ClassyConf

![PyPI](https://img.shields.io/pypi/v/classyconf?style=flat-square)
[![Build Status](https://travis-ci.org/hernantz/classyconf.svg?branch=master)](https://travis-ci.org/hernantz/classyconf)
[![Coverage Status](https://coveralls.io/repos/github/hernantz/classyconf/badge.svg?branch=master)](https://coveralls.io/github/hernantz/classyconf?branch=master)


![carbon(2)](https://user-images.githubusercontent.com/613512/83956588-258e3b00-a836-11ea-9599-3a0a0d6c2c61.png)



ClassyConf is an extensible library for settings & code separation.

It was born as a wrapper around
[prettyconf](https://github.com/osantana/prettyconf), inspired by
[goodconf](https://github.com/lincolnloop/goodconf).

It adds a declarative way to define settings for your projects contained in a
class that can be extended, config objects can be passed around modules and
settings are lazyly loaded, plus some other goodies.

It's classy, it's pretty, it's good.

Here is a preview of how to use it. You can find out more documentation at
[Read the Docs](https://classyconf.readthedocs.io/en/latest/index.html) website.

```python
from classyconf import Configuration, Value, Environment, IniFile, as_boolean, env_prefix

class AppConfig(Configuration):
    """Configuration for My App"""
    class Meta:
        loaders = [
            Environment(keyfmt=env_prefix("MY_APP_")),
            IniFile("/etc/app/conf.ini", section="myapp")
        ]

    DEBUG = Value(default=False, cast=as_boolean, help="Toggle debugging mode.")
    DATABASE_URL = Value(default="postgres://localhost:5432/mydb", help="Database connection.")
```

Later this object can be used to print settings

```python
>>> conf = AppConfig()
>>> print(conf)
DEBUG=True
DATABASE_URL=postgres://localhost:5432/mydb
```

Or with `__repl__()`

```python
>>> conf = AppConfig()
>>> conf
DEBUG=True (Toggle debugging.)
DATABASE_URL=postgres://localhost:5432/mydb (Database connection.)
```

extended

```python
class AppConfig(ClassyConf):
    class Meta:
        loaders = [IniFile("app_settings.ini")]

    DEBUG = Value(default=False)


class DevConfig(AppConfig):
    class Meta:
        loaders = [IniFile("test_settings.ini")]
```

overridden at runtime

```python
>>> dev_config = AppConfig(loaders=[IniFile("test_settings.ini")])
>>> dev_config.DEBUG
True
```

accessed as dict or object

```python
>>> config.DEBUG
False
>>> config["DEBUG"]
False
```

or passed around

```python
def do_something(cfg):
    if cfg.DEBUG:   # this is evaluated lazily
         return
```
