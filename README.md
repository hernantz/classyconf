# ClassyConf

![PyPI](https://img.shields.io/pypi/v/classyconf?style=flat-square)

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
from classyconf import Configuration, Value, EnvFile, IniFile

class AppConfig(Configuration):
    """Configuration for My App"""
    class Meta:
        loaders = [EnvFile(".env"), IniFile("/etc/conf.ini/")]

    DEBUG = Value(default=False, help="Toggle debugging.")
    DATABASE_URL = Value(
        default="postgres://localhost:5432/mydb",
        help="Database connection.")
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

accessed as dict or object

```python
config.DEBUG
config["DEBUG"]
```

or passed around

```python
def do_something(cfg):
    if cfg.DEBUG:   # this is evaluated lazily
         return
```
