Tutorial 2: Binary extensions
=============================

Suppose for a moment that Numpy_ did not have a dot product implementation and that
the implementation provided in Tutorial-1 is way too slow to be practical for your
research project. Consequently, you are forced to accelarate your dot product code
in some way or another. There are several approaches for this. Here are a number of
interesting links covering them:

* `Why you should use Python for scientific research <https://developer.ibm.com/dwblog/2018/use-python-for-scientific-research/>`_
* `Performance Python: Seven Strategies for Optimizing Your Numerical Code <https://www.youtube.com/watch?v=zQeYx87mfyw>`_
* `High performance Python 1 <http://www.admin-magazine.com/HPC/Articles/High-Performance-Python-1>`_
* `High performance Python 2 <http://www.admin-magazine.com/HPC/Articles/High-Performance-Python-2>`_
* `High performance Python 3 <http://www.admin-magazine.com/HPC/Articles/High-Performance-Python-3>`_
* `High performance Python 4 <http://www.admin-magazine.com/HPC/Articles/High-Performance-Python-4>`_

Most of these approaches do not require special support from Micc_ to get you going, and
we encourage you to go try out the *High Performance Python* series 1-3 for the ET-dot
project. Two of the approaches discussed involve rewriting your code in Modern Fortran or
C++ and generate a shared library that can be imported in Python just as any Python module.
Such shared libraries are called *binary extension modules*. Constructing binary extension
modules is by far the most scalable and flexible of all current acceleration strategies, as
these languages are designed to squeeze the maximum of performance out of a CPU. However,
figuring out how to make this work is a bit of a challenge, especially in the case of C++.

This is in fact one of the main reasons why Micc_ was designed: facilitating the construction
of binary extension modules and enabling the developer to create high performance tools with
ease.

2.1 Binary extensions in Micc_ projects
---------------------------------------
Micc_ provides boilerplate code for binary extensions as well as some practical wrappers
around top-notch tools for building binary extensions from Fortran and C++. Fortran code
is compiled into a Python module using `f2py <https://docs.scipy.org/doc/numpy/f2py/>`_
(which comes with Numpy_). For C++ we use Pybind11_ and `CMake <https://cmake.org>`_.

Adding a binary extension is as simple as:

.. code-block:: bash

   > micc add foo --f2py   # add a binary extension 'foo' written in Fortran
   > micc add bar --cpp    # add a binary extension 'bar' written in C++

.. note::
    For the ``micc add`` command to be valid, your project must have a package
    structure (see `Modules and packages`_).

Enter your own code in the generated source code files and execute :

.. code-block:: bash

   (.venv) > micc-build

.. note::
    The virtual environment must be activated to execute the ``micc-build``
    command (see `Virtual environments`_).

If there are no syntax errors your binary extensions will be built, and you
will be able to import the  modules :py:mod:`foo` and :py:mod:`bar` in your
project and use their subroutines and functions. Because :py:mod:`foo` and
:py:mod:`bar` are submodules of your micc_ project, you must import them as::

    import my_package.foo
    import my_package.bar

    # call foofun in my_package.foo
    my_package.foo.foofun(...)

    # call barfun in my_package.bar
    my_package.bar.barfun(...)

where :py:mod:`my_package` is the name of the top package of your micc_ project.

Choosing between Fortran and C++ for binary extension modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Here are a number of arguments that you may wish to take into account for choosing the
programming language for your binary extension modules:

* Fortran is a simpler language than C++
* It is easier to write efficient code in Fortran than C++.
* C++ is a much more expressive language
* C++ comes with a huge standard library, providing lots of data structures and algorithms
  that are hard to match in Fortran. If the standard library is not enough, there is also
  the highly recommended `Boost <https://boost.org>`_ libraries and many other domain
  specific libraries. There are also domain specific libraries in Fortran, but the amount
  differs by an order of magnitude at least.
* With Pybind11_ you can almost expose anything from the C++ side to Python, not just
  functions.
