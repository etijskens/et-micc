#!/bin/bash
#-------------------------------------------------------------------------------
# This shell script detects and reports the best fortran compiler available in 
# the environment, and uses it to build a python module from fortran code using
# the f2py it finds in the environment.
#-------------------------------------------------------------------------------

# set -x # uncomment for debugging this script

module={{ cookiecutter.module_name }}{{ cookiecutter.f2py_suffix }}
source=${module}.f90

# look for fortran compiler either ifort, or gfortran
rm -f stderr.txt
F90=$(which ifort 2>> stderr.txt)
if [ $? -eq 1 ]; then
    F90=$(which gfortran 2>> stderr.txt)
    if [ $? -eq 1 ]; then
        echo "ERROR: no fortran compiler found (looking for ifort, gfortran)".
        exit 1
    else
        # gfortran options
        f2py_opt_flags="-O3 -fopt-info-all"
        f2py_arch_flags="-march=native"
    fi
else
    # gfortran options
    f2py_opt_flags="-O3 -qopt-report"
    f2py_arch_flags="-xHost"
    # the latter assumes that we are compiling for the same CPU as where the
    # process is running. This is ok for the VSC clusters, where the login
    # nodes always have the same cpu as the compute nodes.
fi

echo
echo "Fortran compiler = ${F90}"
${F90} --version

# Avoid that users use the system compilers for compiling cluster software.
me=$(whoami)
if [[ "${F90}" = "/usr/bin/gfortran" ]]; then
	if [[ "${me}" = "vsc"* ]]; then 
	    echo "===================================================================="
	    echo "WARNING: It is strongly recommended NOT to use the system compilers"
	    echo "         for compiling HPC modules, as they are old and not fit for"
	    echo "         this purpose. Use a HPC toolchain instead."
	    echo "           > module load intel/..."
	    echo "           > module load GCC/..."
	    echo "===================================================================="
	    exit 1
	fi
fi

echo "Fortran compiler options:"
echo "  f2py_arch_flags = ${f2py_arch_flags}"
echo "  f2py_opt_flags = ${f2py_opt_flags}"
echo

# we always use gcc for compiling the wrapper
# (always available when intel compiler suite is activated)
GCC=$(which gcc 2>> stderr.txt)
if [ $? -eq 1 ]; then
    echo "ERROR: gcc not found."
    exit 1
fi
echo "C compiler = ${GCC}"
gcc --version

F2PY=$(which f2py 2>> stderr.txt)
if [ $? -eq 1 ]; then
    echo "ERROR: f2py not found."
    exit 1
fi
echo
echo "F2PY  = ${F2PY} $(f2py -v)"
echo "numpy = $(python -c 'import numpy; print(numpy.__version__)')"

# we always use gcc for compiling the wrapper
# (always available when intel compiler suite is activated)
GCC=$(which gcc)
if [ $? -eq 1 ]; then
	echo "ERROR: gcc not found."
	exit 1
fi
echo "C compiler = ${GCC}"
gcc --version

F2PY=$(which f2py)
if [ $? -eq 1 ]; then
	echo "ERROR: f2py not found."
	exit 1
fi
echo
echo "F2PY  = ${F2PY} $(f2py -v)"
echo "numpy = $(python -c 'import numpy; print(numpy.__version__)')"
echo
# Here's the real work:

# remove the module if it exists already:
rm -rf ${module}.cpython-*

f2py -c\
    --build-dir _f2py_build \
    --opt="${f2py_opt_flags}" \
    --arch="${f2py_arch_flags}" \
    -DF2PY_REPORT_ON_ARRAY_COPY=1 -DNPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION -Dlong_double="long double"\
    --f90exec=${F90} \
    ${source} -m ${module}

# indicate success/failure 
if [ $? -eq 0 ]; then
	echo
 	echo "Module built : $(ls ${module}*so)"
else
	echo
 	echo "ERROR: module not built."
fi
