History
=======

Current issues
**************

* Using pyproject.toml instead of the flawed setup.py

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
This seems to do the trick::

    > pip install -e <project_dir>
    
But take care, **uninstalling removes the source files**? 
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
