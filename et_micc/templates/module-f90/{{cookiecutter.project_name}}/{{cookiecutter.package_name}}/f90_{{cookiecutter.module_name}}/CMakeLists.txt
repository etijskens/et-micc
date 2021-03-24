#-------------------------------------------------------------------------------
# Build f90 binary extension module {{ cookiecutter.package_name }}.{{ cookiecutter.module_name }}
#   > cd _cmake_build
# For a clean build:
#   > rm -rf *
# Configure:
#   > cmake ..
# build and install the .so file:
#   > make install
#-------------------------------------------------------------------------------
# It sets the following CMake variables and transfers them to the f2py executable.
#  - F2PY_opt      ->  f2py --opt=<${F2PY_opt}>
#  - F2PY_arch     ->  f2py --arch=<${F2PY_arch}>
#  - F2PY_f90flags ->  f2py --f90flags=<${F2PY_arch}>
#  - F2PY_debug    ->  f2py --debug
# Suitable values for these are estimated from CMAKE_BUILD_TYPE (RELEASE by default).
#
# In addition the following CMake variables are defined:
#  - F2PY_defines  : a list of defines passed to the Fortran compiler
#  - F2PY_includes : a list of included directories passed to the Fortran compiler
#  - F2PY_linkdirs : a list of directories to be searched for linked libraries
#  - F2PY_linklibs : a list of libraries to be linked into the binary extension module
# You can of course modify their values to suit your needs.

# There is a lot of boilerplate code, which normally needs not to be changed. It
# is always indented and surrounded by comment lines marking the begin and end of
# the boilerplate code, like this:
#<< begin boilerplate code
    # some code
#>> end boilerplate code

#<< begin boilerplate code
    cmake_minimum_required(VERSION 3.4)

    project({{ cookiecutter.module_name }} Fortran)
    if(NOT CMAKE_BUILD_TYPE)
        # RELEASE is the default build type:
        set(CMAKE_BUILD_TYPE RELEASE)
    endif()

    # Set the module name:
    set(F2PY_module_name "{{ cookiecutter.module_name }}")

#>> end boilerplate code

# Some useful defines to be passed to the build process:
list(APPEND F2PY_defines "-DNPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION")
list(APPEND F2PY_defines "-DF2PY_REPORT_ON_ARRAY_COPY=1")

# Set the build type:
#  - If you do not specify a build type, it is RELEASE by default.
#  - Note that the DEBUG build type will trigger f2py's '--noopt --noarch --debug' options.
# set(CMAKE_BUILD_TYPE DEBUG | MINSIZEREL | RELEASE | RELWITHDEBINFO)

#<< begin boilerplate code
    # Infer variables from CMAKE_BUILD_TYPE
    # Uncomment these lines to see the default flags for each build type:
    # message("CMAKE_Fortran_FLAGS_RELEASE        : ${CMAKE_Fortran_FLAGS_RELEASE}")
    # message("CMAKE_Fortran_FLAGS_RELWITHDEBINFO : ${CMAKE_Fortran_FLAGS_RELWITHDEBINFO}")
    # message("CMAKE_Fortran_FLAGS_MINSIZEREL     : ${CMAKE_Fortran_FLAGS_MINSIZEREL}")
    # message("CMAKE_Fortran_FLAGS_DEBUG          : ${CMAKE_Fortran_FLAGS_DEBUG}")
    if(CMAKE_BUILD_TYPE STREQUAL "RELEASE")
        # CMAKE_Fortran_FLAGS_RELEASE = -O3 -DNDEBUG -O3
        set(F2PY_opt "-O3")
        list(APPEND F2PY_defines "-DNDEBUG")
    elseif( CMAKE_BUILD_TYPE STREQUAL "RELWITHDEBINFO")
        # CMAKE_Fortran_FLAGS_RELWITHDEBINFO = -O2 -g -DNDEBUG
        set(F2PY_opt "-O2")
        list(APPEND F2PY_defines "-DNDEBUG")
        set(F2PY_debug "--debug")
    elseif( CMAKE_BUILD_TYPE STREQUAL "MINSIZEREL")
        # CMAKE_Fortran_FLAGS_MINSIZEREL = -Os -DNDEBUG -Os
        set(F2PY_opt "-Os")
        list(APPEND F2PY_defines "-DNDEBUG")
    elseif( CMAKE_BUILD_TYPE STREQUAL "DEBUG")
        # CMAKE_Fortran_FLAGS_DEBUG = -g
        set(F2PY_opt "-O0")
        list(APPEND F2PY_defines "-DDEBUG")
        set(F2PY_debug "--debug")
    endif()
