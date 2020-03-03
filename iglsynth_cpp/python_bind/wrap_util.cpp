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
        .def("serialize", &Graph::serialize)
        .def("deserialize", &Graph::deserialize)
        ;

    // Class Vertex
    bp::class_<Graph::Vertex, bp::bases<Entity>>("Vertex")
        .def("serialize", &Graph::Edge::serialize)
        .def("deserialize", &Graph::Edge::deserialize)
        ;

    // Class Edge
    bp::class_<Graph::Edge, bp::bases<Entity>>("Edge", bp::init<Graph::Vertex&, Graph::Vertex&>())
            .def("serialize", &Graph::Edge::serialize)
            .def("deserialize", &Graph::Edge::deserialize)
            ;
}