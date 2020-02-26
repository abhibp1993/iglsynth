//
// Created by abhibp1993 on 2/25/20.
//

#ifndef IGLSYNTH_ACTION_H
#define IGLSYNTH_ACTION_H

#include "../util/graph.h"
#include "../util/types.h"
#include "../util/entity.h"
#include <functional>


namespace IGLSynth{

    /**
     * Action is a functional that returns a new state when it applied to
     */
    class Action : public Entity {

    public:     // Variables
        std::string desc = "No description given by user.";
        std::function<bool(Graph&, Graph::Vertex&)> pre;
        std::function<bool(Graph&, Graph::Vertex&)> act;
        std::function<void(Graph::Vertex&, Graph::Vertex&)> post;

    public:     // Methods

        // Constructor
        explicit Action(const std::string &name, std::string &desc);

        // Input-Output
        IGLMap serialize() override;
        void deserialize(IGLMap ser) override;

        // Apply action to a graph vertex
        void apply(Graph::Vertex&, Graph::Vertex&);

    };
}


#endif //IGLSYNTH_ACTION_H
