//
// Created by abhibp1993 on 2/23/20.
//

#ifndef IGLSYNTH_GRAPH_H
#define IGLSYNTH_GRAPH_H

#include "types.h"
#include "entity.h"
//#include <unordered_map>
//#include <unordered_set>
#include <vector>
#include <boost/shared_ptr.hpp>
#include <boost/unordered_set.hpp>
#include <boost/unordered_map.hpp>



namespace IGLSynth {
    class Graph : public Entity {

    public: // Classes
        class Vertex : public Entity {

        };

        class Edge : public Entity {

            protected:
                Vertex source_;
                Vertex target_;

            public:
                // constructor
                Edge(Vertex& u, Vertex& v) : source_(u), target_(v) {}

                // methods
                Vertex source(Edge& e){
                    return e.source_;
                }

                Vertex target(Edge& e){
                    return e.target_;
                }
        };


    protected:  // Variables

        // TODO Check how to use the following boost map, set.
        //      Also consider the effect of these objects under python binding.
        boost::unordered_set<boost::shared_ptr<Edge>> edges_;
        boost::unordered_map<boost::shared_ptr<Vertex>, boost::shared_ptr<Edge>> vemap_;


    public: // Properties
        // Read-only properties
        int num_edges();
        int num_vertices();
        std::vector<Edge> edges();                  // TODO: Should this return iterator?
        std::vector<Edge> vertices();               // TODO: Should this return iterator?
        bool is_multigraph();


    public: // Methods
        // Constructor
        Graph() {class_name_ = __PRETTY_FUNCTION__;}

        // Input-Output
        IGLMap serialize();                         // TODO: Can we replace IGLMap with boost::property_map?
        void deserialize(IGLMap ser);               // Will initialize "this" object.
//        std::string to_string();

        // Containment checking
//        bool contains_vertex(Vertex& u);
//        bool contains_edge(Edge& e);
//
//        // Graph manipulation
//        bool add_edge(Edge& e);                     // Return true: if added, false: if not added.
//        bool add_edges(std::vector<Edge>& e);       // Return true: if added, false: if not added.
//        bool add_vertex(Vertex& u);                 // Return true: if added, false: if not added.
//        bool add_vertices(std::vector<Vertex>& e);  // Return true: if added, false: if not added.
//
//        bool rem_edge(Edge& e);                     // Return true: if added, false: if not added.
//        bool rem_edges(std::vector<Edge>& e);       // Return true: if added, false: if not added.
//        bool rem_vertex(Vertex& u);                 // Return true: if added, false: if not added.
//        bool rem_vertices(std::vector<Vertex>& e);  // Return true: if added, false: if not added.
//
//        std::vector<Edge>& get_edges(Vertex& u);
//        std::vector<Edge>& get_edges(Vertex& u, Vertex& v);
//        std::vector<Edge>& get_in_edges(Vertex& v);
//        std::vector<Edge>& get_out_edges(Vertex& u);
//        std::vector<Edge>& get_neighbors(Vertex& u);
//        std::vector<Edge>& get_in_neighbors(Vertex& v);
//        std::vector<Edge>& get_out_neighbors(Vertex& u);

    };  // End of class Graph



    class SubGraph : public Graph {

    protected:
        boost::unordered_set<boost::shared_ptr<Vertex>> vfilt_;
        boost::unordered_set<boost::shared_ptr<Vertex>> efilt_;

    public: // Methods

        // Constructor
        // TODO: Might merge the following two constructors into a single.
        SubGraph(Graph& g);
        SubGraph(SubGraph& g);

        // Containment checking
        // TODO: These functions are key to filtering.
        bool contains_vertex(Vertex& u);
        bool contains_edge(Edge& e);

        // Graph manipulation
        // TODO: While adding new edge to sub-graph, remember to add it to vfilt/efilt if not already done.
        bool add_edge(Edge& e);                     // Return true: if added, false: if not added.
        bool add_edges(std::vector<Edge>& e);       // Return true: if added, false: if not added.
        bool add_vertex(Vertex& u);                 // Return true: if added, false: if not added.
        bool add_vertices(std::vector<Vertex>& e);  // Return true: if added, false: if not added.

        // TODO(Think) Should removal operation only remove edge from v/e-filt or from base graph?
        bool rem_edge(Edge& e);                     // Return true: if added, false: if not added.
        bool rem_edges(std::vector<Edge>& e);       // Return true: if added, false: if not added.
        bool rem_vertex(Vertex& u);                 // Return true: if added, false: if not added.
        bool rem_vertices(std::vector<Vertex>& e);  // Return true: if added, false: if not added.

        // TODO (Think) We need not override get_**** methods because containment checking will take care of it.
        // TODO (Think) Does everything remain good if we construct a sub-graph of sub-graph?
    };
}

#endif //IGLSYNTH_GRAPH_H
