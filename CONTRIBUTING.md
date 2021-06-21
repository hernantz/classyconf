# Setup the project

1. Clone the project [https://github.com/hernantz/classyconf](https://github.com/hernantz/classyconf)
1. Make sure you have [poetry](https://python-poetry.org/) and `make` installed.
2. Run `make setup` to install the dependencies.
3. Run `make test` to check everything is running properly.


# Release

1. Update the changelog at `docs/source/changelog.rst`.
2. Run `make version=<VERSION> release`
