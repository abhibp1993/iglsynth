//
// Created by abhibp1993 on 3/7/20.
//

#include <iostream>
#include "util/graph.h"

int main(){

    IGLSynth::Graph g;
    std::shared_ptr<IGLSynth::Graph::Vertex> v1, v2;
    std::shared_ptr<IGLSynth::Graph::Edge> e = ;

    g.edges_.insert(e);

    std::cout << g.to_string() << std::endl;
    std::cout << v1.tostring() << std::endl;
    std::cout << v2.tostring() << std::endl;
    std::cout << e.tostring() << std::endl;
}