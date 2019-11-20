This file documents a python module built from C++ code with pybind11.
You should document the Python interfaces, *NOT* the C++ interfaces.

Module {{ cookiecutter.package_name }}.{{ cookiecutter.module_name }}
*********************************************************************

Module :py:mod:`{{ cookiecutter.module_name }}` built from C++ code in :file:`cpp_{{ cookiecutter.module_name }}/{{ cookiecutter.module_name }}.cpp`.

.. function:: add(x,y,z)
   :module: {{ cookiecutter.package_name }}.{{ cookiecutter.module_name }}
   
   Compute the sum of *x* and *y* and store the result in *z* (overwrite).

   :param x: 1D Numpy array with ``dtype=numpy.float64`` (input)
   :param y: 1D Numpy array with ``dtype=numpy.float64`` (input)
   :param z: 1D Numpy array with ``dtype=numpy.float64`` (output)
   