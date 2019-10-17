from typing import Callable, Iterable
from iglsynth.util.graph import *
from iglsynth.logic.core import *


class Kripke(Graph):
    def __init__(self, propositions: Iterable[AP] = None, labeling_func: Callable = None):
        super(Kripke, self).__init__()

        # TODO: Validate labeling_func signature

        # Define graph properties
        self.add_graph_property(name="propositions", of_type="object")
        self.set_graph_property(name="propositions", value=propositions)

        self.add_graph_property(name="labeling_func", of_type="object")
        self.set_graph_property(name="labeling_func", value=labeling_func)

    def label_state(self, st: int) -> set:
        propositions = self.get_graph_property(name="propositions")
        labeling_func = self.get_graph_property(name="labeling_func")
        return labeling_func(graph=self, st=st, propositions=propositions)

    def label_graph(self) -> dict:
        label = dict()
        for st in self.vertices:
            label[st] = self.label_state(st)

        return label

