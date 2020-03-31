import uuid


class Entity(object):
    def __init__(self, name=None):
        # Entity data structure
        self._id = self._get_unique_id()
        self._name = name
        self._class_name = self.__class__.__qualname__

    def __eq__(self, other):
        if self._name is None:
            return isinstance(other, self.__class__) and self._id == other._id

        return isinstance(other, self.__class__) and self._name == other._name

    def __hash__(self):
        if self._name is None:
            return hash(self._id)

        return hash(self._name)

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        if self._name is None:
            return f"<{self.__class__.__name__} object with id={self._id}>"

        return f"<{self.__class__.__name__} object with name={self._name}>"

    def serialize(self):
        for key, value in self.__dict__.items():
            if value != eval(repr(value)):
                print(f"Improper serialization detected. "
                      f"{value} cannot be reconstructed from its representation {repr(value)}."
                      f"Deserialization may not work as expected.")

        return self.__repr__()

    @classmethod
    def _get_unique_id(cls):
        return f"{cls.__qualname__}::{uuid.uuid4()}"

    @classmethod
    def deserialize(cls, obj_dict):
        if obj_dict['_class_name'] != cls.__qualname__:
            raise TypeError(f"Cannot deserialize {obj_dict['_class_name']} into {cls.__qualname__} class.")

        new_obj = cls()
        for name, value in obj_dict.items():
            new_obj.__setattr__(name, value)

        return new_obj

