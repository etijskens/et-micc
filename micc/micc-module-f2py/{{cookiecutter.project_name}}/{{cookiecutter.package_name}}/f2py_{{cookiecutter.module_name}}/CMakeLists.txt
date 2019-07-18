cmake_minimum_required(VERSION 2.8.12)
project({{ cookiecutter.module_name }} Fortran C CXX)

#list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/pybind11/tools")
find_package(pybind11 CONFIG REQUIRED)
message(STATUS "Found pybind11 v${pybind11_VERSION}: ${pybind11_INCLUDE_DIRS}")
include(FindPythonLibsNew)

list(APPEND CMAKE_MODULE_PATH "{{ cookiecutter.path_to_cmake_tools }}")
include(FindF2PY)
find_package(F2PY REQUIRED)

include(F2pyAddModule)
f2py_add_module({{ cookiecutter.module_name }})