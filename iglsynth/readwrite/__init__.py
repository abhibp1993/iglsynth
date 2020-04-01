import importlib
import logging
from datetime import datetime
from iglsynth.util.entity import Entity


if __name__ == '__main__':
    logging.basicConfig(filename="readwrite.log")

PRIMITIVE_DATATYPE = (bool, int, float, str, type(None))
ITERABLE_DATATYPE = (list, tuple, set, dict)


def get_fname(obj):
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%m-%H%M%S")

    if obj.name is not None:
        return f"{dt_string}-{obj.name}"
    else:
        return f"{dt_string}-{obj.id}"

def serialize(obj):
    # Setup a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    if type(obj) in PRIMITIVE_DATATYPE:
        return repr(obj)

    elif type(obj) in ITERABLE_DATATYPE:
        if type(obj) in (list, tuple, set):
            return repr(type(obj)([serialize(item) for item in obj]))
        else:   # type(obj) == dict
            return repr({serialize(item): serialize(obj[item]) for item in obj})

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
            module = importlib.import_module(mod_name)
        except ImportError as err:
            logger.exception(f"Cannot import module {mod_name} required to instantiate {dict_obj}.")
            raise err

        # Get the required class from imported module
        try:
            class_ = eval(f"module.{cls_name}")
        except KeyError as err:
            logger.exception(f"Cannot find {cls_name} class in module {mod_name} required to instantiate {dict_obj}.")
            print(f"Cannot find {cls_name} class in module {mod_name} required to instantiate {dict_obj}.")
            raise err

        # Ensure class_ is an Entity.
        #   At present (v1.0.0) we do not support deserialization of non-IGLSynth objects except PRIMITIVE_DATATYPE.
        assert issubclass(class_, Entity), f"Cannot deserialize an object of type {class_} as its not an {Entity}."

        # Instantiate an object of class
        try:
            obj = class_.instantiate_by_dict(dict_obj)
        except Exception as err:
            logger.exception(f"Could not instantiate object: obj = {class_}({dict_obj}).")
            raise err

        # Return new object
        return obj

    # Else (we expect a primitive/iterable python type)
    try:
        obj = eval(ser)

    except TypeError or SyntaxError:
        logger.error(f"Ill-constructed string for deserialization. "
                     f"Expected {[t for t in PRIMITIVE_DATATYPE]}, got {ser}.")
        raise TypeError(f"Ill-constructed string for deserialization. "
                        f"Expected {[t for t in PRIMITIVE_DATATYPE]}, got {ser}.")

    # If obj is primitive return it
    if type(obj) in PRIMITIVE_DATATYPE:
        return obj

    # Else, (we expect it to be iterable)
    elif type(obj) in ITERABLE_DATATYPE:
        if type(obj) in (list, tuple, set):
            return type(obj)([deserialize(item) for item in obj])
        else:  # type(obj) == dict
            return {deserialize(item): deserialize(obj[item]) for item in obj}


if __name__ == '__main__':
    from iglsynth.util.graph import Graph, Vertex, Edge

    g = Graph(name="MyGraph")
    v1 = Vertex()
    v2 = Vertex()
    e = Edge(u=v1, v=v2)
    g._edges.add(e)

    ser = serialize(g)
    print(f"ser\n\t{ser}")

    obj = deserialize(ser)
    print(f"obj\n\t{obj},\t{obj.__dict__}")
    print(f"\t{obj._edges}")

    for i in obj._edges: print(i)