* Modern Fortran is (imho) not as good documented as C++. Useful place to look for
  language features and idioms are:

  * https://www.fortran90.org/
  * http://www.cplusplus.com/
  * https://en.cppreference.com/w/

In short, C++ provides much more possibilities, but it is not for the novice.
As to my own experience, I discovered that working on projects of moderate complexity
I progressed significantly faster using Fortran rather than C++, despite the fact that
my knowledge of Fortran is quite limited compared to C++. However, your mileage may vary.

2.2 Building binary extensions from Fortran
-------------------------------------------
Binary extension modules based on Fortran are called *f2py modules* because micc_ uses
the f2py_ tool to build these binary extension modules from Fortran. F2py_ is part of
Numpy_.

.. note::
    To be able to add a binary extension module (as well as any other component supported
    by micc_, such as Python modules or CLI applications) to a micc_ project, your project
    must have a package structure. This is easily checked by running the ``micc info`` command::

        > micc info
        Project ET-dot located at /home/bert/software/workspace/ET-dot
          package: et_dot
          version: 0.0.0
          structure: et_dot/__init__.py (Python package)
        >

    If it does, the *structure* line of the output will read as above. If, however, the
    *structure* line reads::

        structure: et_dot.py (Python module)

    you should convert it by running::

        > micc convert-to-package --overwrite

    See `Modules and packages`_ for details.

We are now ready to create a f2py module for a Fortran implementation fof the
dot product, say :py:mod:`dotf`, where the ``f``, obviously, stands for Fortran:

.. code-block:: bash

    > micc add dotf --f2py
    [INFO]           [ Adding f2py module dotf to project ET-dot.
    [INFO]               - Fortran source in       ET-dot/et_dot/f2py_dotf/dotf.f90.
    [INFO]               - Python test code in     ET-dot/tests/test_f2py_dotf.py.
    [INFO]               - module documentation in ET-dot/et_dot/f2py_dotf/dotf.rst (in restructuredText format).
    [WARNING]            Dependencies added. Run \'poetry update\' to update the project\'s virtual environment.
    [INFO]           ] done.

The output tells us where to enter the Fortran source code, the test code and the documentation.
Enter the Fortran implementation of the dot product below in the Fortran source file
:file:`ET-dot/et_dot/f2py_dotf/dotf.f90` (using your favourite editor or an IDE):

.. code-block:: fortran

   function dotf(a,b,n)
     ! Compute the dot product of a and b
     !
       implicit none
     !-------------------------------------------------------------------------------------------------
       integer*4              , intent(in)    :: n
       real*8   , dimension(n), intent(in)    :: a,b
       real*8                                 :: dotf
     !-------------------------------------------------------------------------------------------------
     ! declare local variables
       integer*4 :: i
     !-------------------------------------------------------------------------------------------------
       dotf = 0.
       do i=1,n
           dotf = dotf + a(i) * b(i)
       end do
   end function dotf

The output of the ``micc add dotf --f2py`` command above also shows a warning::

    [WARNING]            Dependencies added. Run `poetry update` to update the project's virtual environment.

Micc_ is telling you that it added some dependencies to your project. In order to be able to build the binary
extension *dotf* these dependencies must be installed in the virtual environment of our project by running
``poetry update``.

