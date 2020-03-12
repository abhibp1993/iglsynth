//
// Created by abhibp1993 on 3/3/20.
//

#include "../util/entity.h"
#include "../util/graph.h"
#include "wrap_util.h"

using namespace IGLSynth;
void boost_bind_util(){

    namespace bp = boost::python;

    // map the core namespace to a sub-module
    // make "from ltlsynth.core import ____" work
    bp::object utilModule(bp::handle<>(bp::borrowed(PyImport_AddModule("iglsynth.util"))));

    // make "from ltlsynth import core" work
    bp::scope().attr("util") = utilModule;

    // set the current scope to the new sub-module
    bp::scope util_scope = utilModule;

    // Class Entity
    bp::class_<Entity>("_Entity")
        .add_property("id", &Entity::id)
        .def("to_string", &Entity::tostring)
        .def("serialize", &Entity::serialize)
        .def("__str__", &Entity::tostring)
        ;

    // Class Graph
    bp::class_<Graph, bp::bases<Entity>>("Graph")
        .def("num_edges", &Graph::num_edges)
        .def("num_vertices", &Graph::num_vertices)
        .def("is_multigraph", &Graph::is_multigraph)
        .def("add_edge", &Graph::add_edge)
        .def("serialize", &Graph::serialize)
        .def("deserialize", &Graph::deserialize)
        .def("__str__", &Graph::tostring)
        ;

    // Class Vertex
    bp::class_<Graph::Vertex, bp::bases<Entity>>("Vertex")
        .def("serialize", &Graph::Vertex::serialize)
        .def("deserialize", &Graph::Vertex::deserialize)
        ;

    // Class Edge
    bp::class_<Graph::Edge, bp::bases<Entity>>("Edge", bp::init<Graph::Vertex&, Graph::Vertex&>())
            .def("serialize", &Graph::Edge::serialize)
            .def("deserialize", &Graph::Edge::deserialize)
            ;
}