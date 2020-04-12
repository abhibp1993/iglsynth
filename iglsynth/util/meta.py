class EntityMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        ins = super(EntityMeta, cls).__call__(*args, **kwargs)
        name = ins._name
        print(f"__call__: ins.name = {name}")
        return ins


class Entity(metaclass=EntityMeta):
    _instances = {}

    def __init__(self, *args, **kwargs):
        name = kwargs["name"]
        self._name = name


e1 = Entity(name="Hello")
e2 = Entity(name="Hello")

print(id(e1))
print(id(e2))