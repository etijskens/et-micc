Converting a module structure to a package structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Module structure projects are meant for small projects consisting of a single
module files in the project directory. For more involved projects a package 
structure is more appropriate. Package structure projects can contain additional
python modules, binary extension modules based on Fortran and C++, as well as
command line interfaces (CLIs).
  
Since we started out with a module project ET-dot, its module structure 
(:file:`ET-dot/et_dot.py`) must be converted to a package structure 
(:file:`ET-dot/et_dot/__init__.py`) before we can add a f2py (Fortran) binary
extension module to it.

.. code-block:: bash
   
   > micc convert-to-package
   Converting simple Python project ET-dot to general Python project.
   [WARNING]        Pre-existing files in /Users/etijskens/software/dev/workspace that would be overwrtitten:
   [WARNING]          /Users/etijskens/software/dev/workspace/ET-dot/docs/index.rst
      Aborting because 'overwrite==False'.
        Rerun the command with the '--backup' flag to first backup these files (*.bak).
        Rerun the command with the '--overwrite' flag to overwrite these files without backup.
      Aborting.
   [CRITICAL]       Exiting (-3) ...
   [WARNING]        It is normally ok to overwrite 'index.rst' as you are not supposed
                    to edit the '.rst' files in '/Users/etijskens/software/dev/workspace/ET-dot/docs.'
                    If in doubt: rerun the command with the '--backup' flag,
                      otherwise: rerun the command with the '--overwrite' flag,     
                      
Without extra options the command fails because it wants to replace the file 
:file:`ET-dot/docs/index.rst`. Although the :file:`ET-dot/docs/index.rst` directory 
is in fact not meant for being edited by the user, the user may choose to do so and 
thus the user is warned. If he has not edited :file:`ET-dot/docs/index.rst` the user 
can safely rerun the command with the ``--overwrite`` flag. Otherwise he must use the
``--backup`` flag to keep a backup of the original :file:`ET-dot/docs/index.rst`.

.. code-block:: bash
   
   > micc convert-to-package --overwrite
   Converting simple Python project ET-dot to general Python project.
   [WARNING]        '--overwrite' specified: pre-existing files in /Users/etijskens/software/dev/workspace will be overwritten WITHOUT backup:
   [WARNING]        overwriting /Users/etijskens/software/dev/workspace/ET-dot/docs/index.rst
   
Building binary extensions from Fortran
---------------------------------------
Binary extension modules based on Fortran are called *f2py modules* because these 
modules are build with the f2py tool, which is part of Numpy. Since our project 
ET-dot now has a package structure, we are now ready to add a f2py module. Let us 
call this module :py:mod:`dotf`, where the ``f`` stands for Fortran:

.. code-block:: bash
   
   > micc module dotf --f2py
   [INFO]           [ Creating f2py module dotf in Python package ET-dot.
   [INFO]               - Fortran source in       ET-dot/et_dot/f2py_dotf/dotf.f90.
   [INFO]               - Python test code in     ET-dot/tests/test_f2py_dotf.py.
   [INFO]               - module documentation in ET-dot/et_dot/f2py_dotf/dotf.rst (in restructuredText format).
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
 
 Build the module:
 
.. code-block:: bash
   
   > micc build
   [INFO] [ Building f2py module dotf in directory '/Users/etijskens/software/dev/workspace/ET-dot/et_dot/f2py_dotf/build_'
   ...
   [DEBUG]          >>> shutil.copyfile( 'dotf.cpython-37m-darwin.so', '/Users/etijskens/software/dev/workspace/ET-dot/et_dot/dotf.cpython-37m-darwin.so' )
   [INFO] ] done.
   [INFO] Check /Users/etijskens/software/dev/workspace/ET-dot/micc-build-f2py_dotf.log for details.
   >
   
This command produces a lot of output, most of which is rather uninteresting - except in the
case of errors. If the source file does not have any syntax errors, you will see a file like 
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
at the output of ``micc build``, you will see information about the wrappers that f2py 
constructs. 

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

