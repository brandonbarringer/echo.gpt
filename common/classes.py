import warnings

class ManagerMeta(type):
    def __getattr__(cls, name: str):
        return getattr(super().__getattribute__(name))

    def __setattr__(cls, name: str, value):
        if hasattr(super().__getattribute__(name), name):
            super().__setattr__(name, value)
        else:
            super().__setattr__(name, value)

    def __delattr__(cls, name: str):
        delattr(super().__getattribute__(name), name)


class Manager(metaclass=ManagerMeta):
    _instance = None
    _data = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._data = {}
        return cls._instance

    def __getattr__(self, name: str):
        if name in self._data and isinstance(self._data[name], dict):
            return DotDict(self._data[name])
        return self._data.get(name)

    def __setattr__(self, name: str, value):
        if isinstance(value, dict):
            self._data[name] = DotDict(value)
        else:
            self._data[name] = value

    def __delattr__(self, name: str):
        del self._data[name]


class DotDict(dict):
    def __getattr__(self, name: str):
        if name in self:
            return self[name]
        # raise warning that the attribute name was not found in the caller name and return None
        warnings.warn(f'Attribute {name} not found in {self.__class__.__name__}')

    def __setattr__(self, name: str, value):
        self[name] = value

    def __delattr__(self, name: str):
        del self[name]