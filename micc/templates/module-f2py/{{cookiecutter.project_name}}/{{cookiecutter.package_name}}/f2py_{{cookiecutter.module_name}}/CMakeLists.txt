#-------------------------------------------------------------------------------
# Build f2py module {{ cookiecutter.package_name }}.{{ cookiecutter.module_name }}
#   > cd _build
# For a clean build:
#   > rm -rf * 
# Configure:
#   > cmake ..
# build and install the .so file:
#   > make install
#-------------------------------------------------------------------------------
cmake_minimum_required(VERSION 2.8.12)
project({{ cookiecutter.module_name }} Fortran C CXX)

find_package(pybind11 CONFIG REQUIRED)
message(STATUS "Found pybind11 v${pybind11_VERSION}: ${pybind11_INCLUDE_DIRS}")
include(FindPythonLibsNew)

# expose micc/cmake_tools
if(EXISTS "${PYTHON_SITE_PACKAGES}/micc/cmake_tools")
	list(APPEND CMAKE_MODULE_PATH "${PYTHON_SITE_PACKAGES}/micc/cmake_tools")
else()
	if(EXISTS "{{ cookiecutter.path_to_cmake_tools }}")
		list(APPEND CMAKE_MODULE_PATH "{{ cookiecutter.path_to_cmake_tools }}")
	    message(WARNING 
	    	"Directory ${PYTHON_SITE_PACKAGES}/micc/cmake_tools not found.\n"
	        "Using {{ cookiecutter.path_to_cmake_tools }} instead."
	    )
	else()
	    message(FATAL_ERROR
	    	"No micc/cmake_tools directory found. Looked for:\n"
	        "  * ${PYTHON_SITE_PACKAGES}/micc/cmake_tool.\n"
	    	"  * {{ cookiecutter.path_to_cmake_tools }}."
		)
	endif()
endif()

include(FindF2PY)
find_package(F2PY REQUIRED)

include(F2pyAddModule)
f2py_add_module({{ cookiecutter.module_name }})