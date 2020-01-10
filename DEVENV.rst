Principles
----------

.. warning:: `Micc <https://github.com/etijskens/et-micc>`_ was designed for supporting HPC
    developers, and, consequentially, with Linux systems in mind. We provide support for Linux
    (Ubuntu 19.10, CentOS 7.7), and macOS. Due to lack of human resources, it has not been
    tested on Windows, and no support is provided for it.

For Python development, we highly recommend to set up your development environment as described in
`My Python Development Environment <https://jacobian.org/2019/nov/11/python-environment-2020/>`_
by Jacob Kaplan-Moss. We will assume that this is indeed the case for all tutorials here. In
particular:

*   We are using `pyenv <https://github.com/pyenv/pyenv>`_ to manage different Python versions on
    our system (except for Anaconda or Miniconda Python distributions, where the Python version is
    naturally embedded in conda_ virtual environmnent).
*   We use `pipx <https://github.com/pipxproject/pipx/>`_ to install applications which must be
    available system-wide, e.g. micc_, and `CMake <https://cmake.org>`_ system-wide together with their own virtual environment.
*   `Poetry <https://poetry.eustace.io/docs/pyproject/>`_ is used to set up virtual environments for
    the projects we are working, for managing their dependencies and for publishing them.
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

Setting up your Development environment - step by step
------------------------------------------------------
#.  Install pyenv: See
    `Managing Multiple Python Versions With pyenv <https://realpython.com/intro-to-pyenv/>`_
    for common install instructions on macos and Linux.

    If you're on Windows, consider using the fork `pyenv-win <https://github.com/pyenv-win/pyenv-win>`_.
    (Pyenv does not work on windows outside the Windows Subsystem for Linux).

#.  Install your favourite Python versions. E.g.::

        > pyenv install 3.8.0

#.  Install poetry_. The `recommended way <https://python-poetry.org/docs/#installation>`_
    for this is::

    > curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

    This approach will give you one single system-wide Poetry_ installations, which
    will automatically pick up the current Python version as set by pyenv_. Note,
    that as of Poetry_ 1.0.0, Poetry will alse detect
    `conda <https://conda.io/projects/conda/en/latest/index.html>`_ virtual environments.

#. Configure your poetry_ installation::

        > poetry config virtualenvs.in-project true

    This ensures that running ``poetry install`` in a project directory will create a
    project's virtual environment in its own root directory, rather than somewhere in
    the Poetry_ configuration directories, where it is less accessible. If you have
    several Poetry_ installations, they all use the same configuration.

#.  Install pipx_ ::

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

    .. note:: micc_ will be run under the Python version with which pipx_ was installed.

    To upgrade micc_ to the newest version run::

        > pipx upgrade et-micc

#.  To upgrade to a newer version of a tool that you installed with pipx_, use the ``upgrade``
    command::

        > pipx upgrade et-micc
        et-micc is already at latest version 0.10.8 (location: /Users/etijskens/.local/pipx/venvs/et-micc)

#.  If you want to develop binary extensions in  C++ with micc_, make sure CMake and make
    are installed and on your system PATH. You can download CMake_ directly from
    `cmake.org <https://cmake.org/download/>`_.
    Alternatively, CMake is also available as a Python Package which can be installed
    with pipx_::

        > pipx install cmake
        installed package cmake 3.15.3, Python 3.8.0
          These apps are now globally available
            - cmake
            - cpack
            - ctest
        done!

    If you are on one of the VSC clusters, check `Tutorial 7 - Using micc projects on the VSC-clusters`_.

#.  Install an IDE. For many years I have been using `Eclipse IDE for Scientific Computing`_
    with the `PyDev <https://pydev.org>`_ plugin,  but recently I became addicted to
    `PyCharm Community Edition`_. Both are available for MacOS, Linux and Windows.

You should be good to go now.

