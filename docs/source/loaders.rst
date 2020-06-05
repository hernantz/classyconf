Configuration Loaders
---------------------

.. raw:: html

   <blockquote class="twitter-tweet"><p lang="en" dir="ltr">The history of config files:<br><br>.ini: maybe we need a little more<br>.xml: ok, this is too much<br>.json: ok, now we need comments back<br>.yaml: I&#39;m not sure about this python approach<br>.toml: back to .ini</p>&mdash; David Capello (@davidcapello) <a href="https://twitter.com/davidcapello/status/1262782791105892354?ref_src=twsrc%5Etfw">May 19, 2020</a></blockquote>

Loaders are in charge of loading configuration from various sources, like
``.ini`` files or *environment* variables, and expose configuration as a
dict-like object. Loaders are ment to be chained, so that classyconf checks
one by one for a given configuration variable.

If a loader doesn't find the configuration variable it raises a ``KeyError``
so that the next loader get's checked. If no loader returns any value, and no
default value was set, an
:py:class:`UnknownConfiguration<classyconf.exceptions.UnknownConfiguration>`
exception is thrown.

Classyconf comes with some loaders already included in
:py:mod:`classyconf.loaders<classyconf.loaders>`.

By default the library will check the environment with the
:py:class:`Environment<classyconf.loaders.Environment>` loader. You can
change that behaviour, by customizing the loaders and the order in wich
configuration discovery happens.

Loaders can be set in the ``Meta`` class when extending
:py:class:`ClassyConf<classyconf.configuration.ClassyConf>` or passed as a
param when instantiating it. The later takes precedence and overrides loaders
defined in ``Meta``. The order within the list of loaders matters and defines
the lookup order.

.. code-block:: python

    from classyconf import ClassyConf, IniFile, Environment, Value, EnvFile

    class AppConfig(ClassyConf):

        class Meta:
            loaders = [
                Environment(),
                IniFile("/path/to/config.ini")
            ]

        DEBUG = Value(default=False)
        OTHER_CONFIG = Value(default=0)


    # Checks for enviroment variables first
    # Then lookup settings in the `config.ini` file
    config = AppConfig()

    # Override loaders and only lookup in the `.env` file
    test_config = AppConfig(loaders=[EnvFile("/path/to/.env")])


.. _variable-naming:

Naming conventions and namespaces for settings
++++++++++++++++++++++++++++++++++++++++++++++

There happen to be some formatting conventions for configuration paramenters
based on where they are set. For example, it is common to name environment
variables in uppercase:

.. code-block:: sh

    $ DEBUG=yes OTHER_CONFIG=10 ./app.py

Since the enviroment is a global and shared dictionary, it is a good practice
to also apply some prefix to each setting to avoid collitions with other
known settings, like ``LOCALE``, ``TZ``, etc. This prefix works as a
namespace for your app.

.. code-block:: sh

    $ MY_APP_DEBUG=yes MY_APP_OTHER_CONFIG=10 ./app.py

but if you were to set this config in an ``.ini`` file, each setting should
probably be in lower case, the namespace is implicit in the file path, i.e:
``/etc/myapp/config.ini``.

.. code-block:: ini

    [settings]
    debug=yes
    other_config=10

Command line argments have yet another conventions:

.. code-block:: sh

    $ ./app.py --debug=yes --another-config=10

Classyconf let's you follow these aesthetics patterns by setting a
``fmt`` function when instantiating the loaders.

By default, the :py:class:`Environment<prettyconf.loaders.Environment>` is
instantiated with ``fmt=env_prefix('')`` so that it looks for
UPPER_CASED settings. But it can be easyly tweaked to address the prefix
issue by using ``fmt=env_prefix("MY_APP_")``, and look for
MY_APP_UPPER_CASED to play nice with other env variables.

.. code-block:: python

    from classyconf import ClassyConf, IniFile, Environment, Value, env_prefix

    class AppConfig(ClassyConf):

        class Meta:
            loaders = [
                Environment(fmt=env_prefix("MY_APP_")),
                IniFile("/etc/myapp/config.ini")
            ]

        DEBUG = Value(default=False)
        OTHER_CONFIG = Value(default=0)

    config = AppConfig()

    # looks for `MY_APP_DEBUG` in environment, then  `debug` in `settings` section of config.ini
    config.DEBUG

