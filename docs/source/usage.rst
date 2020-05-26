Getting started
---------------

.. code-block:: python

    from classyconf import Configuration


    config = Configuration()
    MY_CONFIG = config("PROJECT_MY_CONFIG")

If ``PROJECT_MY_CONFIG`` is not defined in an environment variable,
``classyconf`` will raise a
:py:class:`UnknownConfiguration<classyconf.exceptions.UnknownConfiguration>`
exception.

In these cases you could define a default configuration value:

.. code-block:: python

    MY_CONFIG = config("PROJECT_MY_CONFIG", default="default value")

You can also use the ``cast`` argument to convert a string value into
a specific value type:

.. code-block:: python

    from classyconf import as_boolean

    DEBUG = config("DEBUG", default=False, cast=as_boolean)

The ``as_boolean`` cast converts strings values like ``On|Off``, ``1|0``,
``yes|no``, ``true|false`` into Python boolean ``True`` or ``False``.

.. seealso::
    Find out more about other casts or how to write
    your own at :doc:`Casts<casts>`.


Declarative configuration object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The simplest ways to get started with classyconf is to use the
:py:class:`ClassyConf<classyconf.configuration.Configuration>` class, to
declare all the settings of your app.

.. code-block:: python

    from classyconf import ClassyConf, Value, Enviroment, IniFile, Option


    class AppConfig(ClassyConf):
        """Configuration for My App"""

        DEBUG = Value(default=False, help="Toggle debugging.")
        DATABASE_URL = Value(
            default='postgres://localhost:5432/mydb',
            help="Database connection.")
        LOG_LEVEL = Value(
            default="INFO", cast=Option({"INFO": "info", "DEBUG": "debug"}))

        class Meta:
            loaders = [Environment(), IniFile("/etc/myapp/conf.ini")]


This pythonic class allows you to encapsulate all configuration
in one object by declaring your settings using the
:py:class:`Value<classyconf.configuration.Value>` descriptor.

You will notice that we have defined some loaders. :doc:`Loaders<loaders>`
will help you customize how configuration discovery works. This is a list of
objects that will be used to discover settings from different sources.

Each loader is checked in the given order. In this case, we will first lookup
each setting in the enviroment variables and, when not found, the declared
``.ini`` file. If a setting is not found by any loader, the default value is
returned, if set, or a
:py:class:`UnknownConfiguration<classyconf.exceptions.UnknownConfiguration>`
exception is thrown.

.. seealso::
    Some loaders include a ``var_format`` callable argument, see
    :ref:`variable-naming` to read more about it's purpose.

Later this object can be used to print settings

.. code-block:: python

    >>> conf = AppConfig()
    >>> print(conf)
    DEBUG=True
    DATABASE_URL=postgres://localhost:5432/mydb

Or with ``__repl__()``

.. code-block:: python

    >>> conf = AppConfig()
    >>> conf
    DEBUG=True (Toggle debugging.)
    DATABASE_URL=postgres://localhost:5432/mydb (Database connection.)

extended

.. code-block:: python

    class AppConfig(ClassyConf):
        class Meta:
            loaders = [IniFile("app_settings.ini")]

        DEBUG = Value(default=False)


    class DevConfig(AppConfig):
        class Meta:
            loaders = [IniFile("test_settings.ini")]


accessed as dict or object

.. code-block:: python

    config.DEBUG
    config["DEBUG"]

or passed around

.. code-block:: python

    def do_something(cfg):
        if cfg.DEBUG:   # this is evaluated lazily
            return

:doc:`Loaders<loaders>` will help you customize how configuration
discovery works.

.. seealso::
    Some loaders include a ``var_format`` callable argument, see
    :ref:`variable-naming` to read more about it's purpose.

.. code-block:: python
