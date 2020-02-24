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
    std::string _id;
    std::string _class_name;

public:
    // TODO: Auto assign entity ID.
    // TODO: Can we concatenate __func__ to obtain "A.B.C"?
    Entity() { _class_name = __func__; }

    // Should serialize return a dictionary of string to IGLTypes?
    // Or should it return a string directly?
    // Reason: We could leave it to the "Transmission" module (GraphML/pickle/whatever)
    // to do whatever it wants to do.
    std::string serialize(){
        std::map<std::string, std::string> ser;
        ser["__class__"] = _class_name;
        ser["id"] = _id;

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

    // Deserialize should return an object of same class.
    // How to define generic return type then?
    Entity deserialize(std::map<std::string, std::string> msg){
        // TODO: Raise IGLException_NotImplemented.
        Entity e;
        e.id = msg["id"];
        e._class_name = msg["__class__"];
        return e;
    }

    std::string tostring(){
        return "<" + _class_name + " object with id=" + id + ">";
    }

    std::string get_id(){
        return id;
    }
};


#endif //IGLSYNTH_ENTITY_HPP
