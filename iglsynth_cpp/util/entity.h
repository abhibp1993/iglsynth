//
// Created by abhibp1993 on 2/23/20.
//

#ifndef IGLSYNTH_ENTITY_H
#define IGLSYNTH_ENTITY_H

#include "types.h"
#include <boost/uuid/uuid.hpp>
#include <boost/uuid/uuid_generators.hpp>
#include <boost/uuid/uuid_io.hpp>
#include <stdexcept>


namespace IGLSynth {


    class Entity {

    protected:  // Class Variables
        std::string id_;
        std::string class_name_;

    public:     // Class Methods
        Entity() : id_(to_string(boost::uuids::random_generator()())), class_name_(__PRETTY_FUNCTION__) {}

        std::string id() {
            return id_;
        }

        std::size_t hash() {
            return std::hash<std::string>{}(id_);
        }

        std::string tostring() {
            return "<" + class_name_ + " object with ID=" + id_ + ">";
        }

        virtual IGLMap serialize() {
            IGLMap ser;
            ser["id"] = id_;
            ser["__class__"] = class_name_;
            return ser;
        }

        virtual Entity deserialize(IGLMap ser) {
            std::string tmp_id = std::get<std::string>(ser["id"]);
            std::string tmp_class = std::get<std::string>(ser["__class__"]);

            if (tmp_class != "Entity"){
                throw std::runtime_error("error");      // TODO: Change the Error type and string later.
            }

            Entity e;
            e.id_ = tmp_id;
            e.class_name_ = tmp_class;
            return e;
        }

        inline bool operator==(const Entity& rhs){
            return id_ == rhs.id_;
        }
    };  // Entity Class
}  // namespace

#endif //IGLSYNTH_ENTITY_H