#>> end boilerplate code

####################################################################################################
######################################################################### Customization section ####
# Specify compiler options #########################################################################
# Uncomment to turn off optimization:
# set(F2PY_noopt 1)

# Uncomment to turn off architecture specific optimization:
# set(F2PY_noarch 1)

# Set additional f90 compiler flags:
# set(F2PY_f90flags your_flags_here)
# set(F2PY_f90flags -cpp)   # enable the C preprocessor (preprocessor directives must appear on the
                            # on the first column of the line).

# Set architecture specific optimization compiler flags:
# set(F2PY_arch your_flags_here)

# Overwrite optimization flags
# set(F2PY_opt your_flags_here)

# Add preprocessor macro definitions ###############################################################
# add_compile_definitions(
#     OPENFOAM=1912                     # set value
#     WM_LABEL_SIZE=$ENV{WM_LABEL_SIZE} # set value from environment variable
#     WM_DP                             # just define the macro
# )

# Add include directories ##########################################################################
# include_directories(
#     path/to/dir1
#     path/to/dir2
# )

# Add link directories #############################################################################
# link_directories(
#     path/to/dir1
# )

# Add link libraries (lib1 -> liblib1.so) ##########################################################
# link_libraries(
#     lib1
#     lib2
# )
####################################################################################################

# only boilerplate code below

