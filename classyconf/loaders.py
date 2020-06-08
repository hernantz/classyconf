import os
from configparser import ConfigParser, MissingSectionHeaderError, NoOptionError
from glob import glob

from .exceptions import InvalidConfigurationFile, InvalidPath, MissingSettingsSection
from .parsers import EnvFileParser


class NotSet(str):
    """
    A special type that behaves as a replacement for None.
    We have to put a new default value to know if a variable has been set by
    the user explicitly. This is useful for the ``CommandLine`` loader, when
    CLI parsers force you to set a default value, and thus, break the discovery
    chain.
    """

    pass


NOT_SET = NotSet()


class EnvPrefix:
    """
    Since the environment is a global dictionary, it is a good practice to
    namespace your settings by using a unique prefix like ``MY_APP_``.
    """

    def __init__(self, prefix=""):
        self.prefix = prefix

    def __call__(self, value):
        return "{}{}".format(self.prefix, value.upper())

    def __repr__(self):
        return '{}("{}")'.format(self.__class__.__name__, self.prefix)


def get_args(parser):
    """
    Converts arguments extracted from a parser to a dict,
    and will dismiss arguments which default to NOT_SET.

    :param parser: an ``argparse.ArgumentParser`` instance.
    :type parser: argparse.ArgumentParser
    :return: Dictionary with the configs found in the parsed CLI arguments.
    :rtype: dict
    """
    args = vars(parser.parse_args()).items()
    return {key: val for key, val in args if not isinstance(val, NotSet)}


class AbstractConfigurationLoader:
    def __repr__(self):
        raise NotImplementedError()  # pragma: no cover

    def __contains__(self, item):
        raise NotImplementedError()  # pragma: no cover

    def __getitem__(self, item):
        raise NotImplementedError()  # pragma: no cover

    def check(self):
        return True

    def reset(self):
        pass


class CommandLine(AbstractConfigurationLoader):
    """
    Extract configuration from an ``argparse`` parser.
    """

    # noinspection PyShadowingNames
    def __init__(self, parser, get_args=get_args):
        """
        :param parser: An `argparse` parser instance to extract variables from.
        :param function get_args: A function to extract args from the parser.
        :type parser: argparse.ArgumentParser
        """
        self.parser = parser
        self.configs = get_args(self.parser)

    def __repr__(self):
        return "{}(parser={})".format(self.__class__.__name__, self.parser)

    def __contains__(self, item):
        return item in self.configs

    def __getitem__(self, item):
        return self.configs[item]


class IniFile(AbstractConfigurationLoader):
    def __init__(self, filename, section="settings", keyfmt=lambda x: x):
        """
        :param str filename: Path to the ``.ini/.cfg`` file.
        :param str section: Section name inside the config file.
        :param function keyfmt: A function to pre-format variable names.
        """
        self.filename = filename
        self.section = section
        self.keyfmt = keyfmt
        self.parser = ConfigParser(allow_no_value=True)
        self._initialized = False

    def __repr__(self):
        return '{}("{}")'.format(self.__class__.__name__, self.filename)

    def _parse(self):
        if self._initialized:
            return

        with open(self.filename) as inifile:
            try:
                self.parser.read_file(inifile)
            except (UnicodeDecodeError, MissingSectionHeaderError):
                raise InvalidConfigurationFile()

        if not self.parser.has_section(self.section):
            raise MissingSettingsSection(
                "Missing [{}] section in {}".format(self.section, self.filename)
            )

        self._initialized = True

    def check(self):
        try:
            self._parse()
        except (FileNotFoundError, InvalidConfigurationFile, MissingSettingsSection):
            return False

        return super().check()

    def __contains__(self, item):
        if not self.check():
            return False

        return self.parser.has_option(self.section, self.keyfmt(item))

    def __getitem__(self, item):
        if not self.check():
            raise KeyError("{!r}".format(item))

        try:
            return self.parser.get(self.section, self.keyfmt(item))
        except NoOptionError:
            raise KeyError("{!r}".format(item))

    def reset(self):
        self._initialized = False


