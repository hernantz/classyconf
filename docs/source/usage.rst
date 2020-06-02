Getting started
---------------

ClassyConf aims to be the configuration management solution for
perfectionists with deadlines.

It solves many problems, so let's get started with an incremental
introduction to what it can do for you.


1. Declaring settings
~~~~~~~~~~~~~~~~~~~~~

The simplest ways to get started with classyconf is to use the
:py:class:`ClassyConf<classyconf.configuration.Configuration>` class, to
declare all the settings of your app.

This pythonic class allows you to encapsulate all configuration
in one object by declaring your settings using the
:py:class:`Value<classyconf.configuration.Value>` descriptor.

In this case, we will use a single debug setting, but there could be as many
as you need.

.. code-block:: python

    from classyconf import ClassyConf, Value, as_boolean


    class AppConfig(ClassyConf):

        DEBUG = Value(default=False, cast=as_boolean, help="Toggle debugging on/off.")


We are using the ``as_boolean`` cast for the ``DEBUG`` setting. The
``as_boolean`` cast converts values like ``On|Off``, ``1|0``, ``yes|no``,
``true|false``, ``t|f`` into Python boolean ``True`` or ``False``.

.. seealso::
    Visit the :doc:`Casts<casts>` section to find out more about other casts
    or how to write your own.

    Since we provided a boolean default, there is no need to explicitely set
    a cast in this case, classyconf will choose the ``as_boolean`` to save
    you some typing. Visit the :ref:`implicit-casts` section to see how to
    customize this.


2. Discovering settings
~~~~~~~~~~~~~~~~~~~~~~~

Now that we defined the settings we needed, we will define where to obtain
them.

:doc:`Loaders<loaders>` will help you customize how configuration discovery
works. This is a list of objects that will be used to discover settings from
different sources.

Loaders can be declared in the ``Meta`` class:

.. code-block:: python

    from classyconf import ClassyConf, Value, Environment


    class AppConfig(ClassyConf):

        DEBUG = Value(default=False, help="Toggle debugging on/off.")

        class Meta:
            loaders=[Environment()]

In this case we are telling classyconf to only search for settings in the
``os.enviroment`` variables. I know, this is not very useful, and seems like
an overkill. Let's override this default loaders list and introduce another
loader to gather setting from a `.ini` file.

.. code-block:: python

    >>> from classyconf import Environment, IniFile
    >>> config = AppConfig(loaders=[
            Environment(),
            IniFile("/etc/myapp/conf.ini", section="settings")
        ])

Now you might be asking, is this reading a file? do I have to create it? How
do I access my settings?

Configuration discovery only happens when a ``Value`` setting is first accessed,
so nothing gets evaluated until then.

The config instance can accessed as dict or object. Let's trigger a look up:

.. code-block:: python

    >>> config.DEBUG  # config["DEBUG"] also works!
    False

Each loader is checked in the given order. In this case, we will first lookup
each setting in the ``os.enviroment`` variables and, when not found, the
declared `.ini` file (inside the ``settings`` section), but if this file
doesn't exist or is broken, this loader is ignored.

If a setting is not found by any loader, the default value is returned, if
set, or a
:py:class:`UnknownConfiguration<classyconf.exceptions.UnknownConfiguration>`
exception is thrown.

Now we all know that the industry practices have set different naming
conventions for diffent configuration formats. Is it ``camelCase`` for
`.json` files? Is it ``UPPER_CASE`` for the enviroment variables and
``lower_case`` for `.ini` files? Don't worry, classyconf has your back.

Most loaders include a ``var_format`` callable argument. This allows you
to alter the name of the setting for each individual loader.

Let's customize this:

.. code-block:: python

    >>> from classyconf import env_prefix
    >>> config = AppConfig(loaders=[
            Environment(var_format=env_prefix("MY_APP_")),
            IniFile("/etc/myapp/conf.ini", section="settings", var_format=str.lower)
        ])

Now if you access ``config.DEBUG``, classyconf will first check for
``MY_APP_DEBUG=xxx`` in the ``os.enviroment`` but for ``debug=xxx`` in the
``.ini`` file.

.. seealso::
    The rationale for ``var_format`` is to follow the best practices for
    naming variables, and respecting namespaces for each source of config.

    Read more at :ref:`variable-naming`.


3. Extending settings
~~~~~~~~~~~~~~~~~~~~~

As you know, the same code might run in several different enviroments, like
dev, staging, prod, etc.

Although ``ClassyConf`` classes can be extended to define new ``Value``
attributes or override them, the recomended way is to simply override the
settings sources per enviroment.

.. code-block:: python

    from classyconf import EnvFile

    class StagingConfig(AppConfig):
        class Meta:
            loaders = [EnvFile("staging.env")]


As we saw earlier, loaders can also be overridden at instantiation time.

.. code-block:: python

    from classyconf import Dict, EnvFile

    test_config = AppConfig(loaders=[Dict({"DEBUG": True}), EnvFile("test.env")]

In the snippet above we used the :py:class:`Dict<classyconf.loaders.Dict>`
loader, which comes handy to ensure certain hardcoded settings always get
picked up.


4. Inspecting settings
~~~~~~~~~~~~~~~~~~~~~~

Later this object can be used to print configuration, this will evaluate every setting.

.. code-block:: python

    >>> config = AppConfig()
    >>> print(config)
    DEBUG=False - Toggle debugging on/off.

Or with ``__repl__()`` you get a preview of how it was instantiated.

.. code-block:: python

    >>> config = AppConfig()
    >>> config
    AppConf(loaders=[Environment()])


It can also be iterated. This gives you the field key and the ``Value``
instance for you to keep inspecting (this doesn't evaluate the setting).

.. code-block:: python

    >>> for setting in config:
    ...     print(setting)
    ...
    ('DEBUG', Value(key="DEBUG", help="Output extra debugging info"))


Lastly, if you want to pickup new values at some point, for example when
using a long running daemon, call the reset method.

.. code-block:: python

    import signal

    config = AppConfig()

    def signal_handler(signum, frame):
        if signum == signal.SIGHUP:  # kill -1 <pid>
            config.reset()

    signal.signal(signal.SIGHUP, signal_handler)

    if __name__ == '__main__':
        main(config)
