//
// Created by abhibp1993 on 3/7/20.
//

#include <iostream>
#include "util/graph.h"

int main(){

    IGLSynth::Graph g;
    // v1 and v2 are shared pointers to vertex objects
    boost::shared_ptr<IGLSynth::Graph::Vertex> v1(boost::make_shared<IGLSynth::Graph::Vertex>());
    boost::shared_ptr<IGLSynth::Graph::Vertex> v2(boost::make_shared<IGLSynth::Graph::Vertex>());
    // e is shared pointer to edge connecting v1 and v2
    boost::shared_ptr<IGLSynth::Graph::Edge> e(boost::make_shared<IGLSynth::Graph::Edge>(*v1, *v2));
    // Insert edge e into IGLSynth::Graph object g
    g.edges_.insert(e);
    
    std::cout << v1 << " " << v2 << " " << e << std::endl;
    std::cout << g.tostring() << std::endl;
//    std::cout << v1.tostring() << std::endl;
//    std::cout << v2.tostring() << std::endl;
//    std::cout << e.tostring() << std::endl;
}