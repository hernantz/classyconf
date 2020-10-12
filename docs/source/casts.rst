Casts
-----

:doc:`Loaders<loaders>` gather configuration from different sources, but that
configuration usually is digested as strings and it might not be the correct
type you need in your programs.

That's why you can specify cast functions for each individual setting.

.. code-block:: python

    from classyconf import Configuration, Value, Environment, as_boolean
    from decimal import Decimal

    class Config(Configuration)
        class Meta:
          loaders = [Environment()]

        BASE_PRICE = Value(default=Decimal(10), cast=Decimal, help="Base product price.")
        DEBUG = Value(default=False, cast=as_boolean, help="Enables debug mode.")



Buitin Casts
~~~~~~~~~~~~

In :py:mod:`classyconf.casts<classyconf.casts>` you can find some common cast
functions that ship by default. If the cast fails it will rise an
:py:class:`InvalidConfiguration<classyconf.exceptions.InvalidConfiguration>`
exception.


Boolean
+++++++

Converts values like ``On|Off``, ``1|0``, ``yes|no``, ``y|n``,
``true|false``, ``t|f``
into booleans.

These options can be also extended by passing an extra True/False mapping.

.. code-block:: python

    from classyconf import Boolean

    boolean = Boolean({"sim": True, "não": False})
    assert boolean("sim")
    assert boolean("yes")
    assert not boolean("não")
    assert not boolean("no")


List
++++

Converts comma separated strings into lists by default.

This cast can accept other separators.

.. code-block:: python

    from classyconf import List

    as_list = List(delimiter=";")
    assert as_list("1; 2;3; ' 4; ';") == ['1', '2', '3', "' 4; '"]


Tuple
+++++

Same as ``List``, but converts comma separated strings into tuples.

.. code-block:: python

    from classyconf import Tuple

    as_tuple = Tuple()
    assert as_tuple("a, b, c") == ['a', 'b', 'c']


Option
++++++

Gets a return value based on specific options:

.. code-block:: python

    from classyconf import Option

    choices = {
        'option1': "asd",
        'option2': "def",
    }
    option = Option(choices)

    assert option("option1") == "asd"
    assert option("option2") == "def"


Evaluate
++++++++

Safely evaluate strings with Python literals to Python objects (alias to
Python's :py:func:`ast.literal_eval<ast.literal_eval>`).

.. code-block:: python

    from classyconf import evaluate


    assert evaluate("None") is None


Identity
++++++++

It is the no-op type of cast, returns anything it receives as is.

.. code-block:: python

    from classyconf import Identity


    as_is = Identity()

    assert as_is("None") is "None"


Shortcuts for standard casts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``classyconf`` ships with cast instances already configured for convenience.

.. code-block:: python

    from classyconf import as_list, as_tuple, as_boolean, as_option, as_is, evaluate

They are pretty much self explanatory, but ``as_is`` is an instance of
``Identity`` cast.


Custom casts
~~~~~~~~~~~~

You can implement your own custom casting function by passing any callable:

.. code-block:: python
    from classyconf import Configuration, Environment

    def number_list(value):
        return [int(v) for v in value.split(";")]

    class Config(Configuration)
        class Meta:
          loaders = [Environment()]

        NUMBERS = Value(default="1;2;3", cast=number_list, help="Semicolon separated numbers.")


.. _implicit-casts:

Implicit casts
~~~~~~~~~~~~~~
``classyconf`` tries to provide some sensible default casts based on the
default's value type.

1. If the user provides a cast function, we use that one, no questions asked.
2. If the user sets a default that is an ``int``, ``str``, ``boolean``, ``float``,
   etc, and doesn't set a cast function, we can set a default one: ``int()``,
   ``str()``, ``as_boolean()`` and ``float()`` respectively.
3. If the user doesn't set a default value we use the Identity cast (``as_is()``).
4. If the user sets a non callable value as cast, we raise a ``TypeError`` exception.

So following the first example:

.. code-block:: python

    from classyconf import Configuration, Value, Environment
    from decimal import Decimal


    def number_list(value):
        return [int(v) for v in value.split(";")]


    class Config(Configuration)
        class Meta:
          loaders = [Environment()]

        NUMBERS = Value("NUMBERS", default="1;2;3", cast=number_list)  # cast is number_list
        BASE_PRICE = Value(default=Decimal(10), help="Base product price.")  # cast is Decimal
        DEBUG = Value(default=False, help="Enables debug mode.")  # cast is as_boolean
