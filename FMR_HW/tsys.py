from kripke import *


class TSys(Kripke):
    def __init__(self, propositions: Iterable[AP] = None, labeling_func: Callable = None):
        super(TSys, self).__init__(propositions, labeling_func)

        # Define vertex/edge properties
        self.add_vertex_property(name="is_p1_turn", of_type="bool", default=False)
        self.add_vertex_property(name="is_init", of_type="bool", default=False)
        self.add_edge_property(name="action", of_type="object", default=None)

    @property
    def init_state(self):
        for v in self.vertices:
            if self.get_vertex_property(name="is_init", vid=st):
                return v

    def initialize(self, st):
        self.set_vertex_property(name="is_init", vid=st, value=True)


if __name__ == '__main__':
    print("Imports OK")