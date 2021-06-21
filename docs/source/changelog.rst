Changelog
---------

All notable changes to this project will be documented in this file.

This project adheres to `Semantic Versioning`_.

.. _`Semantic Versioning`: https://semver.org/spec/v2.0.0.html

Unreleased
==========

  - Added python 3.9 support.

0.5.0
=====

  - Migrated from ``setup.py`` to ``pyproject.toml``.
  - Refactored Makefile and added tbump directive.


0.4.0
=====

  - Changed references to the obsolete ``ClassyConf`` object in docs.
  - Exposed ``CommandLine`` loader in the library import root.


0.3.0
=====

  - Added keyword only flag for ``Value`` and ``Configuration`` classes.
  - Added cache option for ``Configuration`` class.


0.2.0
=====

  - Replaced ``env_prefix`` with the ``EnvPrefix`` class.
  - Replaced coveralls with codecov.
  - Replaced TravisCI with Github Actions.


0.1.0
=====

  - First version