Keep reading to find out more about different loaders and their configurations.


Environment
+++++++++++

.. autoclass:: classyconf.loaders.Environment

The ``Environment`` loader gets configuration from ``os.environ``. Since it
is a common pattern to write env variables in caps, the loader accepts a
``fmt`` function to pre-format the variable name before the lookup
occurs. By default it is ``env_prefix("")`` which combines ``str.upper()``
and an empty prefix.

.. note::
    In the case of CLI apps, it would be recommended to set some sort of
    namespace so that you don't accidentally override other programs
    behaviour, like LOCALE or EDITOR, but instead MY_APP_LOCALE, etc. So
    consider using the ``env_prefix("MY_APP_")`` approach.



.. code-block:: python

    from classyconf import ClassyConf, Environment, Value

    class AppConf(ClassyConf):
        debug = Value(default=False)


    config = AppConf(loaders=[Environment(fmt=str.upper)])
    config.debug  # will look for a `DEBUG` variable


EnvFile
+++++++

.. autoclass:: classyconf.loaders.EnvFile

The ``EnvFile`` loader gets configuration from ``.env`` file. If the file
doesn't exist, this loader will be skipped without raising any errors.

.. code-block:: text

    # .env file
    DEBUG=1


.. code-block:: python

    from classyconf import ClassyConf, EnvFile, Value

    class AppConf(ClassyConf):
        debug = Value(default=False)


    config = AppConf(loaders=[EnvFile(file='.env', fmt=str.upper)])
    config.debug  # will look for a `DEBUG` variable instead of `debug`


.. note::
    You might want to use dump-env_, a utility to create ``.env`` files.


.. _`dump-env`: https://github.com/sobolevn/dump-env


IniFile
+++++++

.. autoclass:: classyconf.loaders.IniFile

The ``IniFile`` loader gets configuration from ``.ini`` or ``.cfg`` files. If
the file doesn't exist, this loader will be skipped without raising any errors.


CommandLine
+++++++++++

.. autoclass:: classyconf.loaders.CommandLine

This loader lets you extract configuration variables from parsed CLI arguments.
By default it works with `argparse`_ parsers.


.. code-block:: python

    import argparse
    from classyconf import ClassyConf, Value, NOT_SET, CommandLine


    parser = argparse.ArgumentParser(description='Does something useful.')
    parser.add_argument('--debug', '-d', dest='debug', default=NOT_SET, help='set debug mode')

    class AppConf(ClassyConf):
        DEBUG = Value(default=False)

    config = AppConf(loaders=[CommandLine(parser=parser)])
    print(config.DEBUG)


Something to notice here is the
:py:const:`NOT_SET<classyconf.loaders.NOT_SET>` value. CLI parsers often
force you to put a default value so that they don't fail. In that case, to
play nice with classyconf, you must set one. But that would break the
discoverability chain that classyconf encourages. So by setting this special
default value, you will allow classyconf to keep the lookup going.

The :py:func:`get_args<classyconf.loaders.get_args>` function converts the
argparse parser's values to a dict that ignores
:py:const:`NOT_SET<classyconf.loaders.NOT_SET>` values.


.. _argparse: https://docs.python.org/3/library/argparse.html


Dict
++++

.. autoclass:: classyconf.loaders.Dict

This loader is great when you want to pin certain settings without having to
change/override other loaders, files or defaults. It really comes handy when
you are extending a
:py:class:`ClassyConf<classyconf.configuration.ClassyConf>` class.

.. code-block:: python

    from classyconf import ClassyConf, Value, IniFile, Dict

    class AppConfig(ClassyConf):
        class Meta:
            loaders = [IniFile("/opt/myapp/config.ini"), IniFile("/etc/myapp/config.ini")]

        NUMBER = Value(default=1)
        DEBUG = Value(default=False)
        LABEL = Value(default="foo")
        OTHER  = Value(default="bar")


    class TestConfig(AppConfig):
        class Meta:
            loders = [Dict({"DEBUG": True, "NUMBER": 0})]


RecursiveSearch
+++++++++++++++

