TODO
====
.. _readthedocs: https://readthedocs.org/
.. _poetry: https://poetry.eustace.io/
.. _PyPI: https://pypi.org/
.. _micc: https://micc.readthedocs.io/en/master/

* check for a the presence of a global CMake or add it as a dev dependency
  in pyproject.toml.

* update tutorial 7
* move ``LINKS.rst`` to a separate git repo (it changes too often)
* add a remove command for removing a component of a micc_ project
  see https://github.com/etijskens/et-micc/issues/32
* add a rename command for renaming a component of a micc_ project or the project itself.
  see https://github.com/etijskens/et-micc/issues/29

* Put makefile targets into micc commands and remove micc/makefile? This
  makes a more uniform interface. Use subprocess or lrcmd for this?

* Fortran compiler options (while using f2py): is ``-O3`` enough?
* allow for multiple Fortran/C++ source files?
* how to add external projects for f2py and C++ modules (include files,
  libraries)?

    * this was fixed for C++ by using the CMake framework

* check `cppimport <https://github.com/tbenthompson/cppimport>`_
* undo ``micc app ...``?
* undo ``micc module ...``?

* check if project_name exists already on `readthedocs`_ or `pypi`_. If not
  abort and print a message that suggests to use a different name, or to create
  the project anyway by using ``--force``.

* remove dependency on `toml <https://pypi.org/project/toml/>`_ in favor of
  `tomlkit <https://pypi.org/project/tomlkit/>`_ which comes with poetry.
  (now that we are fixed poetry issue #1182)

* regression tests
* Reflect about "do we really need poetry? (see below)

Poetry considerations
------------------------
* What are we using `poetry`_ for?
* Do we really need it?
* Maybe we should wait a bit for poetry to mature, before we start building our
  micc project around it.
* Maybe we should decouple micc and `poetry`_?
* Maybe we should still use ``setup.py`` rather than `poetry`_ because it is
  well established?

There is a poetry issue on poetry+anaconda python 
`Any plans to make it work with anaconda python? <https://github.com/sdispater/poetry/issues/190>`_.
Locally, we are completely relying on Anaconda Python. 
Consequentially, I am not completely feeling comfortable with `poetry`_` - but it is
very actively developed.

Anaconda Python used to be very convenient, but maybe the standard python+pip+virtualenv is good
enough today? One advantage anaconda python still has is that its numpy
well aligned numpy arrays which is in favor of vectorization.

So far we use `poetry`_ for:

* **building wheels** (which are used for installing and publishing):
  ``poetry build``, typically inside the ``Makefile``. However, I haven't
  figured out how to go with e.g. f2py modules and C++ modules. 
  
* ``poetry.console.commands.VersionCommand`` for **updating version strings**

* we are not using 
   * ``poetry install`` to create a virtual environment
   * ``poetry run ...`` to run code in that virtual environment
   
* We could use ``poetry install`` to create a virtual environment and 
  point to it in eclipse/pydev so that we will always run our code in that
  environment
* tests should probably be run as::

   > poetry run pytest tests/test*

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
  `poetry`_. After reading (just part) of the documentation
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

