Advanced Usage
--------------

Most of the time you can use the ``prettyconf.config`` function to get your
settings and use the ``prettyconf``'s standard behaviour. But some times
you need to change this behaviour.

To make this changes possible you can always create your own
``Configuration()`` instance and change it's default behaviour:

.. code-block:: python

    from prettyconf import Configuration

    config = Configuration()

.. warning:: ``prettyconf`` will skip configuration files inside ``.zip``,
   ``.egg`` or wheel packages.


.. _discovery-customization:


Customizing the configuration discovery
+++++++++++++++++++++++++++++++++++++++

By default the library will use the envrionment and the directory of the file
where ``config()`` was called as the start directory to look for a ``.env``
configuration file.  Consider the following file structure:

.. code-block:: text

    project/
      app/
        .env
        config.ini
        settings.py

If you call ``config()`` from ``project/app/settings.py`` the library will
inspect the envrionment and then look for configuration files at
``project/app``.

You can change that behaviour, by customizing configuration loaders to look at
a different ``path`` when instantiating your ``Configuration()``:

.. code-block:: python

    # Code example in project/app/settings.py
    import os

    from prettyconf import Configuration
    from prettyconf.loaders import Environment, EnvFile

    project_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
    env_file = f"{project_path}/.env"
    config = Configuration(loaders=[Environment(), EnvFile(filename=env_file)])

The example above will start looking for configuration in the environment and
then in a ``.env`` file at ``project/`` instead of ``project/app``.

Because ``config`` is nothing but an already instantiated ``Configuration`` object,
you can also alter this ``loaders`` attribute in ``prettyconf.config`` before use it:

.. code-block:: python

    # Code example in project/app/settings.py
    import os

    from prettyconf import config
    from prettyconf.loaders import Environment, EnvFile

    project_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
    env_file = f"{project_path}/.env"
    config.loaders = [Environment(), EnvFile(filename=env_file)]

Read more about how loaders can be configured in the :doc:`loaders section<loaders>`.

.. _variable-naming:

Naming conventions for variables
++++++++++++++++++++++++++++++++

There happen to be some formating conventions for configuration paramenters
based on where they are set. For example, it is common to name environment
variables in uppercase:

.. code-block:: sh

    $ DEBUG=yes OTHER_CONFIG=10 ./app.py

but if you were to set this config in an ``.ini`` file, it should probably be
in lower case:

.. code-block:: ini

    [settings]
    debug=yes
    other_config=10

command line argments have yet another conventions:

.. code-block:: sh

    $ ./app.py --debug=yes --another-config=10

Prettyconf let's you follow these aesthetics patterns by setting a
``var_format`` function when instantiating the :doc:`loaders<loaders>`.

By default, the :py:class:`Environment<prettyconf.loaders.Environment>` is
instantiated with ``var_format=str.upper`` so that lookups play nice with the
env variables.

.. code-block:: python

    from prettyconf import Configuration
    from prettyconf.loaders import Environment

    config = Configuration(loaders=[Environment(var_format=str.upper)])
    debug = config('debug', default=False, cast=config.boolean)  # lookups for DEBUG=[yes|no]

