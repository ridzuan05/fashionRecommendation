cmake_minimum_required(VERSION 2.8) 
project(demo) 
set(CMAKE_BUILD_TYPE release)

# add packages here
find_package(OpenCV REQUIRED)

# add includes
include_directories(${OpenCV_INCLUDE_DIRS})

set(SOURCEFILES
src/demo.cpp
)

add_executable(demo ${SOURCEFILES})

target_link_libraries( demo ${OpenCV_LIBS})
