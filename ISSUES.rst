Open Issues
===========

#1 [bug] FileExistsError in micc module
---------------------------------------
in v0.5.6:

The commands::

    > micc module --f2py <module_name>
    > micc module --cpp <module_name>

generate::

    FileExistsError: [Errno 17] File exists: '<package_name>/tests'

if the flag ``--overwrite`` is not specified. This behavior is incorrect.
Only if existing **files** are overwritten an exception must be raised, not
when a new file is added to an existing directory.

#2 [feature] simple python project
----------------------------------
add ``--simple`` flag to ``micc create`` to create a simple (=unnested) python module ``<package_name>.py``
instead of the nested ``<package_name/>__init__.py``

#3 [feature] add useful example code to templates
-------------------------------------------------
Put more useful example code in

* ``cpp_{{cookiecutter.module_name}}/{{cookiecutter.module_name}}.cpp``
* ``f2py_{{cookiecutter.module_name}}/{{cookiecutter.module_name}}.f90``

as well as in the corresponding test files.

#4 [bug] build commands for f2py and cpp modules
------------------------------------------------
``<package_name>/Makefile`` contains wrong builder for f2py modules and no builder for
cpp modules.

Running CMake build from the command line::

    > cd <package_name>/cpp_<module_name>
    > mkdir build_
    > cd build_
    > cmake CMAKE_BUILD_TYPE=RELEASE ..
    > make

Then, either copy the ``.so`` file to ``<package_name>``, or make a softlink.

#5 [feature] packaging and deployment
-------------------------------------
The `Python Packaging User Guide <https://packaging.python.org/guides/>`_
has a section `Packaging binary extensions <https://packaging.python.org/guides/packaging-binary-extensions/>`_,
with two interesting subsections `Publishing binary extensions <https://packaging.python.org/guides/packaging-binary-extensions/#publishing-binary-extensions>`_ and
`Cross-platform wheel generation with scikit-build <https://packaging.python.org/guides/packaging-binary-extensions/#cross-platform-wheel-generation-with-scikit-build>`_.
Thus, it seems we are  on the right track as scikit-build is based on CMake, which we
are using too for building our f2py and C++ binary modules. Unfortunately, the section `Publishing binary extensions <https://packaging.python.org/guides/packaging-binary-extensions/#publishing-binary-extensions>`_
is broken, as it mentions "For interim guidance on this topic, see the discussion `in this issue <https://github.com/pypa/packaging.python.org/issues/284>`_."
There, two interesting links are found:

* `Building and testing a hybrid Python/C++ package <https://www.benjack.io/2017/06/12/python-cpp-tests.html>`_:
  this is describe a setup.py approach, also based on pybind11 and CMake.
* `cmake-pip <https://distutils-cmake.readthedocs.io/en/latest/>`_: is a simple wrapper around CMake in order to be able
  to have CMake extensions as python modules.

Note that the setup.py approach can become rather convoluted: https://github.com/zeromq/pyzmq/blob/master/setup.py.

The scikit-build approach is further mentioned `here <https://github.com/pypa/packaging.python.org/issues/381>`_.

These approaches request the user that installs your package to also build the binary Python
extensions (f2py, C++), which may be challenging on Windows.

Windows support
+++++++++++++++
The `Python Packaging User Guide`_ suggests `Appveyor <https://www.appveyor.com>`_  , a CI solution,
for providing windows support: https://packaging.python.org/guides/supporting-windows-using-appveyor/.

Poetry?
+++++++
how does poetry deal with binary extensions?

Closed Issues
=============
