//
// Created by abhibp1993 on 3/3/20.
//

#include "../game/action.h"
#include "wrap_game.h"

using namespace IGLSynth;
void boost_bind_game(){

    namespace bp = boost::python;

    // map the core namespace to a sub-module
    // make "from ltlsynth.core import ____" work
    bp::object gameModule(bp::handle<>(bp::borrowed(PyImport_AddModule("iglsynth.game"))));

    // make "from ltlsynth import core" work
    bp::scope().attr("game") = gameModule;

    // set the current scope to the new sub-module
    bp::scope util_scope = gameModule;

    // Import Classes, Functions
    bp::class_<Action, bp::bases<Entity>>("Action", bp::init<const std::string, std::string>())
        .def_readwrite("desc", &Action::desc)
        .def("serialize", &Entity::serialize)
        .def("deserialize", &Entity::deserialize)
        ;
}