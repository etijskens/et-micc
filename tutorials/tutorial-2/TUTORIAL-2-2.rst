2.2 Building binary extensions from C++
---------------------------------------
.. note:: To add binary extension modules to a project, it must have a package structure.
   To check, you may run the ``micc info`` command:

   .. code-block:: bash

      > micc info
      Project ET-dot located at /Users/etijskens/software/dev/workspace/ET-dot
        package: et_dot
        version: 0.0.0
        structure: et_dot/__init__.py (Python package)
        contents:
          f2py module f2py_dotf/dotf.f90

Binary extionsion modules based on C++ are called cpp modules. This time we will call
the module :py:mod:`dotc` where the ``c`` stands for C++.

.. code-block:: bash

    > micc add dotc --cpp
    [INFO]           [ Adding cpp module dotc to project ET-dot.
    [INFO]               - C++ source in           ET-dot/et_dot/cpp_dotc/dotc.cpp.
    [INFO]               - module documentation in ET-dot/et_dot/cpp_dotc/dotc.rst (in restructuredText format).
    [INFO]               - Python test code in     ET-dot/tests/test_cpp_dotc.py.
    [WARNING]            Dependencies added. Run \'poetry update\' to update the project\'s virtual environment.
    [INFO]           ] done.

The output explains you where to add the C++ source code, the test code and the
documentation.  First take care of the warning::

    (.venv) > poetry update
    Updating dependencies
    Resolving dependencies... (1.7s)

    No dependencies to install or update

There is nothing to install, because micc-build_ was already installed when we added the Fortran
module :py:mod:`dotf` (see `2.1 Building binary extensions from Fortran`_).

We will be using pybind11_ to create Python wrappers for C++
functions. Pybind11_ is by far the most practical choice for this (see
https://channel9.msdn.com/Events/CPP/CppCon-2016/CppCon-2016-Introduction-to-C-python-extensions-and-embedding-Python-in-C-Apps
for a good overview of this topic). It has a lot of 'automagical' features, and
it has a header-only C++ library - so, thus effectively preventing installation problems.
`Boost.Python <https://www.boost.org/doc/libs/1_70_0/libs/python/doc/html/index.html>`_
offers very similar features, but is not header-only and its library depends on
the python version you want to use - so you need a different library for every
Python version you want to use.

Increment the minor component of the version string::

    (.venv) > micc version -m
    [INFO]           (ET-dot)> micc version (0.1.1) -> (0.2.0)

Enter this code in the C++ source file :file:`ET-dot/et_dot/cpp_dotc/dotc.cpp`

.. code-block:: c++

   #include <pybind11/pybind11.h>
   #include <pybind11/numpy.h>

   double
   dotc( pybind11::array_t<double> a
       , pybind11::array_t<double> b
       )
   {
       auto bufa = a.request()
          , bufb = b.request()
          ;
    // verify dimensions and shape:
       if( bufa.ndim != 1 || bufb.ndim != 1 ) {
           throw std::runtime_error("Number of dimensions must be one");
       }
       if( (bufa.shape[0] != bufb.shape[0]) ) {
           throw std::runtime_error("Input shapes must match");
       }
    // provide access to raw memory
    // because the Numpy arrays are mutable by default, py::array_t is mutable too.
    // Below we declare the raw C++ arrays for x and y as const to make their intent clear.
       double const *ptra = static_cast<double const *>(bufa.ptr);
       double const *ptrb = static_cast<double const *>(bufb.ptr);

       double d = 0.0;
       for (size_t i = 0; i < bufa.shape[0]; i++)
           d += ptra[i] * ptrb[i];

       return d;
   }

   // describe what goes in the module
   PYBIND11_MODULE(dotc, m)
   {// optional module docstring:
       m.doc() = "pybind11 dotc plugin";
    // list the functions you want to expose:
    // m.def("exposed_name", function_pointer, "doc-string for the exposed function");
       m.def("dotc", &dotc, "The dot product of two arrays 'a' and 'b'.");
   }

Obviously the C++ source code is more involved than its Fortran equivalent in the
previous section. This is because f2py_ is a program performing clever introspection
into the Fortran source code, whereas pybind11_ is nothing but a C++ template library.
As such it is not capable of introspection and the user is obliged to use
`pybind11 <https://pybind11.readthedocs.io/>`_ for accessing the arguments passed in
by Python.