.. code-block:: bash

    > poetry update
    Updating dependencies
    Resolving dependencies... (2.5s)

    Writing lock file


    Package operations: 40 installs, 0 updates, 0 removals

      - Installing certifi (2019.11.28)
      - Installing chardet (3.0.4)
      - Installing idna (2.8)
      - Installing markupsafe (1.1.1)
      - Installing python-dateutil (2.8.1)
      - Installing pytz (2019.3)
      - Installing urllib3 (1.25.7)
      - Installing alabaster (0.7.12)
      - Installing arrow (0.15.4)
      - Installing babel (2.7.0)
      - Installing docutils (0.15.2)
      - Installing imagesize (1.1.0)
      - Installing jinja2 (2.10.3)
      - Installing pygments (2.5.2)
      - Installing requests (2.22.0)
      - Installing snowballstemmer (2.0.0)
      - Installing sphinxcontrib-applehelp (1.0.1)
      - Installing sphinxcontrib-devhelp (1.0.1)
      - Installing sphinxcontrib-htmlhelp (1.0.2)
      - Installing sphinxcontrib-jsmath (1.0.1)
      - Installing sphinxcontrib-qthelp (1.0.2)
      - Installing sphinxcontrib-serializinghtml (1.1.3)
      - Installing binaryornot (0.4.4)
      - Installing click (7.0)
      - Installing future (0.18.2)
      - Installing jinja2-time (0.2.0)
      - Installing pbr (5.4.4)
      - Installing poyo (0.5.0)
      - Installing sphinx (2.2.2)
      - Installing whichcraft (0.6.1)
      - Installing cookiecutter (1.6.0)
      - Installing semantic-version (2.8.3)
      - Installing sphinx-click (2.3.1)
      - Installing sphinx-rtd-theme (0.4.3)
      - Installing tomlkit (0.5.8)
      - Installing walkdir (0.4.1)
      - Installing et-micc (0.10.10)
      - Installing numpy (1.17.4)
      - Installing pybind11 (2.4.3)
      - Installing et-micc-build (0.10.10)

Note from the last lines in the output that `micc-build <https://github.com/etijskens/et-micc-build>`_,
which is a companion of Micc_ that encapsulates the machinery that does the hard work of building the
binary extensions, depends on pybind11_, Numpy_, and on micc_ itself. As a consaequence, micc_ is now
also installed in the projects virtual environment. Therefore, when the project's virtual environment
is activated, the active ``micc`` is the one in the project's virtual environment::

    > source .venv/bin/activate
    (.venv) > which micc
    path/to/ET-dot/.venv/bin/micc
    (.venv) >

We might want to increment the minor component of the version string by now::

    (.venv) > micc version -m
    [INFO]           (ET-dot)> micc version (0.0.7) -> (0.1.0)

The binary extension module can now be built::

    (.venv) > micc-build
    [INFO] [ Building f2py module dotf in directory '/Users/etijskens/software/dev/workspace/ET-dot/et_dot/f2py_dotf/build_'
    ...
    [DEBUG]          >>> shutil.copyfile( 'dotf.cpython-37m-darwin.so', '/Users/etijskens/software/dev/workspace/ET-dot/et_dot/dotf.cpython-37m-darwin.so' )
    [INFO] ] done.
    [INFO] Check /Users/etijskens/software/dev/workspace/ET-dot/micc-build-f2py_dotf.log for details.
    [INFO] Binary extensions built successfully:
    [INFO] - ET-dot/et_dot/dotf.cpython-37m-darwin.so
    (.venv) >

This command produces a lot of output, most of which is rather uninteresting - except in the
case of errors. At the end is a summary of all binary extensions that have been built, or
failed to build. If the source file does not have any syntax errors, you will see a file like
:file:`dotf.cpython-37m-darwin.so` in directory :file:`ET-dot/et_dot`::

    (.venv) > ls -l et_dot
    total 8
    -rw-r--r--  1 etijskens  staff  720 Dec 13 11:04 __init__.py
    drwxr-xr-x  6 etijskens  staff  192 Dec 13 11:12 f2py_dotf/
    lrwxr-xr-x  1 etijskens  staff   92 Dec 13 11:12 dotf.cpython-37m-darwin.so@ -> path/to/ET-dot/et_dot/f2py_foo/foo.cpython-37m-darwin.so

.. note::
    The extension of the module :file:`dotf.cpython-37m-darwin.so` will depend on the Python
    version (c.q. 3.7) you are using, and on your operating system (c.q. MacOS).

Since our binary extension is built, we can test it. Here is some test code. Enter it in file
:file:`ET-dot/tests/test_f2py_dotf.py`:

