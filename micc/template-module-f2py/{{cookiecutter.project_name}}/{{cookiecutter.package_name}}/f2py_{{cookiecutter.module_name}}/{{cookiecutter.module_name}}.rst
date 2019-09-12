This file documents a python module built from Fortran code with f2py.
You should document the Python interfaces, *NOT* the Fortran interfaces.

Module {{ cookiecutter.package_name }}.{{ cookiecutter.module_name }}
*********************************************************************

Module {{ cookiecutter.module_name }} built from fortran code in ``f2py_{{ cookiecutter.module_name }}/{{ cookiecutter.module_name }}.f90``.

method {{ cookiecutter.package_name }}.{{ cookiecutter.module_name }}.add(x,y,z)
--------------------------------------------------------------------------------
Computes the sum of Numpy arrays ``x`` and ``y`` and stores the result in ``z``. All three arrays must
have ``dtype=np.float`` and have the same shape.

The result array ``z`` is passed as an argument so that the function is not responsible for
memory management.
