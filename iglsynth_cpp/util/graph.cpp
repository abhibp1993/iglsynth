//
// Created by abhibp1993 on 2/23/20.
//

#include "types.h"
#include "graph.h"
#include <iostream>

namespace IGLSynth {

    // Read-Only Properties
    int Graph::num_edges(){
        std::cerr << "Not Implemented Error" << std::endl;
    }

    int Graph::num_vertices(){
        std::cerr << "Not Implemented Error" << std::endl;
    }

    bool Graph::is_multigraph(){
        std::cerr << "Not Implemented Error" << std::endl;
    }


    IGLMap Graph::serialize(){

    }

    void Graph::deserialize(IGLMap ser){

    }

//    std::string to_string();

//    // Containment checking
//    bool contains_vertex(Vertex &u);
//    bool contains_edge(Edge &e);
//
//    // Graph manipulation
//    bool add_edge(Edge &e);                     // Return true: if added, false: if not added.
//    bool add_edges(std::vector<Edge> &e);       // Return true: if added, false: if not added.
//    bool add_vertex(Vertex &u);                 // Return true: if added, false: if not added.
//    bool add_vertices(std::vector<Vertex> &e);  // Return true: if added, false: if not added.
//
//    bool rem_edge(Edge &e);                     // Return true: if added, false: if not added.
//    bool rem_edges(std::vector<Edge> &e);       // Return true: if added, false: if not added.
//    bool rem_vertex(Vertex &u);                 // Return true: if added, false: if not added.
//    bool rem_vertices(std::vector<Vertex> &e);  // Return true: if added, false: if not added.
//
//    std::vector<Edge> &get_edges(Vertex &u);
//
//    std::vector<Edge> &get_edges(Vertex &u, Vertex &v);
//
//    std::vector<Edge> &get_in_edges(Vertex &v);
//
//    std::vector<Edge> &get_out_edges(Vertex &u);
//
//    std::vector<Edge> &get_neighbors(Vertex &u);
//
//    std::vector<Edge> &get_in_neighbors(Vertex &v);
//
//    std::vector<Edge> &get_out_neighbors(Vertex &u);

}