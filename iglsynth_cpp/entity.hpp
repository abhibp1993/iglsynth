//
// Created by abhibp1993 on 2/21/20.
//

#ifndef IGLSYNTH_ENTITY_HPP
#define IGLSYNTH_ENTITY_HPP

#include <iostream>
#include <string>
#include <any>

class Entity {
protected:
    std::string id;
    std::string _class_name;

public:
    Entity() { _class_name = __func__; }

    virtual std::string serialize(){
        std::map<std::string, std::string> ser;
        ser["__class__"] = _class_name;
        ser["id"] = id;

        std::string ser_str;

        ser_str = "{";
        for ( const auto &it : ser ) {
            ser_str += it.first;
            ser_str += ": ";
            ser_str += it.second;
            ser_str += ", ";
        }
        ser_str.pop_back();
        ser_str += "}";

        return ser_str;
    }

    virtual std::string deserialize(std::any msg){
        // TODO: Raise IGLException_NotImplemented.
        return "";
    }

    std::string tostring(){
        return "<" + _class_name + " object with id=" + id + ">";
    }

    std::string get_id(){
        return id;
    }
};


#endif //IGLSYNTH_ENTITY_HPP
