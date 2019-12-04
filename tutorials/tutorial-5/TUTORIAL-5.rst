Tutorial 5 - Publishing your code
=================================
Publishing your code is an easy way to make your code available to other users.

5.1 Publishing to the Python Package Index
------------------------------------------
For this we rely on poetry_. If you do not have a PyPI_  account, create one and 
run this command in your project directory, e.g. :file:`et-foo`:

.. code-block::

   > cd path/to/et-foo
   > source .venv/bin/activate
   (.venv) > poetry publish --build
   Building et-foo (0.1.0)
    - Building sdist
    - Built et-foo-0.1.0.tar.gz
   
    - Building wheel
    - Built et_foo-0.1.0-py3-none-any.whl

   Publishing et-foo (0.1.0) to PyPI
   Username: etijskens
   Password:
   
    - Uploading et-foo-0.1.0.tar.gz 100%
    - Uploading et_foo-0.1.0-py3-none-any.whl 100%
    
.. note:: It is crucial that your project name is not already taken. For this reason,
   we recommend that

   #. before you create a project that you might want to publish, you check wether
      your project name is not already taken.
   #. immediately after your project is created, you publish it, as to reserve the
      name forever.

Now everyone can install the package in his current Python environment as::

   > pip install et-foo



5.2 Publishing packages with binary extension modules
-----------------------------------------------------
Packages with binary extension modules are published in exactly the same way, that is,
as a Python-only project. When you ``pip install`` a Micc_ project the package directory
will end up in the :file:`site-packages` directory of the Python environment in which you
install. The source code directories of the binary extensions modules are installed with
the package, but without the binary extensions themselves. These must be compiled locally.
Fortunately that happens automatically, at least if the binary extension were added to
the package by Micc_. When Micc_ adds a binary extension to a project, two thing happen:

* a dependency on micc-build_ is added to the project, and
* in the top-level module :py:mod:`<package_name>/__init__.py` a :py:obj:`try-except`
  block is added that tries to import the binary extension and in case of failure
  (:py:exc:`ModuleNotFoundError`) will attempt to build it using the machinery provided
  by micc-build_. This will usually succeed, provided the necessary compilers are available.

As an example, let us create a project *foo* with a binary extension module *bar* written
in C++

.. code-block:: bash

   > micc -p Foo create
   > cd auto-build
   > micc add bar --cpp

This creates this :file:`Foo/foo/__init__.py`:

.. code-block:: python

   # -*- coding: utf-8 -*-
   """
   Package foo
   ===========

   Top-level package for foo.
   """

   __version__ = 0.0.0

   try:
       import foo.bar
   except ModuleNotFoundError as e:
       # Try to build this binary extension:
       from pathlib import Path
       import click
       from et_micc_build.cli_micc_build import auto_build_binary_extension
       msg = auto_build_binary_extension(Path(__file__).parent, 'bar')
       if not msg:
           import foo.bar
       else:
           click.secho(msg, fg='bright_red')

   def hello(who='world'):
       ...

If the first ``import foo.bar`` fails, the ``except`` block imports the method
:py:meth:`auto_build_binary_extension` and executes it arguments the  path to
the package directory :file`Foo/foo` and the name of the binary extension module
:py:mod:`bar`. If the build succeeds, the :py:obj:`msg` string is empty and
:py:mod:`foo.bar` is imported at last, otherwise the error message :py:obj:`msg`
is printed.


5.3 Providing :py:meth:`auto_build_binary_extension` with custom build parameters
---------------------------------------------------------------------------------

The auto-build above will normally use the default build options, corresponding to `-O3`,
which optimizes for speed. As the :py:meth:`auto_build_binary_extension` method is called
automatically, we have not many options to set build options. The
:py:meth:`auto_build_binary_extension` method will look for the existence of a file
:file:`Foo/foo/cpp_bar/build_options.<platform>.json`, where ``<platform>`` is ``Darwin``,
on MACOSX, ``Linux` on Linux and ``Windows`` on Windows. If it exists, it should contain a
:py:class:`dict` with the build options to use.

.. note:: The build options files are OS specific:

    * On MacOSX  : ``build_options.Darwin.json``
    * On Linux   : ``build_options.Linux.json``
    * On Windows : ``build_options.Windows.json``

5.3.1 f2py module build option specifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
All `options available to the f2py command line application <https://docs.scipy.org/doc/numpy/f2py/usage.html#command-f2py>`_
can be entered in the build file specification. Pure flags, like e.g. ``--noopt``, which are present
or not, but have no value, are entered in the dictionary with value None. Below are some examples of
much used f2py_ flags.

.. code-block:: python

    import json
    from pathlib import Path
    import platform

    f2py = {
        '--f90exec' : 'f90 compiler executable'
        '--f90flags': 'f90 compiler flags'
        '--opt'     : 'f90 compiler optimization flags'
        '--arch'    : 'f90 compiler architecture specific compiler flags'
        '--noopt'   : None # neglect '--opt' contents
        '--noarch'  : None # neglect '--arch' contents
        '--debug'   : None # compile with debugging information
    }
    module_srcdir_path = Path(project_path) / package_name / f"f2py_{module_name}"
    with (module_srcdir_path / f"build_options.{platform.system()}.json").open('w) as f:
        json.dump(f2py, f)

.. note:: The Python dictionary ``f2py`` is written to file in ``.json``format, which is
   human readable. You can also construct it with an editor.

5.3.2 cpp module build option specifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For cpp binary extension modules the build tool is CMake_. Here, the entries of the build
options dict consist of any CMake_ variable and its desired value.

.. code-block:: python

    import json
    from pathlib import Path
    import platform

    cmake = {
        'CMAKE_BUILD_TYPE' : 'RELEASE',
        ...
    }
    module_srcdir_path = Path(project_path) / package_name / f"cpp_{module_name}"
    with (module_srcdir_path / f"build_options.{platform.system()}.json").open('w) as f:
        json.dump(cmake, f)
