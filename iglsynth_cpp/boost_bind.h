//
// Created by abhibp1993 on 3/3/20.
//

#ifndef IGLSYNTH_BOOST_BIND_H
#define IGLSYNTH_BOOST_BIND_H

#include <boost/python.hpp>
#include <boost/python/object.hpp>
#include <boost/python/list.hpp>
#include <boost/python/tuple.hpp>
#include <boost/python/extract.hpp>
#include <boost/python/to_python_converter.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

#include "python_bind/wrap_util.h"
#include "python_bind/wrap_game.h"

#define IGLSYNTH_FRAMEWORK_VERSION  "1.0.0"

// Current version of ltlsynth framework
std::string version() { return IGLSYNTH_FRAMEWORK_VERSION; }


// How to create modules:
// http://isolation-nation.blogspot.com/2008/09/packages-in-python-extension-modules.html
BOOST_PYTHON_MODULE(iglsynth){
    namespace bp = boost::python;
    bp::def("version", version);

    // Specify that this module is actually a package
    bp::object module = bp::scope();
    module.attr("__path__") = "iglsynth";

    // Export core sub-module
    boost_bind_util();
    boost_bind_game();
}


#endif //IGLSYNTH_BOOST_BIND_H
