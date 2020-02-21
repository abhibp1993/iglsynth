# CMakeLists.txt is modified from AI Toolbox

cmake_minimum_required (VERSION 3.9)

project (iglsynth   LANGUAGES CXX
                    HOMEPAGE_URL https://akulkarni.me/iglsynth
                    VERSION 1.0.0
        )

##############################
## Compiler/Linker Settings ##
##############################

# Set default cmake build type to release
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Release" CACHE STRING
            "Choose the type of build, options are:
          Debug Release RelWithDebInfo MinSizeRel."
            FORCE)
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if (NOT WIN32)
    add_definitions(
            -Wall
            -Wextra
    )
endif()

# Check for Link Time Optimizations with this compiler
include(CheckIPOSupported)
check_ipo_supported(RESULT LTO_SUPPORTED OUTPUT LTO_ERROR)

if( LTO_SUPPORTED )
    message(STATUS "IPO / LTO enabled")
else()
    message(STATUS "IPO / LTO not supported: <${LTO_ERROR}>")
endif()


##############################
##     Project Settings     ##
##############################

# Default is to build everything
if (NOT MAKE_ALL AND NOT MAKE_LIB)
    set(MAKE_ALL    1)
endif()

if (MAKE_ALL)
    set(MAKE_MODULE_GAME        1)
    set(MAKE_PYTHON             1)
    set(MAKE_TESTS              1)
    set(MAKE_EXAMPLES           1)

elseif (MAKE_LIB)
    set(MAKE_MODULE_GAME        1)

endif()

# Check whether to enable logging
#if (${AI_LOGGING_ENABLED})
#    add_definitions(-DAI_LOGGING_ENABLED)
#    set(LOGGING_STATUS "ENABLED")
#else()
#    set(LOGGING_STATUS "DISABLED")
#endif()

# For additional Find library scripts
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${PROJECT_SOURCE_DIR}/cmake/Modules/")

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR})

# Print what we're actually doing
set(MAP_MAKE_MODULE_GAME        "# Building Game Module")
set(MAP_MAKE_PYTHON             "# Building Python bindings")
set(MAP_MAKE_TESTS              "# Building Tests")
set(MAP_MAKE_EXAMPLES           "# Building Examples")

message("")
message("Build type: " ${CMAKE_BUILD_TYPE})
message("Logging is " ${LOGGING_STATUS})
foreach(v MAKE_MODULE_GAME;MAKE_PYTHON;MAKE_TESTS;MAKE_EXAMPLES)
    if (${${v}})
        message(${MAP_${v}})
    endif()
endforeach(v)
message("")


##############################
##       Dependencies       ##
##############################

set(BOOST_VERSION_REQUIRED 1.59)
set(EIGEN_VERSION_REQUIRED 3.2.92)

# Optional to force Boost to use static libraries. Can be useful on Windows.
#
# set(Boost_USE_STATIC_LIBS ON)
# add_definitions(-DBOOST_PYTHON_STATIC_LIB)

find_package(Boost ${BOOST_VERSION_REQUIRED} REQUIRED)
include_directories(SYSTEM ${Boost_INCLUDE_DIRS})

find_package(Eigen3 ${EIGEN_VERSION_REQUIRED} REQUIRED)
include_directories(SYSTEM ${EIGEN3_INCLUDE_DIR})


if (MAKE_PYTHON)
    # Try to find out which version of Python we should be targeting depending
    # on which interpreter is found. If the version has been selected
    # explicitly we search for it directly.
#    find_package(PythonInterp ${PYTHON_VERSION} REQUIRED)
    find_package (Python3 COMPONENTS Interpreter Development)
    set(PYTHON_VERSION ${Python3_VERSION_MAJOR})

    # WARNING: The COMPONENTS parts of Boost here may need to be changed
    # depending on your system. For example, you may need to rename `python3` to
    # `python37`, depending on how your libraries are made.
    # This setup works for Ubuntu, but feel free to change it in Windows.
    if (${PYTHON_VERSION} EQUAL 3)
        find_package(PythonLibs 3 REQUIRED)
        find_package(Boost ${BOOST_VERSION_REQUIRED} COMPONENTS python3 REQUIRED)
        set(BOOST_PYTHON_LIBRARY_NAME "Boost_PYTHON3_LIBRARY")
    else()
        message(WARNING "Python 3.x not found. Finding Python 2.x" ...)
        find_package(PythonLibs 2.7 EXACT REQUIRED)
        find_package(Boost ${BOOST_VERSION_REQUIRED} COMPONENTS python REQUIRED)
        set(BOOST_PYTHON_LIBRARY_NAME "Boost_PYTHON_LIBRARY")
    endif()

    include_directories(SYSTEM ${PYTHON_INCLUDE_DIRS})
endif()

if (MAKE_TESTS)
    find_package(Boost ${BOOST_VERSION_REQUIRED} COMPONENTS unit_test_framework REQUIRED)
endif()


##############################
##      Project Start       ##
##############################

# Add library directories
#include_directories(${PROJECT_SOURCE_DIR}/include)
#add_subdirectory(${PROJECT_SOURCE_DIR}/src)

# If enabled, add tests
#if (MAKE_TESTS)
#    include(CTest)
#    add_subdirectory(${PROJECT_SOURCE_DIR}/test)
#endif()
#
## If enabled, add Python bindings
#if (MAKE_EXAMPLES)
#    add_subdirectory(${PROJECT_SOURCE_DIR}/examples)
#endif()