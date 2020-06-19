Advanced
--------

Caching
~~~~~~~

Everytime you access a Value, classyconf peek on the loaders one by one until
a loader returns a setting. If a setting is not found by any loader, the
default value is returned, if set, or a
:py:class:`UnknownConfiguration<classyconf.exceptions.UnknownConfiguration>`
exception is thrown.

If the loaders chain is long or you are accessing the settings too often,
there is an optimization you can use, which is the cache property:

.. code-block:: python

    from classyconf import Configuration, Value, Environment, EnvFile, IniFile


    class AppConfig(Configuration):

        DEBUG = Value(default=False, help="Toggle debugging on/off.")

        class Meta:
            loaders=[Environment(), EnvFile(".env"), IniFile("config.ini")]
            cache = True

This property can also be set at runtime:

.. code-block:: python

    >>> config = AppConfig(cache=True)
    >>>

It will make the lookup to have a ``O(1)`` performance the second time it is
accesed.


Reloading new settings
~~~~~~~~~~~~~~~~~~~~~~

Typically when files get parsed, their values are kept in an internal cache
by each loader. If at some point you want to pickup new values, for example
when using a long running daemon, call the reset method.

.. code-block:: python

    import signal

    config = AppConfig()

    def signal_handler(signum, frame):
        if signum == signal.SIGHUP:  # kill -1 <pid>
            config.reset()

    signal.signal(signal.SIGHUP, signal_handler)

    if __name__ == '__main__':
        main(config)
