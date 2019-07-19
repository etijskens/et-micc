
*******
History
*******

This section summarizes all my steps on the way to a working micc,
including dead-ends.

v0.5.5 (2019-07-10)
===================

* add cookiecutter template for C++ modules. 

We need:

* a C++ compiler (icpc or g++). On my mac i'd like to use GCC installed
  with ``brew install gcc``, or the g++ that comes with xcode. On the cluster
  I prefer Intel's ``icpc``.
* a Boost.Python library for the python in the environment. On the cluster
  there are  modules with Boost.Python such as the Intel Python distribution. 
  Building Boost with python isn't particulary easy, so, let's see what Anaconda
  cloud provides.
  
  * `boost-cpp v1.70 <https://anaconda.org/conda-forge/boost-cpp>`_,
    which has 1.76M downloads, so it is certainly worth trying. 
    bad luck: does not provide Boost.Python. A pity, I always like to have the
    latest Boost version.
    
  * `libboost <https://anaconda.org/anaconda/libboost>`_: boost v1.67, 
    not the most recent but certainly ok, unfortunately also no Boost.Python.
    
  * `py-boost <https://anaconda.org/anaconda/py-boost>: boost v1.67 and
    ``libboost_python.dylib`` and ``libboost_python37.dylib``. We used this before. 
     
* The include files ``numpy_boost.hpp`` and ``numpy_boost_python.hpp`` are copied to
  the ``<package_name>/numpy_boost`` directory. At some time they can be moved
  to a fixed place in the micc distribution. The user will probably never touch 
  these files anyway.
     
For compiling the module we have several options: 

* a build script, as for the f2pymodules, 
* a separate makefile, or
* suitable targets in the project makefile.
 
For building we use the make system from et/make. For the time being, we
copy all makefiles into the ``<package_name>/make`` directory. In the end 
they could be 
distributed with micc, together with `numpy_boost.hpp`` and 
``numpy_boost_python.hpp``. Note that the locations of the ``make`` and
``numpy_boost`` directories are hardcoded as ``./make`` and ``./numpy_boost``
so that ``make`` must be run in the package directory, for the time being.
That went fine, however, the issue with py-boost MACOS is still there. See
``et/numpy_boost/test_numpy_boost/macosx_anaconda_py-boost.md``.
The problem could be fixed by reverting to python 3.6 using the conda 
environment created as::

   > conda create -n py-boost python=3.7 py-boost
   > conda install py-boost python python-3.6.4 -c conda-forge

as suggested here (`<https://github.com/pybind/pybind11/issues/1579>`_).
Make sure to rerun the last line after installing a package
This fix doesn't seem to work anymore (2019.07.12). Python-3.6.4 is no longer
available... Hence we look further:

* `<https://anaconda.org/anaconda/boost>`_ has libboost-python, but not also
  segfaults. 
  
[At this point i checked that the test code works on Leibniz using the Intel
Python distribution: it does! So the problem is the same as before, but the 
solution does no longer work.]

I gave up... Started compiling Boost.Python myself. Download the boost version
you like, and uncompress ::

   > cd ~/software/boost_1_70_0
   > ./bootstrap.sh --with-python=`which python` --with-libraries="python"
   > ./b2 toolset=darwin stage

Got errors like::

   ...failed darwin.compile.c++ bin.v2/libs/python/build/darwin-4.2.1/release/python-3.6/threading-multi/visibility-hidden/tuple.o...
   darwin.compile.c++ bin.v2/libs/python/build/darwin-4.2.1/release/python-3.6/threading-multi/visibility-hidden/str.o
   In file included from libs/python/src/str.cpp:4:
   In file included from ./boost/python/str.hpp:8:
   In file included from ./boost/python/detail/prefix.hpp:13:
   ./boost/python/detail/wrap_python.hpp:57:11: fatal error: 'pyconfig.h' file not found
   # include <pyconfig.h>
             ^~~~~~~~~~~~
   1 error generated.
   
       "g++"   -fvisibility-inlines-hidden -fPIC -m64 -O3 -Wall -fvisibility=hidden -dynamic -gdwarf-2 -fexceptions -Wno-inline  
       -DBOOST_ALL_NO_LIB=1 -DBOOST_PYTHON_SOURCE -DNDEBUG  -I"." -I"/Users/etijskens/miniconda3/envs/pp2017/include/python3.6m" 
       -c -o "bin.v2/libs/python/build/darwin-4.2.1/release/python-3.6/threading-multi/visibility-hidden/str.o" 
       "libs/python/src/str.cpp"
       
