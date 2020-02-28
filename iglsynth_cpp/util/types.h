//
// Created by abhibp1993 on 2/23/20.
//

#ifndef IGLSYNTH_TYPES_H
#define IGLSYNTH_TYPES_H


#include <map>
#include <string>
#include <boost/variant.hpp>


namespace IGLSynth {

    // Define the types used in IGLSynth
    typedef boost::variant<bool, int, double, std::string> IGLTypes;
    typedef std::map<std::string, IGLTypes> IGLMap;

}


#endif //IGLSYNTH_TYPES_H
