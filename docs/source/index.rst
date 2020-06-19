.. classyconf documentation master file, created by
   sphinx-quickstart on Wed Jul  1 17:34:10 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

classyconf
==========

Configuration is just another API of your app. It allows us to preset or
modify it's behavior based on where it is installed and how it will be
executed, providing more flexibility to the users of such software.

It is important to provide a clear separation of configuration and code. This
is because config varies substantially across deploys and executions, code
should not. The same code can be run inside a container or in a regular
machine, it can be executed in production or in testing environments.

Configuration management is an important aspect of the architecture of any
system. But it is sometimes overlooked.

Classyconf is here to help, it's the configuration management solution for
perfectionists with deadlines.

.. toctree::
   :maxdepth: 2

   introduction.rst
   installation.rst
   usage.rst
   loaders.rst
   casts.rst
   advanced.rst
   faq.rst
   changelog.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