class Environment(AbstractConfigurationLoader):
    """
    Get's configuration from the environment, by inspecting ``os.environ``.
    """

    def __init__(self, keyfmt=EnvPrefix()):
        """
        :param function keyfmt: A function to pre-format variable names.
        """
        self.keyfmt = keyfmt

    def __repr__(self):
        return "{}(keyfmt={})".format(self.__class__.__name__, self.keyfmt)

    def __contains__(self, item):
        return self.keyfmt(item) in os.environ

    def __getitem__(self, item):
        # Uses `os.environ` because it raises an exception if the environmental
        # variable does not exist, whilst `os.getenv` doesn't.
        return os.environ[self.keyfmt(item)]


class EnvFile(AbstractConfigurationLoader):
    def __init__(self, filename=".env", keyfmt=EnvPrefix()):
        """
        :param str filename: Path to the ``.env`` file.
        :param function keyfmt: A function to pre-format variable names.
        """
        self.filename = filename
        self.keyfmt = keyfmt
        self.configs = None

    def __repr__(self):
        return '{}("{}")'.format(self.__class__.__name__, self.filename)

    def _parse(self):
        if self.configs is not None:
            return

        self.configs = {}
        with open(self.filename) as envfile:
            self.configs.update(EnvFileParser(envfile).parse_config())

    def check(self):
        if not os.path.isfile(self.filename):
            return False

        try:
            self._parse()
        except FileNotFoundError:
            return False

        return super().check()

    def __contains__(self, item):
        if not self.check():
            return False

        return self.keyfmt(item) in self.configs

    def __getitem__(self, item):
        if not self.check():
            raise KeyError("{!r}".format(item))

        return self.configs[self.keyfmt(item)]

    def reset(self):
        self.configs = None


class RecursiveSearch(AbstractConfigurationLoader):
    def __init__(
        self,
        starting_path=None,
        filetypes=((".env", EnvFile), (("*.ini", "*.cfg"), IniFile)),
        root_path="/",
    ):
        """
        :param str starting_path: The path to begin looking for configuration files.
        :param tuple filetypes: tuple of tuples with configuration loaders, order matters.
                                Defaults to
                                ``(('*.env', EnvFile), (('*.ini', *.cfg',), IniFile)``
        :param str root_path: Configuration lookup will stop at the given path. Defaults to
                              the current user directory
        """
        self.root_path = os.path.realpath(root_path)
        self._starting_path = self.root_path

        if starting_path:
            self.starting_path = starting_path

        self.filetypes = filetypes
        self._config_files = None

    @property
    def starting_path(self):
        return self._starting_path

    @starting_path.setter
    def starting_path(self, path):
        if not path:
            raise InvalidPath("Invalid starting path")

        path = os.path.realpath(os.path.abspath(path))
        if not path.startswith(self.root_path):
            raise InvalidPath("Invalid root path given")
        self._starting_path = path

    @staticmethod
    def get_filenames(path, patterns):
        filenames = []
        if type(patterns) is str:
            patterns = (patterns,)

        for pattern in patterns:
            filenames += glob(os.path.join(path, pattern))
        return filenames

    def _scan_path(self, path):
        config_files = []

        for patterns, Loader in self.filetypes:
            for filename in self.get_filenames(path, patterns):
                try:
                    loader = Loader(filename=filename)
                    if not loader.check():
                        continue
                    config_files.append(loader)
                except InvalidConfigurationFile:
                    continue

        return config_files

    def _discover(self):
        self._config_files = []

        path = self.starting_path
        while True:
            if os.path.isdir(path):
                self._config_files += self._scan_path(path)

            if path == self.root_path:
                break

            path = os.path.dirname(path)

    @property
    def config_files(self):
        if self._config_files is None:
            self._discover()

        return self._config_files

    def __repr__(self):
        return "{}(starting_path={})".format(
            self.__class__.__name__, self.starting_path
        )

    def __contains__(self, item):
        for config_file in self.config_files:
            if item in config_file:
                return True
        return False

    def __getitem__(self, item):
        for config_file in self.config_files:
            try:
                return config_file[item]
            except KeyError:
                continue
        else:
            raise KeyError("{!r}".format(item))

    def reset(self):
        self._config_files = None


class Dict(AbstractConfigurationLoader):
    def __init__(self, values_mapping):
        """
        :param dict values_mapping: A dictionary of hardcoded settings.
        """
        self.values_mapping = values_mapping

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.values_mapping)

    def __contains__(self, item):
        return item in self.values_mapping

    def __getitem__(self, item):
        return self.values_mapping[item]
