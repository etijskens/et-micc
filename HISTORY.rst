TODO
====

* undo ``micc app ...``?
* undo ``micc module ...``?
* check if project_name exists already on `readthedocs.io`_, and prompt for a 
  different name. (My ``utils`` project works fine, but it was to be expected 
  that the name was already used on `readthedocs.io`_.
* micc feature rename project, in case one forgot to check if that project name 
  does not already exist on `readthedocs.io`_ 
  
* check for overwriting files (we must specify ``overwrite_if_exists`` for 
  cookiecutter because it will already report an error if just the directories
  exist. Adding files to existing directories is not supported out of the box.)
  Maybe, we can monkey patch this problem. We propose that ``micc`` should fail
  when files are overwritten, and that the command be run again with a ``--force``
  option.
      
* add cookiecutter template for C++ modules. We need
   * boost.python (this is compiled and tied to the current Python
     environment
   * Numpy
   * boost.MultiArray (header only)
   * numpy_boost.hpp and numpy_boost_python.hpp 
   * a C++ compiler
   * support for this on on the clusters

* pypi publishing
* virtual environments
* requirements
* tox stuff
* regression tests
*

What are we using poetry for so far?
************************************

(... and do we really need it?)

There is a poetry issue on poetry+anaconda python 
`Any plans to make it work with anaconda python? <https://github.com/sdispater/poetry/issues/190>`_.
Locally, we are completely relying on Anaconda Python. 
Consequentially, I am not completely feeling comfortable with it - but it is
young and very actively developed.

* building wheels (which are used for installing and publishing): 
  ``poetry build``, typically inside the ``Makefile``. However, I haven't
  figured out how to go with e.g. f2py modules and C++ modules. 
  
* ``poetry.console.commands.VersionCommand`` for updating version strings,

* we are not using 
   * ``poetry install`` to create a virtual environment
   * ``poetry run ...`` to run code in that virtual environment
   
* We could use ``poetry install`` to create a virtual environment and 
  point to it in eclipse/pydev so that we will always run our code in that
  environment
* tests should probably be run as::

   > poetry run pytest tests/test*

  
History
=======

* add cookiecutter template for fortran modules with f2py. We need:
   * f2py, comes with Numpy
   * a fortran compiler
   * a C compiler
   * what can be provided out of the box by conda?
   * support for this on on the clusters

I followed this advice: 
`f2py-running-fortran-code-in-python <https://www.scivision.dev/f2py-running-fortran-code-in-python-on-windows/>`_
and installed gcc from homebrew ``brew install gcc``. Inside the Conda 
environment I created soft links to gcc, g++ and gfortran.

There is an issue with Fortran arguments of type real*16, which become 
``long_double`` instead of ``long double`` in the ``<modulename>module.c`` 
wrapper file. The issue is circumvented by editing that file and running 
f2py_local.sh a second time. The issue occurred in gcc 7.4.0, 8.3.0 and 
9.1.0. Switching to gcc provided by XCode does not help either. However, 
adding ``-Dlong_double="long double"`` to the f2py command line options 
solves the problem nicely. :)

I, typically, had different bash scripts for running f2py, one for building 
locally and one for each cluster. It would be nice if a single script would
do and pickup the right compiler from the environment where it is run, as 
well as set the correct compiler options. There may be different f2py modules,
so there will be a different script for every f2py module: ``f2py_<module_name>.sh``.
Preferentially ``<module_name>`` ends with ``f90``. The module name appears 
also inside the script. The script looks for a ifort, and if absent for 
gfortran in the environment. It uses gcc for compiling the C-wrappers and 
for f2py. If one of the components is missing, the script exits with a non-
zero error code and an error message. The makefile can call::

   for s in f2py_*.sh; do ./${s}; done

Do we want a fortran module or not? the fortran module complicates stuff, as
it appears as a namespace inside the python module::

   # a) with a fortran module:
   # import the python module (built from compute_f90_a.f90) which lives
   # in the proj_f2py package: 
   import proj_f2py.compute_f90_a as python_module_a
   # create an alias for the fortran module inside that python module, which
   # is called 'f90_module'. The fortran module  behaves as any other member
   # in the python module.
   f90 = python_module.f90_module
   
   # b) without a fortran module:
   # import the python module (built from compute_f90_b.f90) 
   # this doesn not have a fortran module inside. 
   import proj_f2py.compute_f90_b as python_module_b

v0.5.2 (2019-07-09)
*******************

* add option ``--f2py`` to ``micc module ...``

v0.5.1 (2019-07-09)
*******************

* ``micc create ...`` must write a .gitignore file and other configuration
  files. Addition of modules, apps do not change these.
* Cookiecutter template micc-module-f2py added, no code to use it yet

v0.5.0 (2019-07-04)
*******************

* Fixed poetry issue #1182

v0.4.0 (2019-06-11)
*******************

* First functional working version with
   
  * ``micc create`` 
  * ``micc app``
  * ``micc module``
  * ``micc version``
  * ``micc tag``
  

v0.2.5 (2019-06-11)
*******************

* git support

  * ``git init` in ``micc create``
  * ``micc tag``

v0.2.4 (2019-06-11)
*******************

* Makefile improvements:
  
  * documentation
  * tests
  * install/uninstall
  * install-dev/uninstall-dev

v0.2.3 (2019-06-11)
*******************

* Using pyproject.toml, instead of the flawed setup.py

* Proper local install and uninstall. By Local we mean: not installing from PyPI.
  we had that in et/backbone using pip. But pip uses setup.py which we want to
  avoid. There is not pyproject.toml file sofar... 
  
Moving away from setup.py and going down the pyproject.toml road, we can choose 
between poetry_ and flit_.
  
.. _poetry: https://github.com/sdispater/poetry  
.. _flit: https://github.com/takluyver/flit  

Although, I am having some trouble with reusing some poetry code, i have the
impression that it is better developed, and has a more active community 
(more watchters, downloads, commits, ...)

A pyproject.toml was added (used ``poetry init`` to generate pyproject.toml). 
First issue is how to automatically transfer the version number to our python 
project. `Here <https://github.com/sdispater/poetry/issues/273>`_
is a good post about that. 
  
* using pkg_resources implies a dependence on setuptools = no go
* using tomlkit for reading the pyproject.toml file implies that the 
  pyproject.toml file must be included in the distribution of the 
  package. Since pyproject.toml is complete unnnecessary for the functioning  
  of the module, we'd rather not do that. So, we agree with copying the version
  string from pyproject.toms to the python package (=duplicating). This is 
  basically the same strategy as used by 
  `bumpversion <https://pypi.org/project/bumpversion/>`_.
  
* the command `poetry version ...` allows to modify the version string in 
  pyproject.toml. In principle we can recycle that code. However, we could not 
  get it to work properly (see issue `https://github.com/sdispater/poetry/issues/1182`_).
  This could probably be circumvented by creating my own fork of poetry.
  
  * it is simple to write a hack around this (read the file into a string, 
    replace the version line, and write it back. this preserves the formatting
    but in the unlikely case that there is another version string in some toml table
    it will be incorrect.
  * the `toml package <https://pypi.org/project/toml/>`_ is much simpler than tomlkit, does 
    not cause these problems, but it does not preserve the formatting  of the file.
    
* poetry itself uses a separate __version__.py file in the package, containing 
  nothin but ``__version__ = "M.m.p"``. This is imported in __init__.py as 
  ``from .__version__ import __version__``. This makes transferring the version
  from pyproject.toml to __version__.py easy.
  
Let's first check if we can achieve a proper local install with poetry ...
Install a package::

   > poetry build
   > pip install dist/<package>-<version>-py3-none-any.whl

Uninstall::

   > pip uninstall <package>

This seems to do the trick::

    > pip install -e <project_dir>
    
Install a dev package use cmd::

   > pip install --editable <project_dir>
   
Uninstall::

   > rm -r $(find . -name '*.egg-info')
   
But take care, uninstalling like this::

   > pip uninstall <package>

removed the source files. 
See `this post <https://stackoverflow.com/questions/17346619/how-to-uninstall-editable-packages-with-pip-installed-with-e>`_.


   
v0.1.21 (2019-06-11)
********************

first working version

v0.0.0 (2019-06-06)
*******************

Start of development.

Development plan
----------------

What do we actually need?

* a standardized development environment

   * click : for command line interfaces
   * sphinx : for documentation
   * pytest : for running tests
   * flake8 : for assuring PEP 8 compatibility
   * cookiecutter : if we want sth based on existing templates
   * tox ?
   * poetry?
* a standardized way of creating projects for packages and apps.
* automation of project management tasks, e.g. CI, publishing, ... 
   
This package was inspired by
`Cookiecutter <https://github.com/audreyr/cookiecutter>`_.
 
Inspiration for the project templates came from: 

* `audreyr/cookiecutter-pypackage <https://github.com/audreyr/cookiecutter-pypackage>`_
* `jacebrowning/template-python <https://github.com/jacebrowning/template-python>`_

Interesting posts:

* Here is a particularly readable and concise text about packaging 
  `Current State of Python Packaging - 2019 <https://stefanoborini.com/current-status-of-python-packaging/>`_
  (Pycoder's weekly #372 june 11, by Stefano Borini). The bottom line is: use 
  `poetry <https://poetry.eustace.io>`_. After reading (just part) of the documentation
  I concluded that poetry solves a lot project management issues in an elegant way.
  I am likely to become addicted :).
* version numbers: adhere to `Semantic Versioning <https://semver.org>`_

Think big, start small...
-------------------------
Maybe it is a good idea to get everything going locally + github, and add 
features such as:

* readthedocs,
* publishing to pypi,  
* travis,
* pyup, 
* ..., 

incrementally.
