import inspect
import logging
import uuid


__all__ = ["Entity"]


class Entity(object):
    def __init__(self, name=None):
        # Entity data structure
        self._id = self._get_unique_id()
        self._name = name
        self._class_name = self.__class__.__qualname__
        self._module_name = self.__class__.__module__

        # Logger for logging purposes
        self.logger = logging.getLogger(self.__module__)
        self.logger.info(f"{self} is created.")

    def __eq__(self, other):
        # FIXME: Should two objects of different classes be comparable?
        if self._name is None:
            return isinstance(other, self.__class__) and self._id == other._id

        return isinstance(other, self.__class__) and self._name == other._name

    def __hash__(self):
        if self._name is None:
            return hash(self._id)

        return hash(self._name)

    def __repr__(self):
        if self._name is None:
            return f"<{self.__class__.__name__} object with id={self._id}>"

        return f"<{self.__class__.__name__} object with name={self._name}>"

    def __str__(self):
        if self._name is None:
            return f"<{self.__class__.__name__} object with id={self._id}>"

        return f"<{self.__class__.__name__} object with name={self._name}>"

    @classmethod
    def _get_unique_id(cls):
        return f"{cls.__qualname__}::{uuid.uuid4()}"

    @classmethod
    def instantiate_by_dict(cls, obj_dict):
        logger = logging.getLogger(cls.__module__)

        # Detect init signature
        sig = inspect.signature(cls.__init__)
        init_attr = dict()
        for attr_name in sig.parameters.keys():
            if attr_name == "self":
                continue

            try:
                # Remark: While reconstructing the object from dictionary, default parameter values cannot be used.
                init_attr[attr_name] = obj_dict[attr_name] if attr_name in obj_dict else obj_dict[f"_{attr_name}"]
            except KeyError as err:
                logger.exception(err)
                raise err

        # If all parameters are values are available,
        obj = cls(**init_attr)
        obj.__dict__.update(obj_dict)
        logger.info(f"New {cls} object {obj} instantiated. Dictionary initialized to {obj_dict}.")
        return obj

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def serialize(self, ignores=None):
        ser_dict = self.__dict__.copy()
        ser_dict.pop("logger")
        return ser_dict

