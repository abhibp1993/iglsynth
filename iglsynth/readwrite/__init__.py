import importlib
import logging
from iglsynth.util.entity import Entity

if __name__ == '__main__':
    logging.basicConfig(filename="readwrite.log")

PRIMITIVE_DATATYPE = (bool, int, float, str, list, tuple, set, dict, type(None))


def serialize(obj):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    if type(obj) in PRIMITIVE_DATATYPE:
        return repr(obj)

    elif isinstance(obj, Entity):
        obj_dict = obj.serialize()

        for name, value in list(obj_dict.items()):
            try:
                obj_dict[name] = serialize(value)
            except TypeError:
                obj_dict.pop(name)

        return f"IGL{obj_dict}"

    else:
        logger.warning(f"Cannot serialize {obj} of type {type(obj)}.")
        raise TypeError(f"Cannot serialize {obj} of type {type(obj)}.")


def deserialize(ser):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    if ser[0:3] == "IGL":
        ser = ser[3:]
        dict_obj = eval(ser)
        assert isinstance(dict_obj, dict), f"Ill-constructed string for deserialization. Expected dict, got {dict_obj}."

        for name, value in dict_obj.items():
            dict_obj[name] = deserialize(value)

        # Find the correct module and class to instantiate object
        cls_name = dict_obj["_class_name"]
        mod_name = dict_obj["_module_name"]

        # Get the module in iglsynth
        try:
            importlib.import_module(mod_name)
        except ImportError as err:
            logger.exception(f"Cannot import module {mod_name} required to instantiate {dict_obj}.")
            raise err

        # Get the required class from imported module
        try:
            class_ = globals()[cls_name]
        except KeyError as err:
            logger.exception(f"Cannot find {cls_name} class in module {mod_name} required to instantiate {dict_obj}.")
            raise err

        # Instantiate an object of class
        try:
            obj = class_()
        except Exception as err:
            logger.exception(f"Could not instantiate object: obj = {class_}().")
            raise err

        # Update object's internal representation
        obj.__dict__ = dict_obj

        # Return new object
        return obj

    # Else (we expect a primitive python type)
    try:
        return eval(ser)

    except TypeError or SyntaxError:
        logger.error(f"Ill-constructed string for deserialization. "
                     f"Expected {[t for t in PRIMITIVE_DATATYPE]}, got {ser}.")
        raise TypeError(f"Ill-constructed string for deserialization. "
                        f"Expected {[t for t in PRIMITIVE_DATATYPE]}, got {ser}.")


if __name__ == '__main__':
    from iglsynth.util.graph import Graph, Vertex

    g = Graph(name="MyGraph")
    g._edges = Vertex()

    ser = serialize(g)
    print(f"ser\n\t{ser}")

    obj = deserialize(ser)
    print(f"obj\n\t{obj}")
    print(f"\t{obj._edges}")
