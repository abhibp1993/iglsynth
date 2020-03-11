//
// Created by abhibp1993 on 3/7/20.
//

#include <iostream>
#include "util/graph.h"

int main(){

    IGLSynth::Graph g;
    // v1, v2, v3 are shared pointers to vertex objects
    boost::shared_ptr<IGLSynth::Graph::Vertex> v1(boost::make_shared<IGLSynth::Graph::Vertex>());
    boost::shared_ptr<IGLSynth::Graph::Vertex> v2(boost::make_shared<IGLSynth::Graph::Vertex>());
    boost::shared_ptr<IGLSynth::Graph::Vertex> v3(boost::make_shared<IGLSynth::Graph::Vertex>());
    // e1, e2 are shared pointers to edges connecting v1, v2 and v1, v3
    boost::shared_ptr<IGLSynth::Graph::Edge> e1(boost::make_shared<IGLSynth::Graph::Edge>(*v1, *v2));
    boost::shared_ptr<IGLSynth::Graph::Edge> e2(boost::make_shared<IGLSynth::Graph::Edge>(*v1, *v3));
    // Insert edges e1, e2 into IGLSynth::Graph object g
    g.edges_.insert(e1);
    g.edges_.insert(e2);
    g.vemap_[v1] = boost::make_shared<IGLSynth::Graph::Edge>(*e1);
//    g.vemap_[v2] = (boost::unordered_set<boost::shared_ptr<Edge>>, boost::unordered_set<boost::shared_ptr<Edge>>);
//    g.vemap_[v3] = (boost::unordered_set<boost::shared_ptr<Edge>>, boost::unordered_set<boost::shared_ptr<Edge>>);

    std::cout << v1 << " " << v2 << " " << e1 << " " << e2 << std::endl;
    std::cout << g.tostring() << std::endl;
    std::cout << g.num_edges() << std::endl;
    std::cout << g.num_vertices() << std::endl;
//    std::cout << v1.tostring() << std::endl;
//    std::cout << v2.tostring() << std::endl;
//    std::cout << e.tostring() << std::endl;
}