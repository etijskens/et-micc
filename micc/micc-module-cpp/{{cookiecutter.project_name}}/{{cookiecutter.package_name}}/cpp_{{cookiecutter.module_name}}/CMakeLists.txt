#-------------------------------------------------------------------------------
# Build C++ module {{ cookiecutter.package_name }}.{{ cookiecutter.module_name }}
#   > cd _build
# For a clean build:
#   > rm -rf * 
# Configure:
#   > cmake ..
# build and install the .so file:
#   > make install
#-------------------------------------------------------------------------------
cmake_minimum_required(VERSION 2.8.12)
project({{ cookiecutter.module_name }} CXX)

find_package(pybind11 CONFIG REQUIRED)
pybind11_add_module({{ cookiecutter.module_name }} {{ cookiecutter.module_name }}.cpp)

install(FILES       "_build/{{ cookiecutter.module_name }}${PYTHON_MODULE_EXTENSION}"
        DESTINATION "${CMAKE_CURRENT_SOURCE_DIR}/.."
       )