.. code-block:: python

   # import the binary extension and rename the module locally as f90
   import et_dot.dotf as f90
   import numpy as np

   def test_dotf_aa():
       a = np.array([0,1,2,3,4],dtype=np.float)
       expected = np.dot(a,a)
       a_dotf_a = f90.dotf(a,a)
       assert a_dotf_a==expected

The astute reader will notice the magic that is happening here: *a* is a numpy array,
which is passed as is to our :py:meth:`et_dot.dotf.dotf` function in our binary extension.
An invisible wrapper function will check the types of the numpy arrays, retrieve pointers
to the memory of the numpy arrays and feed those pointers into our Fortran function, the
result of which is stored in a Python variable :py:obj:`a_dotf_a. If you look carefully
at the output of ``micc-build``, you will see information about the wrappers that f2py
constructed.

Passing Numpy arrays directly to Fortran routines is extremely productive.
Many useful Python packages use numpy for arrays, vectors, matrices, linear algebra, etc.
By being able to pass Numpy arrays directly into your own number crunching routines
relieves you from conversion between array types. In addition you can do the memory
management of your arrays and their initialization in Python.

As you can see we test the outcome of dotf against the outcome of :py:meth:`numpy.dot`.
We thrust that outcome, but beware that this test may be susceptible to round-off error
because the representation of floating point numbers in Numpy and in Fortran may differ
slightly.

Here is the outcome of ``pytest``:

.. code-block:: bash

   > pytest
   ================================ test session starts =================================
   platform darwin -- Python 3.7.4, pytest-4.6.5, py-1.8.0, pluggy-0.13.0
   rootdir: /Users/etijskens/software/dev/workspace/ET-dot
   collected 8 items

   tests/test_et_dot.py .......                                                   [ 87%]
   tests/test_f2py_dotf.py .                                                      [100%]

   ============================== 8 passed in 0.16 seconds ==============================
   >

All our tests passed. Of course we can extend the tests in the same way as we did for the
naive Python implementation in the previous tutorial. We leave that as an exercise to the
reader.

Increment the version string and produce tag::

    (.venv) > micc version -p -t
    [INFO]           (ET-dot)> micc version (0.1.0) -> (0.1.1)
    [INFO]           Creating git tag v0.1.1 for project ET-dot
    [INFO]           Done.

.. Note:: If you put your subroutines and functions inside a Fortran module, as in:

   .. code-block:: fortran

      MODULE my_f90_module
        implicit none
        contains
          function dot(a,b)
            ...
          end function dot
      END MODULE my_f90_module

   then the binary extension module will expose the Fortran module name :py:obj:`my_f90_module`
   which in turn exposes the function/subroutine names:

   .. code-block:: Python

      >>> import et_dot
      >>> a = [1.,2.,3.]
      >>> b = [2.,2.,2.]
      >>> et_dot.dot(a,b)
      >>> AttributeError
      Module et_dot has no attribute 'dot'.
      >>> et_dot.my_F90_module.dot(a,b)
      12.0

   If you are bothered by having to type ``et_dot.my_F90_module.`` every time, use this trick::

      >>> import et_dot
      >>> f90 = et_dot.my_F90_module
      >>> f90.dot(a,b)
      12.0
      >>> fdot = et_dot.my_F90_module.dot
      >>> fdot(a,b)
      12.0

2.3 Building binary extensions from C++
---------------------------------------
To illustrate building binary extension modules from C++ code, let us also create a
C++ implementation for the dot product. Such modules are called *cpp modules*.
Analogously to our :py:mod:`dotf` module we will call the cpp module :py:mod:`dotc`,
the ``c`` referring to C++.

.. note::
    To add binary extension modules to a project, it must have a package structure.
    To check, you may run the ``micc info`` command and verify the structure line.
    If it mentions ``Python module``, you must convert the structure by running
    ``micc convert-to-package --overwrite``. See `Modules and packages`_ for details.

Use the ``micc add`` command to add a cpp module:

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

Typically, there will be nothing to install, because micc-build_ was already installed when
we added the Fortran module :py:mod:`dotf` (see `2.2 Building binary extensions from Fortran`_).
Sometimes one of the packages you depend on may just have seen a new release and poetry_ will
perform an upgrade::

    (.venv) > poetry update
    Updating dependencies
    Resolving dependencies... (1.6s)
    Writing lock file
    Package operations: 0 installs, 1 update, 0 removals
      - Updating zipp (0.6.0 -> 1.0.0)
    (.venv) >

Micc_ uses pybind11_ to create Python wrappers for C++ functions. This
is by far the most practical choice for this (see
https://channel9.msdn.com/Events/CPP/CppCon-2016/CppCon-2016-Introduction-to-C-python-extensions-and-embedding-Python-in-C-Apps
for a good overview of this topic). It has a lot of 'automagical' features, and
it has a header-only C++ library - so, thus effectively preventing installation problems.
`Boost.Python <https://www.boost.org/doc/libs/1_70_0/libs/python/doc/html/index.html>`_
offers very similar features, but is not header-only and its library depends on
the python version you want to use - so you need a different library for every
Python version you want to use.

