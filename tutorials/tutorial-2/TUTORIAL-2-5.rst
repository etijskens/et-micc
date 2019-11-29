2.5 Documenting binary extension modules
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
* :file:`ET-dot/et_dot/cpp_dotc/dotc.cpp`

Here are the contents, respectively:

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
      
Note that the documentation must be entirely in :file:`.rst` format.

This is what the result looks like (html):

.. image:: ../tutorials/tutorial-2/img3.png