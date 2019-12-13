2.1 Building binary extensions from Fortran
-------------------------------------------
Binary extension modules based on Fortran are called *f2py modules* because these 
modules are build with the f2py tool, which is part of Numpy. Since our project 
ET-dot now has a package structure, we are now ready to add a f2py module. Let us 
call this module :py:mod:`dotf`, where the ``f`` stands for Fortran:

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

.. note:: The extension of the module :file:`dotf.cpython-37m-darwin.so` 
   will depend on the Python version you are using, and on youe operating system.

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
   
All our tests passed. Of course we can extend the tests in the same way as we dit for the 
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