This is a good point to increment the minor component of the version string::

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

We can now build the module. Because we do not want to rebuild the :py:mod:`dotf` module
we add ``-m dotc`` to the command line, to indicate that only module :py:mod:`dotc` must
be built::

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

The output shows that first ``CMake`` is called, followed by ``make`` and the installation
of the binary extension with a soft link. Finally, lists of modules that have been built
successfully, and modules that failed to build are output.

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

Although we haven't tested :py:mod:`dotc`, this is a good point to increment the version
string::

    (.venv) > micc version -p
    [INFO]           (ET-dot)> micc version (0.2.0) -> (0.2.1)

Here is the test code. It is almost exactly the same as that for the f2py module :py:mod:`dotf`,
except for the module name. Enter the test code in :file:`ET-dot/tests/test_cpp_dotc.py`:

.. code-block:: python

   import et_dot.dotc as cpp    # import the binary extension
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

All our tests passed, which is a good reason to increment the version string and
create a tag::

    (.venv) > micc version -m -t
    [INFO] Creating git tag v0.3.0 for project ET-dot
    [INFO] Done.

2.4 Data type issues
--------------------

An important point of attention when writing binary extension modules - and a
common source of problems - is that the data types of the variables passed in from
Python must match the data types of the Fortran or C++ routines.

Here is a table with the most relevant numeric data types in Python, Fortran and C++.

================  ============   =========   ====================
kind              Numpy/Python   Fortran     C++
================  ============   =========   ====================
unsigned integer  uint32         N/A         signed long int
unsigned integer  uint64         N/A         signed long long int
signed integer    int32          integer*4   signed long int
signed integer    int64          integer*8   signed long long int
floating point    float32        real*4      float
floating point    float64        real*8      double
complex           complex64      complex*4   std::complex<float>
complex           complex128     complex*8   std::complex<double>
================  ============   =========   ====================

F2py
^^^^
F2py_ is very flexible with respect to data types. In between the
Fortran routine and Python call is a wrapper function which translates the
function call, and if it detects that the data type on the Python sides and
the Fortran sideare different, the wrapper function is allowed to copy/convert
the variable when passing it to Fortran routine both, and also when passing the
result back from the Fortran routine to the Python caller. When the input/output
variables are large arrays copy/conversion operations can have a detrimental
effect on performance and this is in HPC highly undesirable. Micc_ runs f2py_ with
the ``-DF2PY_REPORT_ON_ARRAY_COPY=1`` option. This causes your code to produce a
warning everytime the wrapper decides to copy an array. Basically, this warning
means that you have to modify your Python data structure to have the same data
type as the Fortran source code, or vice versa.

Returning large data structures
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The result of a Fortran function and a C++ function is **always** copied back to the
Python variable that will hold it. As copying large data structures is detrimental
to performance this shoud be avoided. The solution to this problem is to write
Fortran functions or subroutines and C++ functions that accept the result variable
as an argument and modify it in place, so that the copy operaton is avoided. Consider
this example of a Fortran subroutine that computes the sum of two arrays.
are some examples of array addition:

