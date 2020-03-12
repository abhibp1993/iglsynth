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
    boost::shared_ptr<IGLSynth::Graph::Vertex> v4(boost::make_shared<IGLSynth::Graph::Vertex>());

    // e1, e2 are shared pointers to edges connecting v1, v2 and v1, v3
    boost::shared_ptr<IGLSynth::Graph::Edge> e1(boost::make_shared<IGLSynth::Graph::Edge>(*v1, *v2));
    boost::shared_ptr<IGLSynth::Graph::Edge> e2(boost::make_shared<IGLSynth::Graph::Edge>(*v1, *v3));
    boost::shared_ptr<IGLSynth::Graph::Edge> e3(boost::make_shared<IGLSynth::Graph::Edge>(*v2, *v3));
    boost::shared_ptr<IGLSynth::Graph::Edge> e4(boost::make_shared<IGLSynth::Graph::Edge>(*v3, *v4));

    // Insert edges e1, e2,.. into IGLSynth::Graph object g
    g.add_edge(e1);
    g.add_edge(e2);
    g.add_edge(e2);
    g.add_edge(e3);
    g.add_edge(e4);
    // Update the vertex edge map
    g.vemap_[v1] = boost::make_shared<IGLSynth::Graph::Edge>(*e1);
    g.vemap_[v1] = boost::make_shared<IGLSynth::Graph::Edge>(*e2);
    g.vemap_[v2] = boost::make_shared<IGLSynth::Graph::Edge>(*e1);
    g.vemap_[v2] = boost::make_shared<IGLSynth::Graph::Edge>(*e3);
    g.vemap_[v3] = boost::make_shared<IGLSynth::Graph::Edge>(*e2);
    g.vemap_[v3] = boost::make_shared<IGLSynth::Graph::Edge>(*e3);
    g.vemap_[v3] = boost::make_shared<IGLSynth::Graph::Edge>(*e4);

    std::cout << g.tostring() << std::endl;
    std::cout << "Number of edges: " << g.num_edges() << std::endl;
    std::cout << "Number of vertices: " << g.num_vertices() << std::endl;

    // Iterate over the Vertex-Edge map to return pointers to the Vertex-Edge objects
    for(auto &i: g.vemap_){
        std::cout << i.first->id() << " " << i.second->tostring() << std::endl;
    }

//    std::cout << v1.tostring() << std::endl;
//    std::cout << v2.tostring() << std::endl;
//    std::cout << e.tostring() << std::endl;
}