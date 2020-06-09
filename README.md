# ClassyConf

![PyPI](https://img.shields.io/pypi/v/classyconf?style=flat-square)
![Run tests](https://github.com/hernantz/classyconf/workflows/Run%20tests/badge.svg?event=push)
[![codecov](https://codecov.io/gh/hernantz/classyconf/branch/master/graph/badge.svg)](https://codecov.io/gh/hernantz/classyconf)


![carbon(2)](https://user-images.githubusercontent.com/613512/83956588-258e3b00-a836-11ea-9599-3a0a0d6c2c61.png)


ClassyConf is a settings management solution for perfectionists with deadlines.

It adds a declarative way to define settings for your projects contained in a
class that can be extended, config objects can be passed around modules and
settings are lazyly loaded, plus some other goodies.

It's classy, it's pretty, it's good.

You can find out more documentation at [Read the
Docs](https://classyconf.readthedocs.io/en/latest/index.html) website, but
here is a preview of how to use it.

```python
from classyconf import Configuration, Value, Environment, IniFile, as_boolean, EnvPrefix

class AppConfig(Configuration):
    """Configuration for My App"""
    class Meta:
        loaders = [
            Environment(keyfmt=EnvPrefix("MY_APP_")),
            IniFile("/etc/app/conf.ini", section="myapp")
        ]

    DEBUG = Value(default=False, cast=as_boolean, help="Toggle debugging mode.")
    DATABASE_URL = Value(default="postgres://localhost:5432/mydb", help="Database connection.")
```

Later this object can be used to print settings

```python
>>> config = AppConfig()
>>> print(config)
DEBUG=True - Toggle debugging mode.
DATABASE_URL='postgres://localhost:5432/mydb' - Database connection.
```

or with `__repl__()`

```python
>>> config = AppConfig()
>>> config
AppConf(loaders=[Environment(keyfmt=EnvPrefix("MY_APP_"), EnvFile("main.env")])
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

iterated

```python
 >>> for setting in config:
...     print(setting)
...
('DEBUG', Value(key="DEBUG", help="Toggle debugging on/off."))
('DATABASE_URL', Value(key="DATABASE_URL", help="Database connection."))
```

or passed around

```python
def do_something(cfg):
    if cfg.DEBUG:   # this is evaluated lazily
         return
```
