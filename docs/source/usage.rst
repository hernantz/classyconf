Usage
-----

One of the simplest ways to get started with ``classyconf`` is to use the
:py:class:`Configuration<classyconf.configuration.Configuration>` class.

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

Another more declarative approach is to use the
:py:class:`ClassyConf<classyconf>`.

.. code-block:: python

    from classyconf import ClassyConf, Value

    class AppConfig(ClassyConf):
        """Configuration for My App"""

        DEBUG = Value(default=False, help="Toggle debugging.")
        DATABASE_URL = Value(
            default='postgres://localhost:5432/mydb',
            help="Database connection.")


This pythonic class allows you to encapsulate all configuration in one object
that can be extended or passed around your codebase.


.. seealso::
    Learn more of what you can achieve and customize at .
    :doc:`Loaders<loaders>` will help you customize how configuration
    discovery works. Find out more at :ref:`discovery-customization`.


.. seealso::
    Some loaders include a ``var_format`` callable argument, see
    :ref:`variable-naming` to read more about it's purpose.

.. code-block:: python

    environments = {
        "production": ("spam", "eggs"),
        "local": ("spam", "eggs", "test"),
    }

    # Will return a tuple with ("spam", "eggs") when
    # ENVIRONMENT is undefined or defined with `production`
    # and a tuple with ("spam", "eggs", "test") when
    # ENVIRONMENT is set with `local`.
    MODULES = config("ENVIRONMENT",
                     default="production",
                     cast=Option(environment))
