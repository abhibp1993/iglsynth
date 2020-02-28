# CMake version
CMAKE_MINIMUM_REQUIRED(VERSION 3.13)
MESSAGE(STATUS "CMake version ${CMAKE_VERSION}")

# Project name and C++ compiler version
PROJECT(iglsynth LANGUAGES CXX)
SET (CMAKE_CXX_STANDARD 17)
SET (BOOST_ROOT "/usr/include")
SET (CMAKE_MODULE_PATH	"${CMAKE_MODULE_PATH}" "${CMAKE_CURRENT_SOURCE_DIR}/CMakeModules")


# Dependency: Python 3.x
FIND_PACKAGE(PythonLibs 3.6 REQUIRED)
INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_DIRS} )
MESSAGE(STATUS "Found Python ver. ${PYTHONLIBS_VERSION_STRING} at ${PYTHON_INCLUDE_DIRS}")


## Dependency: Boost
FIND_PACKAGE( Boost 1.65 COMPONENTS python3 unit_test_framework REQUIRED)
INCLUDE_DIRECTORIES( ${Boost_INCLUDE_DIRS} )
MESSAGE(STATUS "Found Boost.Python ver. ${Boost_VERSION} at ${Boost_INCLUDE_DIRS} with ${Boost_LIBRARIES}")


# Needs: sudo apt-get install pkg-config
# Dependency: Spot
FIND_PACKAGE(Spot)
IF (SPOT_FOUND)
    SET(OMPL_HAVE_SPOT 1)
    INCLUDE_DIRECTORIES("${SPOT_INCLUDE_DIRS}")
    LINK_DIRECTORIES(${SPOT_LIBRARY_DIRS})
    MESSAGE(STATUS "Found Spot ver. ${SPOT_VERSION} at ${SPOT_INCLUDE_DIRS} with ${SPOT_LIBRARIES}")
ELSE (not SPOT_FOUND)
    MESSAGE(STATUS "DID NOT FIND SPOT.")
ENDIF()


# Dependency [Optional]: Boost Test Framework
## Reference: https://eb2.co/blog/2015/06/driving-boost.test-with-cmake/
#FIND_PACKAGE(Boost 1.54 QUIET COMPONENTS unit_test_framework)


# Set Compiler flags
SET (CMAKE_CXX_FLAGS "-fPIC -pthread -I${PYTHON_INCLUDE_DIR}")


# Path for library files (Python include libraries)
SET(BOOST_BIND_OUTPUT_DIR   ${CMAKE_CURRENT_SOURCE_DIR}/iglsynth/util)


# Add files to library
ADD_LIBRARY (iglsynth SHARED
#        iglsynth_cpp/entity.hpp
#        iglsynth_cpp/graph.hpp
#        iglsynth_cpp/graph.cpp
#        iglsynth_cpp/entity_wrap.cpp
        iglsynth_cpp/util/entity.h
        iglsynth_cpp/util/types.h
#        iglsynth_cpp/util/graph.h
#        iglsynth_cpp/util/graph.cpp
        iglsynth_cpp/game/action.cpp
        iglsynth_cpp/game/action.h
        iglsynth_cpp/game_wrap.cpp
        )



TARGET_LINK_LIBRARIES( iglsynth LINK_PUBLIC ${Boost_LIBRARIES} ${SPOT_LIBRARIES} ${PYTHON_LIBRARIES})

SET_TARGET_PROPERTIES(iglsynth PROPERTIES
        PREFIX                        ""
        LIBRARY_OUTPUT_DIRECTORY      ${BOOST_BIND_OUTPUT_DIR})


## Add files to executables
#ADD_EXECUTABLE(tests
#        #        tests/cpp/test_graph.cpp
#        tests/cpp/boost_test_graph.cpp)
#TARGET_LINK_LIBRARIES( tests LINK_PUBLIC iglsynth )


# Ctest Testing Framework
#enable_testing()
#add_test( cpp_test tests )