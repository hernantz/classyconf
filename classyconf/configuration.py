from collections import OrderedDict

from .casts import Boolean, List, Option, Tuple, Identity, evaluate
from .exceptions import UnknownConfiguration
from .loaders import Environment, NOT_SET
from typing import Callable


# Shortcut for standard casts
as_boolean = Boolean()
as_list = List()
as_tuple = Tuple()
as_option = Option
as_is = Identity()


class Configuration(object):
    def __init__(self, loaders=None):
        if loaders is None:
            loaders = [
                Environment(),
            ]
        self.loaders = loaders

    def __repr__(self):
        loaders = ', '.join([repr(l) for l in self.loaders])
        return '{}(loaders=[{}])'.format(self.__class__.__name__, loaders)

    def __call__(self, item, default=NOT_SET, cast=None):

        if callable(cast):
            cast = cast
        elif cast is None and (default is NOT_SET or default is None):
            cast = as_is
        elif isinstance(default, bool):
            cast = as_boolean
        elif cast is None:
            cast = type(default)
        else:
            raise TypeError("Cast must be callable")

        for loader in self.loaders:
            try:
                return cast(loader[item])
            except KeyError:
                continue

        if default is NOT_SET:
            raise UnknownConfiguration("Configuration '{}' not found".format(item))

        return cast(default)

    def reset(self):
        for loader in self.loaders:
            loader.reset()


class Value:
    def __init__(self, key: str = None, help: str = '', default: NOT_SET = NOT_SET, cast: Callable = None):
        """
        :param key:     Name of the value used in file or environment
                        variable. Set automatically by the GoodConf metaclass.
        :param default: Default value if none is provided. If left unset,
                        loading a config that fails to provide this value
                        will raise a RequiredValueMissing exception.
        :param cast:    Callable to cast variable with. Defaults to type of
                        default (if provided), identity if default is not
                        provided or raises TypeError if provided cast is not
                        callable.
        :param help:    Plain-text description of the value.
        """
        self.key = key
        self.help = help
        self.default = default
        self.cast = cast

    def __get__(self, instance, owner):
        if instance:
            return instance._config(self.key, default=self.default, cast=self.cast)
        return self

    def __repr__(self):
        return '{}(key={}, help="{}")'.format(self.__class__.__name__, self.key, self.help)


class DeclarativeValuesMetaclass(type):
    """
    Collect Value objects declared on the base classes
    """

    def __new__(self, class_name, bases, attrs):
        # Collect values from current class and all bases.
        values = OrderedDict()

        # Walk through the MRO and add values from base class.
        for base in reversed(bases):
            if hasattr(base, "_declared_values"):
                values.update(base._declared_values)

        for key, value in attrs.items():
            if isinstance(value, Value):
                if value.key and key != value.key:
                    raise AttributeError(
                        "Don't explicitly set keys when declaring values")
                value.key = key
                values.update({key: value})

        attrs["_declared_values"] = values

        return super(DeclarativeValuesMetaclass, self).__new__(
            self, class_name, bases, attrs)

    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        # Remember the order that values are defined.
        return OrderedDict()


class ClassyConf(metaclass=DeclarativeValuesMetaclass):
    """
    Encapsulates settings than can be loaded from different
    sources
    """
    class Meta:
        loaders = None

    def __init__(self, loaders=None):
        _loaders = self.Meta.loaders
        if _loaders is None:
            _loaders = []
        if loaders:
            _loaders = loaders
        self._config = Configuration(loaders=_loaders)

    def __iter__(self):
        yield from self._declared_values.items()

    def __repr__(self):
        return "{}(loaders=[{}])".format(
            self.__class__.__name__, ", ".join(
                [str(loader) for loader in self._config.loaders]))

    def __str__(self):
        values = [repr(self)]
        for _, v in self:
            if v.default is NOT_SET and not v.help:
                help = "No default value provided"
            elif not v.help:
                help = "Default value is {}.".format(repr(v.default))
            else:
                help = v.help
            try:
                values.append("{}={} - {}".format(v.key, repr(getattr(self, v.key)), help))
            except UnknownConfiguration:
                values.append("{}=NOT_SET - {}".format(v.key, help))
        return "\n".join(values)

    def __hash__(self):
        # TODO: https://eng.lyft.com/hashing-and-equality-in-python-2ea8c738fb9d
        return {}

    def __getitem__(self, value):
        return self._declared_values[value].__get__(self, self.__class__)


def reset_conf(conf):
    """Anytime you want to pick up new values call this function."""
    # TODO: Los loaders son instancias que guardan estado
    conf._config.reset()