.. code-block:: fortran

   subroutine add(a,b,sumab,n)
     ! Compute the sum of arrays a and b and overwrite array sumab with the result
       implicit none

       integer*4              , intent(in)    :: n
       real*8   , dimension(n), intent(in)    :: a,b
       real*8   , dimension(n), intent(inout) :: sumab

     ! declare local variables
       integer*4 :: i

       do i=1,n
           sumab(i) = a(i) + b(i)
       end do
   end subroutine add

The crucial issue here is that the result array *sumab* has ``intent(inout)``. If
you qualify the intent of *sumab* as ``in`` you will not be able to overwrite it,
whereas - surprisingly - qualifying it with ``intent(out)`` will force f2py to consider
it as a left hand side variable, which implies copying the result on returning.

The code below does exactly the same but uses a function, not to return the result
of the computation, but an error code.

.. code-block:: fortran

   function add(a,b,sumab,n)
     ! Compute the sum of arrays a and b and overwrite array sumab with the result
       implicit none

       integer*4              , intent(in)    :: n,add
       real*8   , dimension(n), intent(in)    :: a,b
       real*8   , dimension(n), intent(inout) :: sumab

     ! declare local variables
       integer*4 :: i

       do i=1,n
           sumab(i) = a(i) + b(i)
       end do

       add = ... ! set return value, e.g. an error code.

   end function add

The same can be accomplished in C++:

.. code-block:: c++

   #include <pybind11/pybind11.h>
   #include <pybind11/numpy.h>

   namespace py = pybind11;

   void
   add ( py::array_t<double> a
       , py::array_t<double> b
       , py::array_t<double> sumab
       )
   {// request buffer description of the arguments
       auto buf_a = a.request()
          , buf_b = b.request()
          , buf_sumab = sumab.request()
          ;
       if( buf_a.ndim != 1
        || buf_b.ndim != 1
        || buf_sumab.ndim != 1 )
       {
           throw std::runtime_error("Number of dimensions must be one");
       }

       if( (buf_a.shape[0] != buf_b.shape[0])
        || (buf_a.shape[0] != buf_sumab.shape[0]) )
       {
           throw std::runtime_error("Input shapes must match");
       }
    // because the Numpy arrays are mutable by default, py::array_t is mutable too.
    // Below we declare the raw C++ arrays for a and b as const to make their intent clear.
       double const *ptr_a     = static_cast<double const *>(buf_a.ptr);
       double const *ptr_b     = static_cast<double const *>(buf_b.ptr);
       double       *ptr_sumab = static_cast<double       *>(buf_sumab.ptr);

       for (size_t i = 0; i < buf_a.shape[0]; i++)
           ptr_sumab[i] = ptr_a[i] + ptr_b[i];
   }


   PYBIND11_MODULE({{ cookiecutter.module_name }}, m)
   {// optional module doc-string
       m.doc() = "pybind11 {{ cookiecutter.module_name }} plugin"; // optional module docstring
    // list the functions you want to expose:
    // m.def("exposed_name", function_pointer, "doc-string for the exposed function");
       m.def("add", &add, "A function which adds two arrays 'a' and 'b' and stores the result in the third, 'sumab'.");
   }

Here, care must be taken that when casting ``buf_sumab.ptr`` one does not cast to const.

2.5 Specifying compiler options for binary extension modules
------------------------------------------------------------

[ **Advanced Topic** ]
As we have seen, binary extension modules can be programmed in Fortran and C++.
Micc_ provides convenient wrappers to build such modules. Fortran source code is
transformed to a python module using f2py_, and C++ source using Pybind11_ and
CMake_. Obviously, in both cases there is a compiler under the hood doing the
hard work. By default these tools use the compiler they find on the path, but
you may as well specify your favorite compiler.

.. note::
    Compiler options are distinct for f2py modules and cpp modules.

Building a single module only
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you want to build a single binary extension module rather than all binary
extension modules in the project, add the ``-m|--module`` option:

