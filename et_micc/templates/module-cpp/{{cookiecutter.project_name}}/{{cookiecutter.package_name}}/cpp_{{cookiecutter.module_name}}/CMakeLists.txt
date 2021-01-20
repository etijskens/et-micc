#-------------------------------------------------------------------------------
# Build C++ module {{ cookiecutter.package_name }}.{{ cookiecutter.module_name }}
#   > cd _cmake_build
# For a clean build:
#   > rm -rf *
# Configure:
#   > cmake ..
# build and install the .so file:
#   > make install
#-------------------------------------------------------------------------------
# This is all standard CMake

# There is a lot of boilerplate code, which normally needs not to be changed. It
# is always indented and surrounded by comment lines marking the begin and end of
# the boilerplate code, like this:
#<< begin boilerplate code
    # some code
#>> end boilerplate code

#<< begin boilerplate code
    cmake_minimum_required(VERSION 3.4)
  # Find pybind11_DIR, if python can be found...
  # (that is we assume that the virtual environment is activated)
    project({{ cookiecutter.module_name }} CXX)
    find_program(
        PYTHON_EXECUTABLE
        NAMES python
    )
    if(PYTHON_EXECUTABLE)
      execute_process(
          COMMAND "${PYTHON_EXECUTABLE}" -c "import site; print(site.getsitepackages()[0])"
          OUTPUT_VARIABLE _site_packages
          OUTPUT_STRIP_TRAILING_WHITESPACE
          ERROR_QUIET
      )
    else()
      message(FATAL_ERROR "python executable not found.")
    endif()
    set(pybind11_DIR "${_site_packages}/pybind11/share/cmake/pybind11")
    message("pybind11_DIR : ${pybind11_DIR}")
  # now this will do fine:
    find_package(pybind11 CONFIG REQUIRED)
#>> end boilerplate code

####################################################################################################
######################################################################### Customization section ####
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
####################################################################################################

#<< begin boilerplate code
  # Create the target:
    pybind11_add_module({{ cookiecutter.module_name }} {{ cookiecutter.module_name }}.cpp)

    install(
        FILES       "_cmake_build/{{ cookiecutter.module_name }}${PYTHON_MODULE_EXTENSION}"
        DESTINATION "${CMAKE_CURRENT_SOURCE_DIR}/.."
    )
#>> end boilerplate code
