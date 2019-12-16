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
    
* You can automatically **extract documentation** from the doc-strings of your files,
  and build html documentation that you can consult in your browser, or a .pdf 
  documentation file.
* With a little extra effort the generated html **documentation is automatically published** 
  to `readthedocs <https://readthedocs.org>`_.
* Micc_ helps you with **version management and control**.
* Micc_ helps you with **testing** your code.
* Micc_ helps you with **publishing** your code to e.g. `PyPI <https://pypi.org>`_, so
  that you colleagues can use your code by simply running::

    > pip install your_nifty_package

Credits
-------
Micc_ does not do all of this by itself. For many things it relies on other strong 
open source tools and it is therefor open source as well (MIT Licence). Here is a list 
of tools micc_ is using or cooperating with happily:

*   `Pyenv <https://github.com/pyenv/pyenv>`_: management of different Python versions.
*   `Pipx <https://github.com/pipxproject/pipx/>`_ for installation of CLIs in a system-wide
    way.
*   `Poetry <https://github.com/sdispater/poetry>`_ for dependency management, virtual
    environment management, packaging and publishing.
*   `Git <https://www.git-scm.com/>`_ for version control.
*   `CMake <https://cmake.org>`_ is usde for building binary extension modules written
    in C++.

The above tools are not dependencies of Micc_ and must be installed separately. Then
there are a number of python packages on which micc_ depends and which are automatically
installed when poetry_ creates a virtual environment for a project.

*   `Cookiecutter <https://github.com/audreyr/cookiecutter>`_ for creating boilerplate
    code from templates for all the parts that can be added to your project.
*   `Python-semanticversion <https://github.com/rbarrois/python-semanticversion/blob/master/docs/index.rst>`_
    for managing version strings and dependency version constraints according to the
    `Semver 2.0 <http://semver.org/>`_ specification.
*   `Pytest <https://www.git-scm.com/>`_ for testing your code.
*   `Click <https://click.palletsprojects.com/en/7.x/>`_ for a pythonic and intuitive definition
    of command-line interfaces (CLIs).
*   `Sphinx <http://www.sphinx-doc.org/>`_ to extract documentation from your project's
    doc-strings.
*   `Sphinx-click <https://sphinx-click.readthedocs.io/en/latest/>`_ for extracting documentation
    from the click_ command descriptions.
*   `F2py <https://docs.scipy.org/doc/numpy/f2py/>`_ for transforming modern Fortran code into performant
    binary extension modules interfacing nicely with `Numpy <https://numpy.org/>`_.
*   `Pybind11 <https://pybind11.readthedocs.io/en/stable/>`_ as the
    glue between C++ source code and performant binary extension modules, also interfacing nicely with Numpy_.

Roadmap
=======
These features are still on our wish list:

* Deployment on the `VSC <https://www.vscentrum.be>`_ clusters
* Contininous integtration (CI)
* Code style, e.g. `flake8 <http://flake8.pycqa.org/en/latest/>`_ or `black <https://github.com/psf/black>`_
* Profiling

