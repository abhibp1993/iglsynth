"""
Graph save-load interface.

Ref 1: https://github.com/hadim/pygraphml/blob/master/pygraphml/graphml_parser.py
"""

import inspect
from xml.etree.ElementTree import Element, ElementTree


class GraphMLParser:
    """
    GraphML Parser for IGLSynth :class:`Graph` objects.
    """
    NS_GRAPHML = "http://graphml.graphdrawing.org/xmlns"
    NS_XSI = "http://www.w3.org/2001/XMLSchema-instance"
    SCHEMA_LOCATION = 'http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd'
    XML_HEADER = {'xmlns': NS_GRAPHML, 'xmlns:xsi': NS_XSI, 'xsi:schemaLocation': SCHEMA_LOCATION}

    def __init__(self, graph):
        self._graph = graph
        self.xml = Element("graphml", self.XML_HEADER)

    def indent(self, elem, level=0):
        # in-place prettyprint formatter
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def add_graph_properties(self):
        # Add name of graph class
        xml_data = Element("data", key="classname")
        xml_data.text = str(self._graph.__class__)
        self.xml.append(xml_data)

        # Gather user-defined attributes of graph
        user_attr = [key for key in self._graph.__dict__.keys() if not key.startswith("__")]

        # Add all graph attributes
        for key in user_attr:
            # Do not save default properties of base class Graph.
            if key in ['_edges', '_vertex_edge_map', 'edges', 'vertices', 'num_edges', 'num_vertices']:
                continue

            # Add graph attributes to graphml
            try:
                # Get value of user-attribute
                value = eval(f"self._graph.{key}")

                # Create xml element and add the key-value pair
                xml_data = Element("data", key=key)
                xml_data.text = str(value)
                self.xml.append(xml_data)

            except NotImplementedError:
                continue

    def add_node(self, xml_graph, v):
        xml_graph_node = Element("node", id=str(v.name))
        user_attr = [key for key in dir(v) if not key.startswith("__")]

        for key in user_attr:
            # Add graph attributes to graphml
            try:
                # Check if key is a property
                if key in dir(type(v)):
                    if isinstance(eval(f"type(v).{key}"), property):
                        continue

                # Get value of user-attribute
                value = eval(f"v.{key}")

                # Create xml element and add the key-value pair
                xml_graph_node_data = Element("data", key=key)
                xml_graph_node_data.text = str(value)
                xml_graph_node.append(xml_graph_node_data)

            except NotImplementedError:
                continue

        xml_graph.append(xml_graph_node)

    def add_edge(self, xml_graph, e):
        xml_graph_edge = Element("edge", id=str(e.name))
        user_attr = [key for key in dir(e) if not key.startswith("__")]

        for key in user_attr:
            # Add graph attributes to graphml
            try:
                # Check if key is a property
                if key in dir(type(e)):
                    if isinstance(eval(f"type(e).{key}"), property):
                        continue

                # Get value of user-attribute
                value = eval(f"e.{key}")

                # Create xml element and add the key-value pair
                xml_graph_edge_data = Element("data", key=key)
                xml_graph_edge_data.text = str(value)
                xml_graph_edge.append(xml_graph_edge_data)

            except NotImplementedError:
                continue

        xml_graph.append(xml_graph_edge)

    def write(self, fname):
        """
        Generate GraphML file for given graph object.
        """
        # xml = Element("graphml", self.XML_HEADER)

        # In IGLSynth we deal with only directed graphs
        xml_graph = Element("graph", edgedefault='directed')
        self.xml.append(xml_graph)

        # Add graph class properties/attributes
        self.add_graph_properties()

        # Add nodes of graph
        for v in self._graph.vertices:
            self.add_node(xml_graph=xml_graph, v=v)

        # Add edges of graph
        for e in self._graph.edges:
            self.add_edge(xml_graph=xml_graph, e=e)

        # Generate document
        self.indent(self.xml)
        document = ElementTree(self.xml)
        document.write(fname, encoding='utf-8', xml_declaration=True)
