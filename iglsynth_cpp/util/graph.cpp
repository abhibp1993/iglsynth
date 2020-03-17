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
            auto u_ = boost::make_shared<Graph::Vertex>(u);
            auto v_ = boost::make_shared<Graph::Vertex>(v);

            auto it_u = Graph::vemap_out_.find(u_);
            auto it_v = Graph::vemap_in_.find(v_);

            // The iterators above look for shared pointers u_ v_ which do not match with
            // the shared pointers already existing in the vemap_in_ and vemap_out_ as a
            // result the iterators always go to map.end() and the below loop is never reached
            // This issue needs to be fixed.
            // Possible fix: check hash or id of the source, target vertex to the hash or id
            // of the vertices present in the map.

            if(it_u != Graph::vemap_out_.end() && it_v != Graph::vemap_in_.end()){
//                boost::unordered_set<boost::shared_ptr<Graph::Edge>> edge_ = Graph::vemap_in_[v_];
//                auto edge_in_ = Graph::vemap_in_[v_];
//                auto edge_out_ = Graph::vemap_out_[u_];
//                auto e_ = boost::make_shared<Graph::Edge>(*e);
//                edge_in_.insert(e_);
//                edge_out_.insert(e_);

                Graph::edges_.insert(e);
//                Graph::vemap_in_.insert(std::make_pair(v_, edge_in_));
//                Graph::vemap_out_.insert(std::make_pair(u_, edge_out_));
//                Graph::vemap_in_.insert(std::make_pair(v_, Graph::edges_));
//                Graph::vemap_out_.insert(std::make_pair(u_, Graph::edges_));
                Graph::vemap_in_[v_] = Graph::edges_;
                Graph::vemap_out_[u_] = Graph::edges_;
                std::cout << "Successfully added the edge" << std::endl;
                return true;
            }
            std::cout << "Tried adding the edge" << std::endl;
            return true;
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
    bool Graph::add_vertex(boost::shared_ptr<Graph::Vertex> u){
        /*
         * Return true: if added, false: if not added.
         * Adds a new vertex to graph.
         * An attempt to add existing vertex will be ignored, with a warning.
         */
        auto it_vemap_in = Graph::vemap_in_.find(u);
        auto it_vemap_out = Graph::vemap_out_.find(u);

        // If vertex is not already added, then add it.
        if(it_vemap_in == Graph::vemap_in_.end() && it_vemap_out == Graph::vemap_out_.end()){
//            auto edge_ = Graph::vemap_in_[u];
//            auto e_ = boost::make_shared<Graph::Edge>();
//            edge_.insert(e_);
//            Graph::vemap_in_.insert(std::make_pair(v_, edge_));

//            boost::shared_ptr<Graph::Edge> e(boost::make_shared<IGLSynth::Graph::Edge>());
//            boost::unordered_set<boost::shared_ptr<Graph::Edge>> e;
            Graph::vemap_in_.insert(std::make_pair(u, Graph::edges_));
            Graph::vemap_out_.insert(std::make_pair(u, Graph::edges_));
            std::cout << "Successfully added the vertex" << std::endl;
            return true;
        }
        else{
            std::cout << "The vertex is already present in the Graph. Ignoring request to add." << std::endl;
            return false;
        }

    }
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