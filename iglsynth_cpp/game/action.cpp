//
// Created by abhibp1993 on 2/25/20.
//

#include "action.h"
#include <iostream>


IGLSynth::Action::Action(const std::string &name, std::string& desc) {
    std::cout << "Constructing Action " << name << " " << desc << std::endl;
}

void IGLSynth::Action::apply(IGLSynth::Graph::Vertex &, IGLSynth::Graph::Vertex &) {
    std::cout << "applying Action " << std::endl;

}

IGLSynth::IGLMap IGLSynth::Action::serialize() {
    IGLMap ser;
    ser = Entity::serialize();
    ser["desc"] = desc;
    return ser;
}

void IGLSynth::Action::deserialize(IGLSynth::IGLMap ser) {
    Entity::deserialize(ser);
    desc = std::get<std::string>(ser["desc"]);
}