.. autoclass:: classyconf.loaders.RecursiveSearch

This loader tries to find ``.env`` or ``*.ini|*.cfg`` files and load them
with the :py:class:`EnvFile<classyconf.loaders.EnvFile>` and
:py:class:`IniFile<classyconf.loaders.IniFile>` loaders respectively.

It will start looking at the ``starting_path`` directory for configuration
files and walking up the filesystem tree until it finds any or reaches the
``root_path``.

.. warning::
    It is important to note that this loader uses the glob module internally to
    discover ``.env`` and ``*.ini|*.cfg`` files.  This could be problematic if
    the project includes many files that are unrelated, like a ``pytest.ini``
    file along side with a ``settings.ini``. An unexpected file could be found
    and be considered as the configuration to use.

Consider the following file structure:

.. code-block:: text

    project/
      settings.ini
      app/
        settings.py

When instantiating your
:py:class:`RecursiveSearch<classyconf.loaders.RecursiveSearch>`, if you pass
``/absolute/path/to/project/app/`` as ``starting_path`` the loader will start
looking for configuration files at ``project/app``.

.. code-block:: python

    # Code example in project/app/settings.py
    import os

    from classyconf import config
    from classyconf.loaders import RecursiveSearch

    app_path = os.path.dirname(__file__)
    config.loaders = [RecursiveSearch(starting_path=app_path)]

By default, the loader will try to look for configuration files until it finds
valid configuration files **or** it reaches ``root_path``. The ``root_path`` is
set to the root directory ``/`` initialy.

Suppose the following file structure:

.. code-block:: text

    projects/
      any_settings.ini
      project/
        app/
          settings.py

You can change this behaviour by setting any parent directory of the
``starting_path`` as the ``root_path`` when instantiating
:py:class:`RecursiveSearch<classyconf.loaders.RecursiveSearch>`:

.. code-block:: python

    # Code example in project/app/settings.py
    import os

    from classyconf import Configuration
    from classyconf.loaders import RecursiveSearch

    app_path = os.path.dirname(__file__)
    project_path = os.path.realpath(os.path.join(app_path, '..'))
    rs = RecursiveSearch(starting_path=app_path, root_path=project_path)
    config = Configuration(loaders=[rs])

The example above will start looking for files at ``project/app/`` and will stop looking
for configuration files at ``project/``, actually never looking at ``any_settings.ini``
and no configuration being loaded at all.

The ``root_path`` must be a parent directory of ``starting_path``, otherwise
it raises an :py:class:`InvalidPath<classyconf.exceptions.InvalidPath>`
exception:

.. code-block:: python

    from classyconf.loaders import RecursiveSearch

    # /baz is not parent of /foo/bar, so this raises an InvalidPath exception here
    rs = RecursiveSearch(starting_path="/foo/bar", root_path="/baz")


Writing your own loader
+++++++++++++++++++++++

If you need a custom loader, you should just extend the
:py:class:`AbstractConfigurationLoader<classyconf.loaders.AbstractConfigurationLoader>`.

.. autoclass:: classyconf.loaders.AbstractConfigurationLoader

For example, say you want to write a Yaml loader. It is important to note
that by raising a ``KeyError`` exception from the loader, classyconf knows
that it has to keep looking down the loaders chain for a specific config.

.. code-block:: python

    import yaml
    from classyconf.loaders import AbstractConfigurationLoader


    class YamlFile(AbstractConfigurationLoader):
        def __init__(self, filename):
            self.filename = filename
            self.config = None

        def _parse(self):
            if self.config is not None:
                return
            with open(self.filename, 'r') as f:
                self.config = yaml.load(f)

        def __contains__(self, item):
            try:
                self._parse()
            except:
                return False

            return item in self.config

        def __getitem__(self, item):
            try:
                self._parse()
            except:
                # KeyError tells classyconf to keep looking elsewhere!
                raise KeyError("{!r}".format(item))

            return self.config[item]

        def reload(self):
            self.config = None


Then configure classyconf to use it.

.. code-block:: python

    from classyconf import ClassyConf

    class AppConf(ClassyConf):
        class Meta:
            loaders = [YamlFile('/path/to/config.yml')]
