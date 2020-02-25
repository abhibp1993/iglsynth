//
// Created by abhibp1993 on 2/23/20.
//

#ifndef IGLSYNTH_GRAPH_H
#define IGLSYNTH_GRAPH_H

#include "types.h"
#include "entity.h"
#include <unordered_map>
#include <unordered_set>
#include <vector>



namespace IGLSynth {
    class Graph : protected Entity {

    public: // Classes
        class Vertex : protected Entity {

        };

        class Edge : protected Entity {

        };


    protected:  // Variables

        // TODO Think about whether this is the format we want to use?
        std::unordered_map<std::string, Vertex&> vertices_;
        std::unordered_map<std::string, Edge&> edges_;
        std::unordered_map<std::string, std::string> v_e_map_in_;     // vertex to in-edges map
        std::unordered_map<std::string, std::string> v_e_map_out_;    // vertex to in-edges map


    public: // Properties
        // Read-only properties
        int num_edges();
        int num_vertices();
        std::vector<Edge> edges();                  // TODO: Should we return iterators?
        std::vector<Edge> vertices();
        bool is_multigraph();


    public: // Methods
        // Constructor
        Graph();

        // IO
        IGLMap serialize();                     // TODO: Can we replace IGLMap with boost::property_map?
        void deserialize(IGLMap ser);
        std::string to_string();

        // Containment checking
        bool contains_vertex(Vertex& u);
        bool contains_edge(Edge& e);

        // Graph manipulation
        bool add_edge(Edge& e);                     // Return true: if added, false: if not added.
        bool add_edges(std::vector<Edge>& e);       // Return true: if added, false: if not added.
        bool add_vertex(Vertex& u);                 // Return true: if added, false: if not added.
        bool add_vertices(std::vector<Vertex>& e);  // Return true: if added, false: if not added.

        bool rem_edge(Edge& e);                     // Return true: if added, false: if not added.
        bool rem_edges(std::vector<Edge>& e);       // Return true: if added, false: if not added.
        bool rem_vertex(Vertex& u);                 // Return true: if added, false: if not added.
        bool rem_vertices(std::vector<Vertex>& e);  // Return true: if added, false: if not added.

        std::vector<Edge>& get_edges(Vertex& u);
        std::vector<Edge>& get_edges(Vertex& u, Vertex& v);
        std::vector<Edge>& get_in_edges(Vertex& v);
        std::vector<Edge>& get_out_edges(Vertex& u);
        std::vector<Edge>& get_neighbors(Vertex& u);
        std::vector<Edge>& get_in_neighbors(Vertex& v);
        std::vector<Edge>& get_out_neighbors(Vertex& u);

    };
}

#endif //IGLSYNTH_GRAPH_H