Build the module. Because we do not want to rebuild the :py:mod:`dotf` module we add
``-m dotc`` to the command line, to indicate that only module :py:mod:`dotc` must be
built::

   (.venv)> micc build -m dotc
    [INFO] [ Building cpp module 'dotc':
    [DEBUG]          [ > cmake -D PYTHON_EXECUTABLE=/Users/etijskens/software/dev/workspace/tmp/ET-dot/.venv/bin/python -D pybind11_DIR=/Users/etijskens/software/dev/workspace/tmp/ET-dot/.venv/lib/python3.7/site-packages/et_micc_build/cmake_tools -D CMAKE_BUILD_TYPE=RELEASE ..
    [DEBUG]              (stdout)
                           -- The CXX compiler identification is AppleClang 11.0.0.11000033
                           -- Check for working CXX compiler: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++
                           -- Check for working CXX compiler: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ -- works
                           -- Detecting CXX compiler ABI info
                           -- Detecting CXX compiler ABI info - done
                           -- Detecting CXX compile features
                           -- Detecting CXX compile features - done
                           -- Found PythonInterp: /Users/etijskens/software/dev/workspace/tmp/ET-dot/.venv/bin/python (found version "3.7.5")
                           -- Found PythonLibs: /Users/etijskens/.pyenv/versions/3.7.5/lib/libpython3.7m.a
                           -- Performing Test HAS_CPP14_FLAG
                           -- Performing Test HAS_CPP14_FLAG - Success
                           -- Performing Test HAS_FLTO
                           -- Performing Test HAS_FLTO - Success
                           -- LTO enabled
                           -- Configuring done
                           -- Generating done
                           -- Build files have been written to: /Users/etijskens/software/dev/workspace/tmp/ET-dot/et_dot/cpp_dotc/_cmake_build
    [DEBUG]          ] done.
    [DEBUG]          [ > make
    [DEBUG]              (stdout)
                           Scanning dependencies of target dotc
                           [ 50%] Building CXX object CMakeFiles/dotc.dir/dotc.cpp.o
                           [100%] Linking CXX shared module dotc.cpython-37m-darwin.so
                           [100%] Built target dotc
    [DEBUG]          ] done.
    [DEBUG]          >>> os.remove(/Users/etijskens/software/dev/workspace/tmp/ET-dot/et_dot/cpp_dotc/dotc.cpython-37m-darwin.so)
    [DEBUG]          >>> shutil.copyfile( '/Users/etijskens/software/dev/workspace/tmp/ET-dot/et_dot/cpp_dotc/_cmake_build/dotc.cpython-37m-darwin.so', '/Users/etijskens/software/dev/workspace/tmp/ET-dot/et_dot/cpp_dotc/dotc.cpython-37m-darwin.so' )
    [DEBUG]          [ > ln -sf /Users/etijskens/software/dev/workspace/tmp/ET-dot/et_dot/cpp_dotc/dotc.cpython-37m-darwin.so /Users/etijskens/software/dev/workspace/tmp/ET-dot/et_dot/cpp_dotc/dotc.cpython-37m-darwin.so
    [DEBUG]          ] done.
    [INFO] ] done.
    [INFO]           Binary extensions built successfully:
    [INFO]           - /Users/etijskens/software/dev/workspace/tmp/ET-dot/et_dot/dotc.cpython-37m-darwin.so
    (.venv)   >

The output shows that first ``CMake`` is called, then ``make``, and finally the binary extension is
installed with a soft link.

As usual the ``micc-build`` command produces a lot of output, most of which is rather uninteresting
- except in the case of errors. If the source file does not have any syntax errors, and the build
did not experience any problems, you will see a file like :file:`dotf.cpython-37m-darwin.so` in
directory :file:`ET-dot/et_dot`::

    (.venv) > ls -l et_dot
    total 8
    -rw-r--r--  1 etijskens  staff  1339 Dec 13 14:40 __init__.py
    drwxr-xr-x  4 etijskens  staff   128 Dec 13 14:29 __pycache__/
    drwxr-xr-x  7 etijskens  staff   224 Dec 13 14:43 cpp_dotc/
    lrwxr-xr-x  1 etijskens  staff    93 Dec 13 14:43 dotc.cpython-37m-darwin.so@ -> /Users/etijskens/software/dev/workspace/tmp/ET-dot/et_dot/cpp_dotc/dotc.cpython-37m-darwin.so
    lrwxr-xr-x  1 etijskens  staff    94 Dec 13 14:27 dotf.cpython-37m-darwin.so@ -> /Users/etijskens/software/dev/workspace/tmp/ET-dot/et_dot/f2py_dotf/dotf.cpython-37m-darwin.so
    drwxr-xr-x  6 etijskens  staff   192 Dec 13 14:43 f2py_dotf/
    (.venv) >

.. note:: The extension of the module :file:`dotc.cpython-37m-darwin.so`
   will depend on the Python version you are using, and on the operating system.

Increment the version string::

    (.venv) > micc version -p
    [INFO]           (ET-dot)> micc version (0.2.0) -> (0.2.1)

Here is the test code. It is almost exactly the same as that for the f2py module :py:mod:`dotf`,
except for the module name. Enter the test code in :file:`ET-dot/tests/test_cpp_dotc.py`:

.. code-block:: python

   # import our binary extension
   import et_dot.dotc as cpp
   import numpy as np

   def test_dotc_aa():
       a = np.array([0,1,2,3,4],dtype=np.float)
       expected = np.dot(a,a)
       a_dotc_a = cpp.dotc(a,a)
       assert a_dotc_a==expected

The conversion between the Numpy arrays to C++ arrays is here less magical, as the user
must provide code to do the conversion of Python variables to C++. This has the advantage
of showing the mechanics of the conversion more clearly, but it also leaves more space for
mistakes, and to beginners it may seem more complicated.

Finally, run pytest:

.. code-block:: bash

   > pytest
   ================================ test session starts =================================
   platform darwin -- Python 3.7.4, pytest-4.6.5, py-1.8.0, pluggy-0.13.0
   rootdir: /Users/etijskens/software/dev/workspace/ET-dot
   collected 9 items

   tests/test_cpp_dotc.py .                                                       [ 11%]
   tests/test_et_dot.py .......                                                   [ 88%]
   tests/test_f2py_dotf.py .                                                      [100%]

   ============================== 9 passed in 0.28 seconds ==============================

All our tests passed.

Increment the version string and tag::

    (.venv) > micc version -m -t
    [INFO] Creating git tag v0.3.0 for project ET-dot
    [INFO] Done.
