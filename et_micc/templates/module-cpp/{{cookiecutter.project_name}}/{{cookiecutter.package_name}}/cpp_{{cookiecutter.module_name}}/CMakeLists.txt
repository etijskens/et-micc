#-------------------------------------------------------------------------------
# Build C++ module {{ cookiecutter.package_name }}.{{ cookiecutter.module_name }}
#   > cd _cmake_build
# For a clean build:
#   > rm -rf * 
# Configure:
#   > cmake -Dpybind11_DIR={{ cookiecutter.project_name }}/.venv/lib/python{{ cookiecutter.python_version }}/lib/site-packages/pybind11 ..
# build and install the .so file:
#   > make install
#-------------------------------------------------------------------------------
cmake_minimum_required(VERSION 2.8.12)

find_package(pybind11 CONFIG REQUIRED)

project({{ cookiecutter.module_name }} CXX)

# set compiler:
# set(CMAKE_CXX_COMPILER path/to/executable)

# Set build type:
# set(CMAKE_BUILD_TYPE DEBUG | MINSIZEREL | RELEASE | RELWITHDEBINFO)

# Add compiler options:
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} <additional C++ compiler options>")

# Add preprocessor macro definitions:
# add_compile_definitions(
#     OPENFOAM=1912                     # set value
#     WM_LABEL_SIZE=$ENV{WM_LABEL_SIZE} # set value from environment variable
#     WM_DP                             # just define the macro
# )

# Add include directories
#include_directories(
#     path/to/dir1
#     path/to/dir2
# )

# Add link directories
# link_directories(
#     path/to/dir1
# )

# Add link libraries (lib1 -> liblib1.so)
# link_libraries(
#     lib1
#     lib2
# )

pybind11_add_module({{ cookiecutter.module_name }} {{ cookiecutter.module_name }}.cpp)

install(FILES       "_build/{{ cookiecutter.module_name }}${PYTHON_MODULE_EXTENSION}"
        DESTINATION "${CMAKE_CURRENT_SOURCE_DIR}/.."
       )
