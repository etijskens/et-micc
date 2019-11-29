Tutorial 2: Binary extensions
=============================

Binary extensions are 

Suppose for a moment that Numpy_ did not have a dot product implementation and that 
the implementation provided in Tutorial-1 is way too slow to be practical for your
research project. For the reasons mention you would have to provide your own low-level 
implementation yourself in Fortran, C or C++. Such modules are called *binary extensions*.
Micc_ can assist you with building binary extensions and gives you the option to choose 
between Fortran and C++. As C is approximately a subset of C++ there is little reason to 
provide support for both C++ and C.

2.1 Binary extensions in Micc_ projects
---------------------------------------
Micc_ provides boilerplate code for binary extensions as well as some practical wrappers
around top-notch tools for building binary extensions from Fortran and C++. Fortran code 
is compiled into a Python module using `f2py <https://docs.scipy.org/doc/numpy/f2py/>`_ 
(which comes with Numpy_). For C++ we use Pybind11_ and CMake_.

2.1.1 Choosing between Fortran and C++ for binary extension modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Here are a number of arguments that you may wish to take into account for choosing the
programming language for your binary extension modules:  

* Fortran is a simpler languages than C++
* It is easier to write efficient code in Fortran than C++
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
 
2.1.2 Converting a module structure to a package structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Module structure projects are meant for small projects consisting of a single
module file, here :file:`et_dot.py` in the project directory. For more involved 
projects a package structure is more appropriate. Package structure projects can 
contain additional python modules, binary extension modules written in Fortran 
or C++, as well as command line interfaces (CLIs). In a package structure, 
the project directory has a subdirectory with the package name, c.q. :file:`et_dot`,
that contains an :file:`__init__.py` file, which has the same content as the 
:file:`et_dot.py` file in the module structure.
  
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
:file:`ET-dot/docs/index.rst`, which we do not allow, because the user may have 
modified that file (although the files :file:`ET-dot/docs` directory are in fact not 
meant for being edited by the user). If he has not edited :file:`ET-dot/docs/index.rst` the user 
can safely rerun the command with the ``--overwrite`` flag. Otherwise he must use the
``--backup`` flag to keep a backup of the original :file:`ET-dot/docs/index.rst`. That
way he can inspect the original file and transfer his changes to the new file.

.. code-block:: bash
   
   > micc convert-to-package --overwrite
   Converting simple Python project ET-dot to general Python project.
   [WARNING]        '--overwrite' specified: pre-existing files in /Users/etijskens/software/dev/workspace will be overwritten WITHOUT backup:
   [WARNING]        overwriting /Users/etijskens/software/dev/workspace/ET-dot/docs/index.rst
   
 