.. code-block::

   > micc-build --module my_module <build options>

This will only build module *my_module*.

.. note::
    If you do not use ``--module my_module``, the f2py options apply to all f2py
    modules in the project, and the cpp options to all cpp modules in the project.

Performing a clean build
^^^^^^^^^^^^^^^^^^^^^^^^
To perform a clean build, add the ``--clean`` flag to the ``micc build`` command:

.. code-block::

   > micc-build --clean <other options>

This will remove the previous build directory and as well as the binary extension
module.

Controlling the build of f2py modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To specify the Fortran compiler, e.g. the GNU fortran compiler:

.. code-block::

   > micc-build --f90exec path/to/gfortran

Note, that this exactly how you would have specified it using f2py_ directly.
You can specify the Fortran compiler options you want using the ``--f90flags``
option:

.. code-block::

   > micc-build --f90flags "string with all my favourit options"

In addition f2py_ (and ``micc-build`` for that matter) provides two extra options
``--opt`` for specifying optimization flags, and ``--arch`` for specifying architecture
dependent optimization flags. These flags can be turned off by adding ``--noopt`` and
``--noarch``, respectively. This can be convenient when exploring compile options.
Finally, the ``--debug`` flag adds debug information during the compilation.

``Micc_ build`` also provides a ``--build-type`` options which accepts ``release`` and
``debug`` as value (case insensitive). Specifying ``debug`` is equivalent to
``--debug --noopt --noarch``.

.. note:: ALL f2py modules are built with the same options. To specify separate options
   for a particular module use the ``-m|--module`` option.

.. note:: Although there are some commonalities between the compiler options of the
   various compilers, you will most probably have to change the compiler options when
   you change the compiler.

Controlling the build of cpp modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The build of C++ modules can be fully controlled by modifying the the module's
:file:`CMakeLists.txt` file to your needs. Micc_ provides every cpp module with
a template containing examples of frequently used CMake_ commands commented out.
These include the specification of :

* compiler options
* preprocessor macros
* include directories
* link directories
* link libraries

You just need to uncomment them and provide the values you need:

.. code-block:: cmake

    ...
    # set compiler:
    # set(CMAKE_CXX_COMPILER path/to/executable)

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
    ...

CMake_ provides default build options for four build types: DEBUG, MINSIZEREL,
RELEASE, and RELWITHDEBINFO.

* ``CMAKE_CXX_FLAGS_DEBUG     ``: ``-g``
* ``CMAKE_CXX_FLAGS_MINSIZEREL``: ``-Os -DNDEBUG``
* ``CMAKE_CXX_FLAGS_RELEASE   ``: ``-O3 -DNDEBUG``
* ``CMAKE_CXX_FLAGS_RELWITHDEBINFO``: ``-O2 -g -DNDEBUG``

The build type is selected by setting the ``CMAKE_BUILD_TYPE`` variable (default:
``RELEASE``).

For convenience, micc-build_ provides a command line argument ``--build-type`` for
specifying the build type.

Save and load build options to/from file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
With the ``--save`` option you can save the current build options to a file in .json
format. This acts on a per project basis. E.g.:

.. code-block::

   > micc-build <my build options> --save build[.json]

will save the *<my build options>* to the file :file:`build.json` in every binary module
directory (the .json extension is added if omitted). You can restrict this to a single
module with the ``--module`` option (see above). The saved options can be reused in a
later build as:

.. code-block::

   > micc-build --load build[.json]

2.6 Documenting binary extension modules
----------------------------------------

For Python modules the documentation is automatically extracted from the doc-strings
in the module. However, when it comes to documenting binary extension modules, this
does not seem a good option. Ideally, the source files :file:`ET-dot/et_dot/f2py_dotf/dotf.f90`
amnd :file:`ET-dot/et_dot/cpp_dotc/dotc.cpp` should document the Fortran functions and
subroutines, and C++ functions, respectively, rahter than the Python interface. Yet
from the perspective of ET-dot being a Python project, the users is only interested
in the documentation of the Python interface to those functions and subroutines.
Therefore, micc_ requires you to document the Python interface in separate :file:`.rst`
files:

