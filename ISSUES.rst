Open Issues
===========
#25

#24 [feature] add indentation to logging
----------------------------------------

.. code-block:: bash

   > micc -p foo create
   
   [INFO] Creating project (foo):
          Python package (foo): structure = (foo/foo/__init__.py)
   [INFO] Creating git repository
   [INFO] ... done.
   
   [INFO] ... done.

should look like:


.. code-block:: bash

   > micc -p foo create
   
   [INFO] Creating project (foo):
          Python package (foo): structure = (foo/foo/__init__.py)
          ...
   [INFO]     Creating git repository 
              ...
   [INFO]     done.
   [INFO] done.
   
#22 [issue] building cpp module fails when pybind11 is pip-installed
--------------------------------------------------------------------
(at least on a conda environment) it works however when it is conda-installed.

.. code-block:: bash

   DEBUG    micc-build-cpp_mod4.log:utils.py:295  (stderr)
                                                 CMake Error at CMakeLists.txt:14 (find_package):
                                                   Could not find a package configuration file provided by "pybind11" with any
                                                   of the following names:
   
                                                     pybind11Config.cmake
                                                     pybind11-config.cmake
   
                                                   Add the installation prefix of "pybind11" to CMAKE_PREFIX_PATH or set
                                                   "pybind11_DIR" to a directory containing one of the above files.  If
                                                   "pybind11" provides a separate development package or SDK, be sure it has
                                                   been installed.

also building an f2py module fails for the same reason.
conda installs the missing files in ``~/miniconda3/envs/micc/share/cmake/pybind11``

#5 [feature] packaging and deployment, and the use of poetry in general
-----------------------------------------------------------------------
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

The `scikit-build approach <https://github.com/pypa/packaging.python.org/issues/381>`_ is mentioned .

These approaches request the user that installs your package to also build the binary Python
extensions (f2py, C++), which may be challenging on Windows.

Windows support
+++++++++++++++
The `Python Packaging User Guide`_ suggests `Appveyor <https://www.appveyor.com>`_  , a CI solution,
for providing windows support: https://packaging.python.org/guides/supporting-windows-using-appveyor/.

Poetry?
+++++++
how does poetry deal with binary extensions?

issue #8 cookiecutter.json files
--------------------------------
These files are written in the template directories of the micc installation. If micc happens to be 
installed in a location where the user has no write access, micc will not work.

Closed Issues
=============
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

#3 [feature] add useful example code to templates
-------------------------------------------------
Put more useful example code in

* ``cpp_{{cookiecutter.module_name}}/{{cookiecutter.module_name}}.cpp`` -> added in  v0.5.7.
* ``f2py_{{cookiecutter.module_name}}/{{cookiecutter.module_name}}.f90``

as well as in the corresponding test files.

v0.5.10

#4 [bug] build commands for f2py and cpp modules
------------------------------------------------
``<package_name>/Makefile`` contains wrong builder for f2py modules and no builder for
cpp modules.

Running CMake build from the ccd ..ommand line::

    > cd <package_name>/cpp_<module_name>
    > mkdir build_
    > cd build_
    > cmake CMAKE_BUILD_TYPE=RELEASE ..
    > make

