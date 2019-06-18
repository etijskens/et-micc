History
=======



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