The -I option specifies the wrong Python location! had to remove the Python 
configuration in ``~/user-config.jam``.

Still got "pyconfig.h not found errors"::

   ...failed darwin.compile.c++ bin.v2/libs/python/build/darwin-4.2.1/release/python-3.7/threading-multi/visibility-hidden/list.o...
   darwin.compile.c++ bin.v2/libs/python/build/darwin-4.2.1/release/python-3.7/threading-multi/visibility-hidden/long.o
   In file included from libs/python/src/long.cpp:5:
   In file included from ./boost/python/long.hpp:8:
   In file included from ./boost/python/detail/prefix.hpp:13:
   ./boost/python/detail/wrap_python.hpp:57:11: fatal error: 'pyconfig.h' file not found
   # include <pyconfig.h>
             ^~~~~~~~~~~~
   1 error generated.
   
       "g++"   -fvisibility-inlines-hidden -fPIC -m64 -O3 -Wall -fvisibility=hidden -dynamic -gdwarf-2 
       -fexceptions -Wno-inline  -DBOOST_ALL_NO_LIB=1 -DBOOST_PYTHON_SOURCE -DNDEBUG  -I"." 
      -I"/Users/etijskens/miniconda3/envs/ws2/include/python3.7" -c -o 
      "bin.v2/libs/python/build/darwin-4.2.1/release/python-3.7/threading-multi/visibility-hidden/long.o" 
      "libs/python/src/long.cpp"       

The -I option specifies ``/Users/etijskens/miniconda3/envs/ws2/include/python3.7`` 
whereas on my mac it is called ``/Users/etijskens/miniconda3/envs/ws2/include/python3.7m``.
a soft link ``python3.7`` which links to ``python3.7m`` solves the problem. 
Alternatively, edit the ``project-config.jam`` file and replace the ``using python :`` line
with (on a single line, I guess)::
   
       using python : 3.7 : /Users/etijskens/miniconda3/envs/ws2/bin/python \
                    : /Users/etijskens/miniconda3/envs/ws2/include/python3.7m \
                    : /Users/etijskens/miniconda3/envs/ws2/lib ;
   
Now Boost.Python builds fine. The libraries are in ``stage/lib``::

   > ll stage/lib
   total 13952
   -rw-r--r--  1 etijskens  staff   935152 Jul 12 12:23 libboost_numpy37.a
   -rwxr-xr-x  1 etijskens  staff    73852 Jul 12 12:23 libboost_numpy37.dylib*
   -rw-r--r--  1 etijskens  staff  5750432 Jul 12 12:23 libboost_python37.a
   -rwxr-xr-x  1 etijskens  staff   374980 Jul 12 12:23 libboost_python37.dylib*

In ``/Users/etijskens/miniconda3/envs/ws2/lib`` create soft links to both 
libraries::

   > cd /Users/etijskens/miniconda3/envs/ws2/lib
   > ln -s path/to/boost_1_70_0/stage/lib/libboost_python37.dylib
   > ln -s path/to/boost_1_70_0/stage/lib/libboost_numpy37.dylib

In ``/Users/etijskens/miniconda3/envs/ws2/include``, if there is no ``boost`` 
subdirectory, create soft links to 
libraries::

   > cd /Users/etijskens/miniconda3/envs/ws2/include
   > ln -s path/to/boost_1_70_0/boost

If there is already a ``boost`` subdirectory::

   > cd /Users/etijskens/miniconda3/envs/ws2/include/boost
   > ln -s path/to/boost_1_70_0/boost/python.hpp
   > ln -s path/to/boost_1_70_0/boost/python
   
... on Linux this works fine. On my Mac however I keep running into problems.

While googling for a solution, I came across `pybind11 <https://github.com/pybind/pybind11>`_.
These sections in the readme makes me particularly curious:

* pybind11 is a lightweight header-only library that exposes C++ types in 
  Python and vice versa, mainly to create Python bindings of existing C++ code. 
  