* :file:`ET-dot/et_dot/f2py_dotf/dotf.rst`
* :file:`ET-dot/et_dot/cpp_dotc/dotc.rst`

Here are the contents, respectively, for :file:`ET-dot/et_dot/f2py_dotf/dotf.rst`:

.. code-block:: rst

   Module et_dot.dotf
   ******************

   Module :py:mod:`dotf` built from fortran code in :file:`f2py_dotf/dotf.f90`.

   .. function:: dotf(a,b)
      :module: et_dot.dotf

      Compute the dot product of *a* and *b* (in Fortran.)

      :param a: 1D Numpy array with ``dtype=numpy.float64``
      :param b: 1D Numpy array with ``dtype=numpy.float64``
      :returns: the dot product of *a* and *b*
      :rtype: ``numpy.float64``

and for :file:`ET-dot/et_dot/cpp_dotc/dotc.rst`:

.. code-block:: rst

   Module et_dot.dotc
   ******************

   Module :py:mod:`dotc` built from fortran code in :file:`cpp_dotc/dotc.cpp`.

   .. function:: dotc(a,b)
      :module: et_dot.dotc

      Compute the dot product of *a* and *b* (in C++.)

      :param a: 1D Numpy array with ``dtype=numpy.float64``
      :param b: 1D Numpy array with ``dtype=numpy.float64``
      :returns: the dot product of *a* and *b*
      :rtype: ``numpy.float64``

Note that the documentation must be entirely in :file:`.rst` format (see
restructuredText_).

Build the documentation::

    (.venv) > cd docs && make html
    Already installed: click
    Already installed: sphinx-click
    Already installed: sphinx
    Already installed: sphinx-rtd-theme
    Running Sphinx v2.2.2
    making output directory... done
    WARNING: html_static_path entry '_static' does not exist
    building [mo]: targets for 0 po files that are out of date
    building [html]: targets for 7 source files that are out of date
    updating environment: [new config] 7 added, 0 changed, 0 removed
    reading sources... [100%] readme
    looking for now-outdated files... none found
    pickling environment... done
    checking consistency... /Users/etijskens/software/dev/workspace/tmp/ET-dot/docs/apps.rst: WARNING: document isn't included in any toctree
    done
    preparing documents... done
    writing output... [100%] readme
    generating indices...  genindex py-modindexdone
    highlighting module code... [100%] et_dot.dotc
    writing additional pages...  search/Users/etijskens/software/dev/workspace/tmp/ET-dot/.venv/lib/python3.7/site-packages/sphinx_rtd_theme/search.html:20: RemovedInSphinx30Warning: To modify script_files in the theme is deprecated. Please insert a <script> tag directly in your theme instead.
      {{ super() }}
    done
    copying static files... ... done
    copying extra files... done
    dumping search index in English (code: en)... done
    dumping object inventory... done
    build succeeded, 2 warnings.

    The HTML pages are in _build/html.

The documentation is built using ``make``. The :file:`Makefile` checks that the necessary components
sphinx_, click_, sphinx-click_and `sphinx-rtd-theme <https://sphinx-rtd-theme.readthedocs.io/en/stable/>`_ are installed.

You can view the result in your favorite browser::

    (.venv) > open _build/html/index.html

The filepath is made evident from the last output line above.
This is what the result looks like (html):

.. image:: ../tutorials/img2-1.png

Increment the version string:

    (.venv) > micc version -M -t
    [ERROR]
    Not a project directory (/Users/etijskens/software/dev/workspace/tmp/ET-dot/docs).
    (.venv) > cd ..
    (.venv) > micc version -M -t
    [INFO]           (ET-dot)> micc version (0.3.0) -> (1.0.0)
    [INFO]           Creating git tag v1.0.0 for project ET-dot
    [INFO]           Done.

Note that we first got an error because we are still in the docs directory, and not in
the project root directory.