#<< begin boilerplate code
    if(F2PY_noopt)
        set(F2PY_opt "--noopt")
    else()
        if(F2PY_opt)
            set(F2PY_opt "--opt='${F2PY_opt}'")
        endif()
    endif()

    if(F2PY_noarch)
        set(F2PY_arch "--noarch")
    else()
        if(F2PY_arch)
            set(F2PY_arch "--arch='${F2PY_arch}'")
        endif()
    endif()

    if(F2PY_f90flags)
        set(F2PY_f90flags "--f90flags='${F2PY_f90flags}'")
    endif()

    # If the user used ADD_COMPILE_DEFINITIONS transfer the definitions to F2PY_defines
    get_directory_property( defines DIRECTORY ${CMAKE_SOURCE_DIR} COMPILE_DEFINITIONS )
    # message("defines:${defines}")
    foreach(def IN LISTS defines)
        list(APPEND F2PY_defines "-D${def}")
    endforeach()

    # If the user used include_directories, transfer the include directories to F2PY_includes
    get_directory_property( includes DIRECTORY ${CMAKE_SOURCE_DIR} INCLUDE_DIRECTORIES )
    # message("includes:${includes}")
    foreach(inc IN LISTS includes)
        list(APPEND F2PY_includes "-I${inc}")
    endforeach()

    # If the user used link_directories, transfer the link directories to F2PY_linkdirs
    get_directory_property( linkdirs DIRECTORY ${CMAKE_SOURCE_DIR} LINK_DIRECTORIES )
    # message("linkdirs:${linkdirs}")
    foreach(dir IN LISTS linkdirs)
        list(APPEND F2PY_linkdirs "-L${dir}")
    endforeach()

    # If the user used link_libraries, transfer the link libraries to F2PY_linklibs
    get_directory_property( linklibs DIRECTORY ${CMAKE_SOURCE_DIR} LINK_LIBRARIES )
    # message("linklibs:${linklibs}")
    foreach(lib IN LISTS linklibs)
        list(APPEND F2PY_linklibs "-l${lib}")
    endforeach()

    # list all settings
    message("")
    message("# Build settings ###################################################################################")
    message("CMAKE_Fortran_COMPILER: ${CMAKE_Fortran_COMPILER}")
    message("CMAKE_BUILD_TYPE      : ${CMAKE_BUILD_TYPE}")
    message("F2PY_opt              : ${F2PY_opt}")
    message("F2PY_arch             : ${F2PY_arch}")
    message("F2PY_f90flags         : ${F2PY_f90flags}")
    message("F2PY_debug            : ${F2PY_debug}")
    message("F2PY_defines          : ${F2PY_defines}")
    message("F2PY_includes         : ${F2PY_includes}")
    message("F2PY_linkdirs         : ${F2PY_linkdirs}")
    message("F2PY_linklibs         : ${F2PY_linklibs}")

    # Find necessary components ####################################################################
    # Find the python executable:
    find_program(
        PYTHON_EXECUTABLE
        NAMES python
    )
    if(PYTHON_EXECUTABLE)
      execute_process(
          COMMAND "${PYTHON_EXECUTABLE}" --version
          OUTPUT_VARIABLE _python_version
          OUTPUT_STRIP_TRAILING_WHITESPACE
          ERROR_QUIET
      )
    else()
      message(FATAL_ERROR "python executable not found.")
    endif()
    # Obtain the binary extension suffix for this Python version:
    execute_process(
        COMMAND ${PYTHON_EXECUTABLE} -c "import sysconfig; print(sysconfig.get_config_var('EXT_SUFFIX'))"
        OUTPUT_VARIABLE BINARY_EXTENSION_SUFFIX
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )

    # Find the f2py executable:
    find_program(
        F2PY_EXECUTABLE
        NAMES f2py${PYTHON_VERSION_MAJOR} f2py
    )
    if(F2PY_EXECUTABLE)
      execute_process(
          COMMAND "${F2PY_EXECUTABLE}" -v
          OUTPUT_VARIABLE _f2py_version
          OUTPUT_STRIP_TRAILING_WHITESPACE
          ERROR_QUIET
      )
    else()
      message(FATAL_ERROR "f2py executable not found.")
    endif()

    # Set the fortran source file
    set(F2PY_fortran_source "${CMAKE_CURRENT_SOURCE_DIR}/${F2PY_module_name}.f90")
    # Set the module filepath
    set(F2PY_module_filepath ${CMAKE_CURRENT_BINARY_DIR}/${F2PY_module_name}${BINARY_EXTENSION_SUFFIX})

    message("module name           : ${F2PY_module_name}${BINARY_EXTENSION_SUFFIX}")
    message("module filepath       : ${F2PY_module_filepath}")
    message("source                : ${F2PY_fortran_source}")
    message("python executable     : ${PYTHON_EXECUTABLE} [version=${_python_version}]")
    message("  f2py executable     : ${F2PY_EXECUTABLE} [version=${_f2py_version}]")
    message("####################################################################################################")

    ### Create a CMake target for the binary extension module ##########################################
    add_custom_target(
      ${F2PY_module_name} ALL
      DEPENDS ${F2PY_module_filepath}
    )

    # Create a command for building the binary extension module
    # (This uses the fortran compiler found by CMake.)
    add_custom_command(
      OUTPUT ${F2PY_module_filepath}
      COMMAND ${F2PY_EXECUTABLE}
        -m ${F2PY_module_name}
        -c
        --f90exec=${CMAKE_Fortran_COMPILER}
        ${F2PY_fortran_source}
        ${F2PY_defines}
        ${F2PY_includes}
        ${F2PY_linkdirs}
        ${F2PY_linklibs}
        ${F2PY_debug}
        ${F2PY_opt}
        ${F2PY_arch}
        ${F2PY_f90flags}
        --build-dir ${CMAKE_CURRENT_SOURCE_DIR}/_cmake_build
      WORKING_DIRECTORY
    )

    # Install the binary extension module
    install(
      FILES ${F2PY_module_filepath}
      DESTINATION "${CMAKE_CURRENT_SOURCE_DIR}/.."
    )
#>> end boilerplate code