* Think of this library as a tiny self-contained version of Boost.Python with 
  everything stripped away that isn't relevant for binding generation. Without 
  comments, the core header files only require ~4K lines of code and depend on 
  Python (2.7 or 3.x, or PyPy2.7 >= 5.7) and the C++ standard library. This 
  compact implementation was possible thanks to some of the new C++11 language 
  features (specifically: tuples, lambda functions and variadic templates). Since 
  its creation, this library has grown beyond Boost.Python in many ways, leading 
  to dramatically simpler binding code in many common situations. 
  
Works as a charm. Comes with a cross-platform CMake build system that works out
of the box. Must put a soft link to the pybind11 repository in the project 
directory for the ``add_subdirectory(pybind11)`` statement to work. (in section 
"6.3.3 find_package vs. add_subdirectory" of the pybind11 manual, it is stated 
that this can be overcome with ``find_package(pybind11 REQUIRED)`` (this finds 
the pybind11 installed in the the current python environment out of the box - 
which is a good reason to ``conda|pip install pybind11``, rather than check it
out from github). 
That releaves me from maintaining the ``make`` stuff i wrote. (With a little bit
of CMake code for the f2py modules everything becomes much better streamlined and
the ``et/make`` system is no longer needed.

Had some trouble making it work on Leibniz. CMake's ``FindPythonInterp`` relies on 
``python-config`` to pick up the location current python executable. Unfortunately,
the Python environment I was using only defines ``python3-config``, and not 
``python-config``. That soft link still had to be added. 

Must now figure out how to deal with numpy arrays... There is some interesting
information in section "11.6 Eigen" of the pybind11 manual, allowing numpy arrays
to be passed by reference and work with `Eigen <http://eigen.tuxfamily.org>`_ 
matrices on the C++ side. Using Eigen instead of Boost.MultiArray has the 
additional advantage that there is some dense and sparse linear algebra routines
are also available. 

Set ``Boost_INCLUDE_DIR`` and ``Eigen3_INCLUDE_DIR`` in ``pybind11/CMakeLists.txt``.
Now Eigen tests are run as well and no failures observed.

The fact that cmake does so well, make me wonder if i shouldn't use cmake for the 
f2py modules as well instead of a shell script that will fail on windows. 
`Scikit-build <https://github.com/scikit-build>`_ contains a 
`FindF2py.cmake <https://github.com/scikit-build/scikit-build/blob/master/skbuild/resources/cmake/FindF2PY.cmake>`_
The tool, however, lets f2py find out the Fortran and C compiler it should use, 
and does not add any optimisation flags. 

There is a slight catch in using CMake: the filename ``CMakeLists.txt`` is fixed.
As "fixed"" as in "impossible to change" 
(see `this <http://cmake.3232098.n2.nabble.com/Changing-name-of-CMakeLists-txt-file-td4408932.html>`_).
That requires us to have a separate directory for each cpp module we want to add.
We did not have that restriction with f2py modules. For reasons of consistency,
we might change that. Module directory names should then, probably, be set as
``f2py_module`` and ``cpp_module`` rather than the other way around, so modules 
of the same type appear consecutivel in a directory listing. Sofar, Python modules
added through ``micc module my_module`` appear as my_module.py in the package directory.

CMake version is working. F2py autoselects the compilers (Fortran and C)
We further accomplished

* get rid of the soft link to pybind11 by referring to its installation 
  directory in CMakeLists.txt. Fixed! Finds the pybind11 installed in the current
  Python environment out of the box! (see pybind11 documentation 
  ``Build systems/Building with CMake/find_package vs add_subdirectory)``).
  done.
* get rid of the directory cmake_f2py_tools by referring to its location inside
  micc in CMakeLists.txt (we do not want endless copies of these, nor soft links)
  How can i install the micc CMake files so i can find them in the same way
  ``find_package(micc CONFIG REQUIRED)``. Playing the trick of pybind11 to install 
  files into ``/path/to/my_conda_environment/share/pybind11``
  seems to be non-trivial (`<https://github.com/pybind/pybind11/issues/1628>`_. Let's see
  if we can work around this. We can indeed easily work around. The ``micc.utils`` 
  module now has a function ``path_to_cmake_tools()`` that returns the path to the 
  cmake_tools directory (using ``__file__``). This path is added to the template 
  parameters (before they are exported to cookiecutter.json). Then Cookiecutter 
  knows the path and can insert it in the ``CMakeLists.txt``. Simple, and no loose 
  ends.
  done.
  
The approach to expose the ``micc/cmake_tools`` directory to the ``CMakeLists.txt``
of an fpy module through ``utils.path_to_cmake_tools()`` is a bit static as it 
hardcodes the path of the micc version that was use to create the module. If it 
changes, because that micc version is moved, or because development continues in 
another python environment, the build will fail. Instead we rely on the CMake 
variable ``${PYTHON_SITE_PACKAGES}`` and append ``/micc/cmake_tools`` to it.
  
Now add the cookiecutter templates for C++ modules


v0.5.4 (2019-07-10)
===================

* add cookiecutter template for fortran modules with f2py. We need:
   * f2py, comes with Numpy
   * a fortran compiler
   * a C compiler
   * what can be provided out of the box by conda?
   * support for this on on the clusters

I followed this advice: 
`f2py-running-fortran-code-in-python <https://www.scivision.dev/f2py-running-fortran-code-in-python-on-windows/>`_
and installed gcc from homebrew ``brew install gcc``. Inside the Conda 
environment I created soft links to gcc, g++ and gfortran.

There is an issue with Fortran arguments of type real*16, which become 
``long_double`` instead of ``long double`` in the ``<modulename>module.c`` 
wrapper file. The issue is circumvented by editing that file and running 
f2py_local.sh a second time. The issue occurred in gcc 7.4.0, 8.3.0 and 
9.1.0. Switching to gcc provided by XCode does not help either. However, 
adding ``-Dlong_double="long double"`` to the f2py command line options 
solves the problem nicely. :)

I, typically, had different bash scripts for running f2py, one for building 
locally and one for each cluster. It would be nice if a single script would
do and pickup the right compiler from the environment where it is run, as 
well as set the correct compiler options. There may be different f2py modules,
so there will be a different script for every f2py module: ``f2py_<module_name>.sh``.
Preferentially ``<module_name>`` ends with ``f90``. The module name appears 
also inside the script. The script looks for a ifort, and if absent for 
gfortran in the environment. It uses gcc for compiling the C-wrappers and 
for f2py. If one of the components is missing, the script exits with a non-
zero error code and an error message. The makefile can call::

   for s in f2py_*.sh; do ./${s}; done

Do we want a fortran module or not? the fortran module complicates stuff, as
it appears as a namespace inside the python module::

   # a) with a fortran module:
   # import the python module (built from compute_f90_a.f90) which lives
   # in the proj_f2py package: 
   import proj_f2py.compute_f90_a as python_module_a
   # create an alias for the fortran module inside that python module, which
   # is called 'f90_module'. The fortran module  behaves as any other member
   # in the python module.
   f90 = python_module.f90_module
   
   # b) without a fortran module:
   # import the python module (built from compute_f90_b.f90) 
   # this doesn not have a fortran module inside. 
   import proj_f2py.compute_f90_b as python_module_b

Documenting fortran modules with sphinx is problematic. There exists a sphinx
extension `sphinx-fortran <https://sphinx-fortran.readthedocs.io/en/latest/index.html>`_,
but this works presumably only with `sphinx <http://www.sphinx-doc.org/en/master/>`_ 
versions older than 1.8, and it is not avtively maintained/developed, which is a 
pity imho. As an alternative we include a file ``<project_name>/<package_name>/<module_f2py>.rst``
which has a suitable template for adding the documentation. As we actually want to
document a python module (built from Fortran code with f2py), we expect the user to 
enter documentation for the wrapper functions, not for the pure Fortran functions. 
That goes in the ``<project_name>/<package_name>/<module_f2py>.f90`` file but is 
not exposed in the project documentation. 

v0.5.3 (2019-07-09)
===================

* check for overwriting files (we must specify ``overwrite_if_exists`` for 
  cookiecutter because it will already report an error if just the directories
  exist. Adding files to existing directories is not supported out of the box.)
  The more components one can add, the higher the chance that there is going to 
  be a name clash and files are going to be overwritten. We do not want this to
  happen.
  We propose that ``micc`` should fail when files are overwritten, and that the 
  command be run again with a ``--force`` option.
  
  * Maybe, we can monkey patch this problem in cookiecutter. No success.
  * Create a tree of directories and files to be created and check against the 
    pre-existing tree. Seems complicated.
  * Create the tree to be added in a temporary dir which does not yet exist, and
    than check for collisions. That seems feasible.
      
v0.5.2 (2019-07-09)
===================

* add option ``--f2py`` to ``micc module ...``

v0.5.1 (2019-07-09)
===================

* ``micc create ...`` must write a .gitignore file and other configuration
  files. Addition of modules, apps do not change these.
* Cookiecutter template micc-module-f2py added, no code to use it yet

v0.5.0 (2019-07-04)
===================

* Fixed poetry issue #1182

v0.4.0 (2019-06-11)
===================

* First functional working version with
   
  * ``micc create`` 
  * ``micc app``
  * ``micc module``
  * ``micc version``
  * ``micc tag``
  

v0.2.5 (2019-06-11)
===================

* git support

  * ``git init` in ``micc create``
  * ``micc tag``

v0.2.4 (2019-06-11)
===================

* Makefile improvements:
  
  * documentation
  * tests
  * install/uninstall
  * install-dev/uninstall-dev

v0.2.3 (2019-06-11)
===================

* Using pyproject.toml, instead of the flawed setup.py

* Proper local install and uninstall. By Local we mean: not installing from PyPI.
  we had that in et/backbone using pip. But pip uses setup.py which we want to
  avoid. There is not pyproject.toml file sofar... 
  
Moving away from setup.py and going down the pyproject.toml road, we can choose 
between `poetry`_ and `flit`_.
  
Although, I am having some trouble with reusing some poetry code, i have the
impression that it is better developed, and has a more active community 
(more watchters, downloads, commits, ...)

A pyproject.toml was added (used ``poetry init`` to generate pyproject.toml). 
First issue is how to automatically transfer the version number to our python 
project. `Here <https://github.com/sdispater/poetry/issues/273>`_
is a good post about that. 
  
* using pkg_resources implies a dependence on setuptools = no go
* using tomlkit for reading the pyproject.toml file implies that the 
  pyproject.toml file must be included in the distribution of the 
  package. Since pyproject.toml is complete unnnecessary for the functioning  
  of the module, we'd rather not do that. So, we agree with copying the version
  string from pyproject.toms to the python package (=duplicating). This is 
  basically the same strategy as used by 
  `bumpversion <https://pypi.org/project/bumpversion/>`_.
  
* the command `poetry version ...` allows to modify the version string in 
  pyproject.toml. In principle we can recycle that code. However, we could not 
  get it to work properly (see issue `<https://github.com/sdispater/poetry/issues/1182>`_).
  This could probably be circumvented by creating my own fork of poetry.
  
  * it is simple to write a hack around this (read the file into a string, 
    replace the version line, and write it back. this preserves the formatting
    but in the unlikely case that there is another version string in some toml table
    it will be incorrect.
  * the `toml package <https://pypi.org/project/toml/>`_ is much simpler than tomlkit, does 
    not cause these problems, but it does not preserve the formatting  of the file.
    
* poetry itself uses a separate __version__.py file in the package, containing 
  nothin but ``__version__ = "M.m.p"``. This is imported in __init__.py as 
  ``from .__version__ import __version__``. This makes transferring the version
  from pyproject.toml to __version__.py easy.
  
Let's first check if we can achieve a proper local install with poetry ...
Install a package::

   > poetry build
   > pip install dist/<package>-<version>-py3-none-any.whl

Uninstall::

   > pip uninstall <package>

This seems to do the trick::

    > pip install -e <project_dir>
    
Install a dev package use cmd::

   > pip install --editable <project_dir>
   
Uninstall::

   > rm -r $(find . -name '*.egg-info')
   
But take care, uninstalling like this::

   > pip uninstall <package>

removed the source files. 
See `this post <https://stackoverflow.com/questions/17346619/how-to-uninstall-editable-packages-with-pip-installed-with-e>`_.


   
v0.1.21 (2019-06-11)
====================

first working version

v0.0.0 (2019-06-06)
===================

Start of development.

.. include:: ../TODO.rst

.. _flit: https://github.com/takluyver/flit  