Then, either copy the ``.so`` file to ``<package_name>``, or make a softlink.
A *simple package* (feature #2) should have simple documentation, and complete documentation when
converted to a full blown package.

feature #11 add log files to ``micc build``
-------------------------------------------
controlling the output with verbose is not sufficient. If one of the build commands fails we want
to print all output for building that module. that's hard to control with verbose.

issue #9 prohibit creation of a micc project under another project
------------------------------------------------------------------
This implies asserting that none of the parent directories of the output directory
is a project directory (in ``micc_create_simple`` and ``micc_create_general``

issue #7 cookiecutter.json files are temporary
----------------------------------------------
While workin on issue #2 I realized that these are in fact temporary files, which do neither belong 
in the template directories (although cookiecutter requires them). It is better to remove these files 
when cookiecutter is done. 

v0.5.11

#2 [feature] simple python project
----------------------------------
add ``--simple`` flag to ``micc create`` to create a simple (=unnested) python module ``<package_name>.py``
instead of the nested ``<package_name/>__init__.py``
a *simple* package should be convertible to a normal package

v0.5.13

issue #12 common items in micc.json files
-----------------------------------------
While workin on issue #2 I realized that there are now several ``micc.json` files with common
items which are in fact copies. we need either a single ``micc.json`` or a way of isolating
the common parts in a single file.
Fixed by itself. If there are multiple templates, every new template adds parameters to the original.

#13 [feature] os.path -> pathlib
--------------------------------
more obvious manipulation of file paths

#14 [feature] add flag for nesting a project inside another project
-------------------------------------------------------------------
mainly for running tests.

#6 [feature] decomposition
--------------------------
maybe it is usefull to limit the number of files in the cookiecutter_ templates. For now even the
simples project contains 11 ``.rst`` files. For a beginner that may be too much to grasp. Maybe it is ]
usefull to start with a ``README.rst`` only and have a ``micc doc [options]`` command that adds documentation
topics one at a time::

    > micc doc --authors
    > micc doc --changelog|-c # or
    > micc doc --history|-h
    > micc doc --api|-a
    > micc doc --installation|-i

this is perhaps useful, but rather more complicated. E.g if we first create a package with several
modules (python, f2py, cpp) and then start to add documentation. This is a more complicated situation
and one in which errors will be easily made, and more difficult to maintain.

issue #10 micc files are part of the template
---------------------------------------------
So they better live there.

v0.6.2

#16 [issue] poetry 1.0.0b1 uses different cleo than 0.12.17
-----------------------------------------------------------
this break our code for retrieving the current version number.

#15 [issue] using poetry bumping the version in pyproject.toml
--------------------------------------------------------------
currently we do this by using poetry's source code (import). As poetry recommends a singly 
installation of poetry system-wide, this adds an extra dependency (i.e. poetry itself) on
top of the single installation. There is no way of guaranteeing that both versions are the 
same. Ideally, we would rely on only the system version of poetry.

#19 [issue] avoiding poetry
---------------------------
Poetry is currently used for bumping versions only. As poetry does not play well with conda,
(see issue #18) relying on poetry (and therefore adding it as a dependency of micc) is a ticking time bomb 
because when poetry is there users will use it, even if it is documented that it does not work.
So i propose to use bump(2)version for bumping versions by default. This will always work well 
with Anaconda Python versions.

interesting links:

* https://github.com/peritus/bumpversion
* https://github.com/c4urself/bump2version
* https://blog.developer.atlassian.com/bumpversion-is-automation-for-semantic-versioning

#21 [issue] micc create
-----------------------
raises exception (cannot create project inside another project) when run from a project
directory with a relative path. E.g.::

    ~/path/to/micc/ > micc create 
   
fails when given the path ../foo although this would be created in ``~/path/to/soep``.

#20 [issue] install dependencies in current conda environment
-------------------------------------------------------------
As poetry build works, and pip install dist/<wheel> too, even in a conda python
environment, this is no longer an issue,.

#18 [issue] two tools for reading/writing toml files
----------------------------------------------------
Currently, we are using both tomlkit and toml for reading and writing toml files.
Better stick to one.

#17 [issue] poetry 1.0.0b1 does not play well with conda
--------------------------------------------------------
Poetry made me a virtual environment for micc, based on ``miniconda3``'s active python version
(which was 3.7.3). However, it did not pickup the correct python standard library (used 3.6.whatever
instead), obviously a nightmare. Thus, if we want to use poetry, we must use a non-conda Python, or
if we want to use conda python versions, we must refrain from poetry.
solved: only ``poetry install`` does not work well with a conda python environment,
``poetry build`` does fine 

#23 [issue] remove interactivity from micc app and micc module
--------------------------------------------------------------
behavior is now steered with flags. 
default behavior is abort if pre-existing files would be overwritten.

