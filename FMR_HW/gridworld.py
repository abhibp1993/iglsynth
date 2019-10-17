from tsys import *


class Gridworld(TSys):
    def __init__(self, dim, conn, propositions: Iterable[AP] = None, labeling_func: Callable = None):
        assert conn in [4, 5, 8, 9], "Connectivity must be either 4, 5, 8 or 9."
        super(Gridworld, self).__init__(propositions, labeling_func)

        # Define vertex/edge properties
        self.add_vertex_property(name="is_obs", of_type="bool", default=False)
        self.add_vertex_property(name="is_bouncy_obs", of_type="bool", default=False)
        self.add_graph_property(name="dim", of_type="object")
        self.add_graph_property(name="conn", of_type="int")

        # Set values of properties
        self.set_graph_property(name="dim", value=dim)
        self.set_graph_property(name="conn", value=conn)

    def generate_graph(self):
        """
        Generates a graph of two-player turn-based grid world game
        based on dimension and connectivity information given.
        """
        # Create a new vertex property "cell_name" to store the
        # cell coordinate of p1, p2 and turn information.
        self.add_vertex_property(name="cell_name", of_type="object")

        # Get the dimensions of grid world to be generated
        rows, cols = self.get_graph_property(name="dim")

        # Compute and add the number of vertices in grid world.
        #   This is efficient way of adding vertices, than one-by-one in loop.
        num_vertices = rows**2 * cols**2 * 2
        self.add_vertices(num=num_vertices)


if __name__ == '__main__':
    print("Imports OK.")
    g = Gridworld(dim=(5, 5), conn=4)
