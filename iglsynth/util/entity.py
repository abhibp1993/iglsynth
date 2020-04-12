__all__ = ["Entity"]

import logging
import uuid
from collections.abc import Hashable, Iterable
from weakref import WeakValueDictionary


def make_instance_name(mod_name, cls_name, name):
    return f"{mod_name}:{cls_name}:{name}"


class Entity(object):
    _instances = WeakValueDictionary()

    def __new__(cls, name=None, **kwargs):

        # If name is not given, generate one.
        name = uuid.uuid4() if name is None else name
        iname = make_instance_name(cls.__module__, cls.__qualname__, name)

        # Check if entity with the name already exists. If yes, return it.
        if iname in Entity._instances:
            old_entity = Entity._instances[iname]
            for key in kwargs:
                if key in old_entity.__dict__:
                    assert old_entity.__dict__[key] == kwargs[key], \
                        f"Entity creation failed. " \
                        f"There exists an entity with name={iname}. " \
                        f"But old_entity[{key}]={old_entity.__dict__[key]} does not match given " \
                        f"kwargs[{key}]={kwargs[key]}."
            return old_entity

        # If entity with given name does not exist, then create a new one
        assert isinstance(name, Hashable), f"Cannot create an entity with UnHashable name of type={type(name)}."
        new_entity = object.__new__(cls)
        Entity._instances[iname] = new_entity
        new_entity.__dict__["_name"] = name
        new_entity.__dict__.update(kwargs)
        return new_entity

    def __init__(self, name=None, **kwargs):
        # Entity data structure
        self._name = self._name
        self._class_name = self.__class__.__qualname__
        self._module_name = self.__class__.__module__

        # Logger for logging purposes
        self.logger = logging.getLogger(self.__module__)
        self.logger.info(f"{self} is created.")

    def __eq__(self, other):
        # FIXME: Should two objects of different classes be comparable?
        return type(other) == type(self) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self._name})"

    def __str__(self):
        return self.__repr__()

    @property
    def name(self):
        return self._name

    def serialize(self, ignores=None):
        ser_dict = self.__dict__.copy()
        ser_dict.pop("logger")

        if isinstance(ignores, Iterable):
            for item in ignores:
                ser_dict.pop(item)
        return ser_dict


if __name__ == '__main__':
    a = Entity(**{"name": "abhishek", "work": "student", "record": 10})
    print(a, id(a))

    b = Entity(**{"name": "abhishek", "work": "student"})
    print(b, id(b))

    c = Entity(name="abhishek")
    print(c, id(c))

    d = Entity()
    print(d, id(d))

    e = Entity(name="hello", work="student")
    print(e, e.__dict__)
    print(e.work)
