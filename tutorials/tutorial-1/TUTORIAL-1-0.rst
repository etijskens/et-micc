
Tutorial 1: a simple project
============================


1.0 Setting up your Development environment
-------------------------------------------

.. warning:: `Micc <https://github.com/etijskens/et-micc>`_ was designed for supporting HPC developers,
    and, consequentially, with Linux systems in mind. We provide support for Linux (Ubuntu 19.10,
    CentOS 7.7), and macOS. Due to lack of human resources, Windows is currently not supported.

For Python development, we highly recommend to set up your development environment as described in 
`My Python Development Environment <https://jacobian.org/2019/nov/11/python-environment-2020/>`_
by Jacob Kaplan-Moss. We will assume that this is indeed the case for all tutorials here. In 
particular:

*   We are using `pyenv <https://github.com/pyenv/pyenv>`_ to manage different Python versions on
    our system.
*   We use `pipx <https://github.com/pipxproject/pipx/>`_ to install applications like Micc_ and
    `CMake <https://cmake.org>`_ system-wide together with their own virtual environment.

  .. note:: Ideally, also Poetry_ would be pipx installed, but this approach seems to make the
     command ``poetry install`` ignore the Python version that is set by pyenv_. Instead, it uses
     the Python version with which poetry was installed (that is the one of pipx). A workaround is
     given below `1.0.1 Pyenv workaround for Poetry`_

*   `Poetry <https://poetry.eustace.io/docs/pyproject/>`_ is used to set up virtual environments for
    the projects we are working, for managing their dependencies and for publishing them to PyPI_.
*   Micc_ is used to set up the project structure, as the basis of everything that will be described
    in the tutorials below.

*   For Micc_ projects with binary extension the necessary compilers must be installed on the system.

*   As an IDE for Python/Fortran/C++ development we recommend:

    *   `Eclipse IDE for Scientific Computing <https://www.eclipse.org/downloads/packages/release/photon/rc2/eclipse-ide-scientific-computing>`_
        with the `PyDev <https://pydev.org>`_ plugin. This is an old time favorite of mine, although
        The learning curve is a bit steep and documentation could be better. Today, PyDev_ is beginning
        to lag behind for Python, but Eclipse is still very good for Fortran and C++.

    *   `PyCharm Community Edition <https://www.jetbrains.com/pycharm/download>`_. I only tried this one
        recently and was very soon convinced for python development. (Didn't go back to Eclipse once since
        then). I currently have insufficient experience for Fortran and C++ for making recommendations.

1.0.1 Pyenv workaround for Poetry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Poetry_ is a recent tool which is still undergoing a lot of changes. One of the areas where
it is still a bit rough around the edges is its treatment of pyenv_ and pyenv-virtualenv.
At the time of writing, poetry install does not seem to respect the settings of ``pyenv local``
and ``pyenv global`` when poetry_ is ``pipx installed``. Fortunately, there is a workaround.
probably change in the future as poetry_ matures.
   
The workaround requires installing poetry in every pyenv_ Python version. E.g. suppose we want to
develop projects for Python 3.6.9, 3,7.5 and 3.8.0.
   
.. code-block:: bash

   > pyenv install 3.6.9
   ...                    # all dependencies are installed
   > pyenv local 3.6.9
   > pip install poetry==1.0.0b8
   >
   > pyenv install 3.7.5
   ...                    # all dependencies are installed
   > pyenv local 3.7.5
   > pip install poetry==1.0.0b8
   >
   > pyenv install 3.8.0
   ...                    # all dependencies are installed
   > pyenv local 3.8.0
   > pip install poetry==1.0.0b8

This installs poetry_ 1.0.0b8 (which is a development version) in all three Python versions.

To use set up project *foo* for Python 3.8.0, we would go like this:
   
.. code-block:: bash

   > micc -p path/to/foo create
   > cd path/to/foo
   > pyenv local 3.8.0    # make python 3.8.0 the default python for this project directory
   > poetry install
   ...                    # all dependencies are installed
   > source .venv/bin/activate
   (.venv) > python --version
   Python 3.8.0

The last command verifies that project *foo*'s virtual environment is indeed based on Python 3.8.0.

If, for some reason or another, we decide later that we need 3.7.9, rather than 3.8.0, we must:

* deactivate the virtual environment,
* delete it,
* delete poetry.lock,
* repeat the above procedure, this time for python 3.7.9.

Here is how it goes:

.. code-block:: bash

   (.venv) > dectivate
   > rm -rf .venv
   > rm poetry.lock
   > pyenv local 3.7.9
   > which python
   /Users/etijskens/.pyenv/shims/python
   > python --version
   Python 3.7.9
   > poetry install
   ...                    # all dependencies are installed
   > source .venv/bin/activate
   (.venv) > python --version
   Python 3.7.9
   (.venv) > which python
   /path/to/foo/.venv/bin/python

1.0.2 Setting up your Development environment - step by step
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#.  Install pyenv: See
    `Managing Multiple Python Versions With pyenv <https://realpython.com/intro-to-pyenv/>`_
    for common install instructions on macos and Linux.

#.  Install your favourite Python versions. E.g.::

        > pyenv install 3.8.0

#.  Install poetry in **all** your Python versions::

        > pyenv local 3.8.0
        > pip install poetry==1.0.0b8

    (Use the most recent poetry_ version). When done, unset the local pyenv_ version::

        > pyenv local --unset

#. Configure poetry_ ::

        > poetry config virtualenvs.in-project true

    This ensures that running ``poetry install`` in a project directory will create a
    project's virtual environment in its own root directory, rather than somewhere in
    the Poetry_ configuration directories, where it is less accessible.

#.  Install pipx::

        > python -m pip install --user pipx
        > python -m pipx ensurepath

    .. note:: This will use the Python version returned by ``pyenv version``. Micc_ is
        certainly comfortable with Python 3.7 and 3.8.

#.  Install micc_ with pipx::

        > pipx install et-micc
          installed package et-micc 0.10.8, Python 3.8.0
          These apps are now globally available
            - micc
        done!

    .. note:: This will use the Python version with which.

#.  If you want to develop binary extensions in  C++ with micc_, make sure CMake and make is installed
    and accessible on your system. You can download it directly from `cmake.org <https://cmake.org/download/>`_.
    Alternatively, CMake is also available as a Python Package which can be pipx installed::

        > pipx install cmake
        installed package cmake 3.15.3, Python 3.8.0
          These apps are now globally available
            - cmake
            - cpack
            - ctest
        done!

#.  To if you want to move on to a newer version of a tool that you installed with pipx_, use the ``upgrade``
    command, e.g.::

        > pipx upgrade et-micc
        et-micc is already at latest version 0.10.8 (location: /Users/etijskens/.local/pipx/venvs/et-micc)

You should be good to go now.

