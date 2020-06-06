FAQ
---

Why not use environment variables directly?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is a common pattern to read configurations in environment variable that
look similar to the code below:

.. code-block:: python

    if os.environ.get("DEBUG", False):
        print(True)
    else:
        print(False)

But this code have some issues:

#. If *envvar* ``DEBUG=False`` this code will print ``True`` because
   ``os.environ.get("DEBUG", False)`` will return an string `'False'` instead
   of a boolean `False`. And a non-empty string has a ``True`` boolean value.
#. We can't (dis|en)able debug with *envvars* ``DEBUG=yes|no``, ``DEBUG=1|0``,
   ``DEBUG=True|False``.
#. If we want to use this configuration during development we need to define
   this *envvar* all the time. We can't define this setting in a configuration
   file that will be used if `DEBUG` *envvar* is not defined.


Is classyconf tied to Django_ or Flask_?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No, classyconf was designed to be framework agnostic, be it for the web, CLI
or GUI applications.

.. _`Django`: https://www.djangoproject.com/
.. _`Flask`: http://flask.pocoo.org/


Why create a library similar to prettyconf or goodconf instead of using it?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Although `prettyconf` is great and very flexible, I don't like that the
`config("debug")` call isn't lazy, so putting it into a class isn't enough:

.. code-block:: python
  from prettyconf import config

  class MyConfig():
      debug = config("debug")   # this is evaluated when this module is loaded

I also didn't like the default `RecursiveSearch` that it provides and I also
needed to implement many changes and move fast to see what would work.

I've made several `contributions`_ to `prettyconf` but I needed to change its
behaviour, break things and move fast. This is backward incompatible, so, it
could break software that relies on the old behaviour.

You can use any of them. Both are good libraries and provides a similar set of
features.

.. _contributions: https://github.com/osantana/prettyconf/pulls?q=is%3Apr+author%3Ahernantz+is%3Aclosed


How does classyconf compare to python-dotenv_?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

python-dotenv_ reads the key, value pair from .env file and adds them to
environment variable. It is good for some tools that simply proxy the env to
some other process, like docker-compose_ or pipenv_.

On the other hand, classyconf does not populate the ``os.environ`` dictionary,
because it is designed to discover configuration from diferent sources, the
environment being just one of them.


What are some useful third-parties casts for Django?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Django is a popular python web framework that imposes some structure on the way
its settings are configured. Here are a few 3rd party casts that help you adapt
strings into that inner structures:

* `dj-database-url`_ - Parses URLs like ``mysql://user:pass@server/db`` into
  Django ``DATABASES`` configuration format.
* `django-cache-url`_ - Parses URLs like ``memcached://server:port/prefix``
  into Django ``CACHES`` configuration format.
* `dj-email-url`_ - Parses URLs like
  ``smtp://user@domain.com:pass@smtp.example.com:465/?ssl=True`` with
  parameters used in Django ``EMAIL_*`` configurations.
* `dj-admins-setting`_ - Parses emails lists for the ``ADMINS`` configuration.


.. _dj-database-url: https://github.com/kennethreitz/dj-database-url
.. _django-cache-url: https://github.com/ghickman/django-cache-url
.. _dj-email-url: https://github.com/migonzalvar/dj-email-url
.. _dj-admins-setting: https://github.com/hernantz/dj-admins-setting
.. _`python-dotenv`: https://github.com/theskumar/python-dotenv
.. _`pipenv`: https://pipenv.readthedocs.io/en/latest/advanced/#automatic-loading-of-env
.. _`docker-compose`: https://docs.docker.com/compose/env-file/
