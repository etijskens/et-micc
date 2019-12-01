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
   [WARNING]            Dependencies added. Run `poetry update` to update the project's virtual environment.
   [INFO]           ] done.
 
 The output explains you where to put the Fortran source code, the test code and the documentation  
 Enter this code in the Fortran source file :file:`ET-dot/et_dot/f2py_dotf/dotf.f90`
 
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
 
Before you can build the module, take notes of the WARNING that was printed on adding the
:py:mod:`dotf` module::

   [WARNING]            Dependencies added. Run `poetry update` to update the project's virtual environment.

To build the binary extension, you need some tools which ar not yet in Micc_ itself. In
particular you need `micc-build <https://github.com/etijskens/et-micc-build>`_, which on
its turn depends on Numpy_, pybind11_ and CMake_. To install them in your local virtual
environment, run:

.. code-block:: bash

   > poetry update
   ...
   > source .venv/bin/activate
   (.venv)

Then build the module:
 
.. code-block:: bash
   
   (.venv) > micc-build
   [INFO] [ Building f2py module dotf in directory '/Users/etijskens/software/dev/workspace/ET-dot/et_dot/f2py_dotf/build_'
   ...
   [DEBUG]          >>> shutil.copyfile( 'dotf.cpython-37m-darwin.so', '/Users/etijskens/software/dev/workspace/ET-dot/et_dot/dotf.cpython-37m-darwin.so' )
   [INFO] ] done.
   [INFO] Check /Users/etijskens/software/dev/workspace/ET-dot/micc-build-f2py_dotf.log for details.
   [INFO] Binary extensions built successfully:
   [INFO] - ET-dot/et_dot/dotf.cpython-37m-darwin.so
   >
   
This command produces a lot of output, most of which is rather uninteresting - except in the
case of errors. At the end is a summary of all binary extensions that have been built, or
failed to build. If the source file does not have any syntax errors, you will see a file like
:file:`dotf.cpython-37m-darwin.so` in directory :file:`ET-dot/et_dot`.

.. note:: The extension of the module :file:`dotf.cpython-37m-darwin.so` 
   will depend on the Python version you are using, and on the operating system. 

Here is the test code. Enter it in :file:`ET-dot/tests/test_f2py_dotf.py`:

.. code-block:: python
 
   # import our binary extension
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

   If having to type that much every time, annoys use this trick::

      >>> import et_dot
      >>> f90 = et_dot.my_F90_module
      >>> f90.dot(a,b)
      12.0
      >>> fdot = et_dot.my_F90_module.dot
      >>> fdot(a,b)
      12.0