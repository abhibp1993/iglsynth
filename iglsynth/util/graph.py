"""
iglsynth: graph.py

License goes here...
"""

from typing import Iterable, Iterator, List, Union
from functools import reduce
import warnings

import iglsynth.util.entity as entity


class Graph(entity.Entity):

    def __init__(self, name=None):
        # super(Graph, self).__init__(id=name)

        # Graph data structure
        self._gprop = dict()
        self._edges = set()
        self._ve_map_in = dict()
        self._ve_map_out = dict()

    def __getattr__(self, name):
        return self._gprop[name]

    def __setattr__(self, name, value):
        # Let Python do it's usual work
        super(Graph, self).__setattr__(name, value)

        # Explicitly define which data structure elements should not be added to gprops
        not_to_add_gprop = ["_gprop", "_edges", "_ve_map_in", "_ve_map_out"]

        # Add elements to gprops
        if name not in not_to_add_gprop:
            self._gprop[name] = value

    def __repr__(self):
        # Build representation dictionary
        repr_dict = {"igl_class": self.__class__.__qualname__}
        repr_dict.update(self._gprop)

        # Recursively convert all values to their representation
        for key in repr_dict:
            value = repr_dict[key]
            repr_value = repr(repr_dict[key])

            if eval(repr_value) != value:
                # Add a log warning that representation is failing.
                pass

            repr_dict[key] = repr(repr_dict[key])

        # Return representation dictionary
        return str(repr_dict)


g = Graph()
g.hello = 10

repr_str = g.__repr__()
print(repr_str)
