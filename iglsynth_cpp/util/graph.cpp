//
// Created by abhibp1993 on 2/23/20.
//

#include "types.h"
#include "graph.h"
#include <iostream>
#include <stdexcept>
// uncomment to disable assert()
// #define NDEBUG
#include <cassert>

namespace IGLSynth {

    // Read-Only Properties
    int Graph::num_edges(){
        return Graph::edges_.size();
    }

    int Graph::num_vertices(){
        assert(Graph::vemap_in_.size() == Graph::vemap_out_.size());
        return Graph::vemap_in_.size();
    }

    bool Graph::is_multigraph(){
        std::cerr << "Not Implemented Error" << std::endl;
    }
    
    std::string Graph::tostring(){
        return "<" + class_name_ + " object with id=" + id_ + ">";
    }

    // Containment checking
//    bool Graph::contains_vertex(Vertex &u);


//    bool contains_edge(Edge &e);
//
    // Graph manipulation
    bool Graph::add_edge(boost::shared_ptr<Graph::Edge> e){

        // Return true: if added, false: if not added.
        try{
            // Edge already present in Graph
            if(Graph::edges_.find(e) != Graph::edges_.end()){
                std::cout << "The edge is already present in the Graph. Ignoring request to add." << std::endl;
                return false;
            }
            // Edge not present in Graph
//            if(Graph::edges_.find(e) == Graph::edges_.end()){
//                Graph::edges_.insert(e);
//                std::cout << "Successfully added the edge" << std::endl;
//                return true;
//            }

            Graph::Vertex u = Graph::Edge::source(*e);
            Graph::Vertex v = Graph::Edge::target(*e);

            auto it_u = Graph::vemap_out_.find(boost::make_shared<IGLSynth::Graph::Vertex>(v));
            auto it_v = Graph::vemap_in_.find(boost::make_shared<IGLSynth::Graph::Vertex>(u));

            if(it_u != Graph::vemap_out_.end() && it_v != Graph::vemap_in_.end()){
//                boost::unordered_set<boost::shared_ptr<Graph::Edge>> edge_ = Graph::vemap_in_[v_];
                auto v_ = boost::make_shared<Graph::Vertex>(v);
                auto edge_ = Graph::vemap_in_[v_];
                auto e_ = boost::make_shared<Graph::Edge>(*e);
                edge_.insert(e_);
                Graph::vemap_in_.insert(std::make_pair(v_, edge_));
                std::cout << "Successfully added the edge" << std::endl;
                return true;
            }

        }
        catch(std::exception& ep){
            // Catch standard exceptions
            std::cout << "Error adding the Edge, exception : " << ep.what() << std::endl;
            return false;
        }
        catch(...){
            // Catch any other exception
            std::cout << "Error adding the Edge, some other exception occurred" << std::endl;
            return false;
        }

    }
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