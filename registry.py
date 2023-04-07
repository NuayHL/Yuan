import os
from warnings import warn

class Registry:
    _All_Registry = dict()
    def __init__(self, name):
        assert isinstance(name, str)
        self._name = name
        self._dict = dict()
        Registry._All_Registry[self._name] = self

    @classmethod
    def get_registry(cls, name):
        return cls._All_Registry[name]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __getitem__(self, key):
        return self._dict[key]

    def __contains__(self, key):
        return key in self._dict.keys()

    def register(self, module):
        def _register(value, key=None):
            if key is None:
                key = value.__name__
            if key in self.keys():
                warn('Already has module %s. Please consider change register name' % key)
            self[key] = value
            return value

        if isinstance(module, str):
            return lambda value: _register(value, module)
        else:
            return _register(module)

    def name(self):
        return self._name

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def items(self):
        return self._dict.items()

    def __str__(self):
        return str(self._dict)
