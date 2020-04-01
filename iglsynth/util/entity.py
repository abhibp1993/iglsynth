import logging
import uuid
import re

REGEX_IS_IGL_SERIAL_OUTPUT = re.compile(r"iglsynth{[a]}").match
DESERIALIZATRION_FAILURE = "DESERIALIZATION FAILURE"


class Entity(object):
    def __init__(self, name=None):
        # Entity data structure
        self._id = self._get_unique_id()
        self._name = name
        self._class_name = self.__class__.__qualname__
        self._module_name = self.__class__.__module__

        # Logger for logging purposes
        self.logger = logging.getLogger(self.__module__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.info(f"{self.__str__()} is created.")

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

    def serialize(self, ignores=None):
        return self.__dict__

    #     properties = self.__dict__
    #
    #     for name, value in list(properties.items()):
    #         # Ignore properties that shouldn't be serialized
    #         ignores = list() if ignores is None else list(ignores)
    #         if name in ignores + ["logger"]:
    #             properties.pop(name)
    #             continue
    #
    #         # Check if Python already has a serialization-deserialization protocol for the value-type
    #         try:
    #             if value != eval(repr(value)):
    #                 raise SyntaxError
    #             continue
    #
    #         except SyntaxError:
    #             pass
    #
    #         # If Python cannot serialize-deserialize value, then check whether value has serialize method defined.
    #         try:
    #             # Try serializing value
    #             #   If value is not an IGLSynth object, the following statement will raise AttributeError
    #             serial_out = value.serialize()
    #
    #             # Check if serialization is done by IGLSynth protocol or not.
    #             #   Many non-IGLSynth modules define serialize() function.
    #             #   IGLSynth does not handle deserialization of those data-types.
    #             if not REGEX_IS_IGL_SERIAL_OUTPUT(serial_out):
    #                 raise ValueError
    #
    #             properties[name] = serial_out
    #
    #         except AttributeError or ValueError:
    #             properties[name] = f"{DESERIALIZATRION_FAILURE} -> {repr(value)}"
    #             self.logger.debug(f"Improper serialization detected. "
    #                               f"{value} cannot be reconstructed from its representation {repr(value)}."
    #                               f"Deserialization may not work as expected.")
    #
    #     return properties
    #
    # @classmethod
    # def deserialize(cls, obj_dict):
    #     obj = cls()
    #
    #     for name, value in list(obj_dict.items()):
    #         pass

    @classmethod
    def _get_unique_id(cls):
        return f"{cls.__qualname__}::{uuid.uuid4()}"

