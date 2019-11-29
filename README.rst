****
Micc
****

.. image:: https://img.shields.io/pypi/v/micc.svg
        :target: https://pypi.python.org/pypi/micc

.. image:: https://img.shields.io/travis/etijskens/micc.svg
        :target: https://travis-ci.org/etijskens/micc

.. image:: https://readthedocs.org/projects/micc/badge/?version=latest
        :target: https://micc.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


`Micc <https://github.com/etijskens/et-micc>`_ is a Python project manager: it helps 
you organize your Python project from simple single file modules to fully fledged 
Python packages containing modules, sub-modules, apps and binary extension modules 
written in Fortran or C++. Micc_ organizes your project in a way that is considered good
practice by a large part of the Python community. 

* Micc_ helps you create new projects. You can start small with a simple one-file 
  package and add material as you go, such as:
  
  * Python **sub-modules** and **sub-packages**,
  * **applications**, also known as command line interfaces (CLIs). 
  * **binary extension modules** written in C++ and Fortran. Boiler plate code is 
    automatically added as to build these binary extension with having to go through
    al the details. This is, in fact, the foremost reason that got me started on this
    project: For *High Performance Python* it is essential to rewrite slow and 
    time consuming parts of a Python script or module in a language that is made 
    for High Performance Computing. As figuring out how that can be done, requires 
    quite some effort, Micc_ was made to automate this part while maintaining the 
    flexibility. 
  * Micc_ adds typically files containing example code to show you how to add your
    own functionality.
    
* Micc_ can automatically **extract documentation** from the doc-strings of your files, 
  and build html documentation that you can consult in your browser, or a .pdf 
  documentation file.
* With a little extra effort the generated html **documentation is automatically published** 
  to `readthedocs <https://readthedocs.org>`_.
* Micc_ helps you with **version management and control**.
* Micc_ helps you with **testing** your code.
* Micc_ helps you with **publishing** your code to e.g. `PyPI <https://pypi.org>`_, so
  that you colleagues can use your code by simply running `pip install your_nifty_package`.
  
For details see the `Micc documentation <https://et-micc.readthedocs.io/en/latest/>`_.

Micc_ does not do all of this by itself. For many things it relies on other strong 
open source tools and it is therefor open source as well (MIT Licence). Here is a list 
of tools micc_ is using or cooperating with happily:

* `poetry <https://github.com/sdispater/poetry>`_: dependency management, virtual 
  environments.
* `pyenv <https://github.com/pyenv/pyenv>`_: management of different Python versions
* `pipx <https://github.com/pipxproject/pipx/>`_: installation of CLIs in a system-wide  
  way.
* `cookiecutter <https://github.com/audreyr/cookiecutter>`_ for creating templates for 
  all the things that can be added to your project.
* `sphinx <http://www.sphinx-doc.org/>`_: building of documentation.
* `git <https://www.git-scm.com/>`_: version control.
* `python-semanticversion <https://github.com/rbarrois/python-semanticversion/blob/master/docs/index.rst>`_:
  management of version string according to version specification `Semver 2.0 <http://semver.org/>`_.
* `pytest <https://www.git-scm.com/>`_: testing your code.
* `click <https://click.palletsprojects.com/en/7.x/>`_: a pythonic and intuitive 
  way of developing CLIs. 
* `F2py <https://docs.scipy.org/doc/numpy/f2py/>`_, which is part of `Numpy <https://numpy.org/>`_, 
  the standard for numerical computing in Python. F2py_ easily transforms modern Fortran
  code into performant binary extension modules.
* `CMake <https://cmake.org>`_ and `pybind11 <https://pybind11.readthedocs.io/en/stable/>`_ as the 
  glue between C++ code and performant binary extension modules.

Roadmap
=======
These features are still on our wishlist:

* Contininous integtration (CI)

