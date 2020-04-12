__all__ = ["Entity"]

import logging
import uuid
from collections.abc import Hashable, Iterable
from weakref import WeakValueDictionary


def make_instance_name(mod_name, cls_name, name):
    return f"{mod_name}:{cls_name}:{name}"


class EntityMeta(type):
    _entity_registry = WeakValueDictionary()

    def __call__(cls, *args, **kwargs):
        # Create an instance of the object.
        #   ins below is returned after calling __new__ and __init__ methods of cls.
        ins = super(EntityMeta, cls).__call__(*args, **kwargs)

        # Validate the name of `ins` entity. If it is None, then generate a new one.
        name = ins._name if ins._name is not None else uuid.uuid4()

        # Is an object with the given name already instantiated?
        ins_registry_name = EntityMeta.make_registry_name(cls.__module__, cls.__qualname__, name)
        if ins_registry_name in EntityMeta._entity_registry:
            # Check if keyword arguments of existing instance and requested instance match.
            #   If not, we do not overwrite. Instead, raise an error.
            old_ins = EntityMeta._entity_registry[ins_registry_name]
            for key in kwargs:
                if key in old_ins.__dict__:
                    assert old_ins.__dict__[key] == kwargs[key], \
                        f"Entity creation failed. " \
                        f"There exists an entity with name={ins_registry_name}. " \
                        f"But old_entity[{key}]={old_ins.__dict__[key]} does not match given " \
                        f"kwargs[{key}]={kwargs[key]}."

            return old_ins

        # If an object with name does not exist, return the new instance
        ins._name = name
        EntityMeta._entity_registry[ins_registry_name] = ins
        return ins

    @staticmethod
    def make_registry_name(mod_name, cls_name, name):
        return f"{mod_name}:{cls_name}:{name}"

    @staticmethod
    def instance_by_name(cls, name):
        # Generate the registry name given class and object name
        ins_registry_name = EntityMeta.make_registry_name(cls.__module__, cls.__qualname__, name)

        # Find the object in the registry
        if ins_registry_name in EntityMeta._entity_registry:
            return EntityMeta._entity_registry[ins_registry_name]

        return None


class Entity(metaclass=EntityMeta):

    # def __new__(cls, name=None, *args, **kwargs):
    #
    #     # Create a dummy instance
    #     ins = object.__new__(cls)
    #     ins.__init__(name=name, *args, **kwargs)
    #
    #     # If name of instance is not given, then generate one.
    #     name = uuid.uuid4() if ins._name is None else ins._name
    #     iname = make_instance_name(cls.__module__, cls.__qualname__, name)
    #
    #     # Check if entity with the name already exists. If yes, return it.
    #     if iname in Entity._instances:
    #         old_entity = Entity._instances[iname]
    #         for key in kwargs:
    #             if key in old_entity.__dict__:
    #                 assert old_entity.__dict__[key] == kwargs[key], \
    #                     f"Entity creation failed. " \
    #                     f"There exists an entity with name={iname}. " \
    #                     f"But old_entity[{key}]={old_entity.__dict__[key]} does not match given " \
    #                     f"kwargs[{key}]={kwargs[key]}."
    #         return old_entity
    #
    #     # If entity with given name does not exist, then return the dummy instance
    #     Entity._instances[iname] = ins
    #     ins._name = name
    #     return ins

    def __init__(self, name=None, *args, **kwargs):

        # Initialize the Entity data structure only if uninitialized
        #   The only initialization should happen through __init__
        # if "_name" not in self.__dict__:
        self._name = name
        self._class_name = self.__class__.__qualname__
        self._module_name = self.__class__.__module__
        self.__dict__.update(kwargs)

        # Logger for logging purposes
        self.logger = logging.getLogger(self.__module__)
        self.logger.info(f"{self} is created.")

    def __eq__(self, other):
        return type(other) == type(self) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self._name})"

    def __str__(self):
        return self.__repr__()

    def __setattr__(self, key, value):
        try:        # AttributeError occurs when _name is set during instantiation (__init__)
            if key == "_name" and key in self.__dict__:
                self.logger.debug(f"Name of Entity is changed from {self._name} to {value}.")
        except AttributeError:
            pass

        return super(Entity, self).__setattr__(key, value)

    @property
    def name(self):
        return self._name

    @classmethod
    def get_object_by_name(cls, name):
        iname = make_instance_name(cls.__module__, cls.__qualname__, name)
        if iname in Entity._instances:
            return Entity._instances[iname]
        return None

    def serialize(self, ignores=None):
        ser_dict = self.__dict__.copy()
        ser_dict.pop("logger")

        if isinstance(ignores, Iterable):
            for item in ignores:
                ser_dict.pop(item)
        return ser_dict


if __name__ == '__main__':
    e1 = Entity()
    e2 = Entity("abhishek")
    print(id(e1) == id(e2))
    print(Entity.instance_by_name(Entity, "abhishek"))
