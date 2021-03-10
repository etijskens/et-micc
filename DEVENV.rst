.. _pip: https://pypi.org/project/pip/


Principles
----------

This document aims at setting up a practical development environment for Python projects,
allowing the integration of binary extension modules based on C++ or Fortran.
Developing on a local machine, a desktop or a laptop, is often somewhat more practical than
developing on the cluster. Typically, I start developing on my own machine until things are
working well, and then I port the code to the cluster for further testing. I switch back and
forth between both environments several times.

There are important differences in managing your environment on your local machine and on the
cluster. They are described in detail in :ref:`tutorial-6`.

.. warning:: `Micc <https://github.com/etijskens/et-micc>`_ was designed for supporting HPC
    developers, and, consequentially, with Linux systems in mind. We provide support for Linux
    (Ubuntu 19.10, CentOS 7.7), and macOS. Due to lack of human resources, it has not been
    tested on Windows, and no support is provided for it. However,
    `WSL-2 <https://pbpython.com/wsl-python.html>`_ may do the trick on Windows. Any feedback
    is welcome

If you want to experiment with micc without having to setup the environment, You can download
anb Ubuntu 20.10 virtual machine for VirtualBox with everything pre-installed at
https://calcua.uantwerpen.be/courses/parallel-programming/ubuntu-20.10.ova. It has a userid
``user`` with password ``calcua@ua``.

For Python development on your local machine, we highly recommend to set up your development
environment as described in
`My Python Development Environment <https://jacobian.org/2019/nov/11/python-environment-2020/>`_
by Jacob Kaplan-Moss. We will assume that this is indeed the case for all tutorials here. In
particular:

*   We use `pyenv <https://github.com/pyenv/pyenv>`_ to manage different Python versions on
    our system.
*   `Pipx <https://github.com/pipxproject/pipx/>`_ is used to install Python applications
    system-wide. If your projects depend on different Python versions it is a good idea to
    ``pipx install`` Micc_, which we use for project management and and building binary extension
    modules.
*   `Poetry <https://poetry.eustace.io/docs/pyproject/>`_ is used to set up virtual environments for
    the projects we are working, for managing their dependencies and for publishing them.
*   For building binary extension modules from C++ `CMake <https://cmake.org>`_ must be available.
*   For Micc_ projects with binary extension the necessary compilers (C++, Fortran) must be installed
    on the system.
*   As an IDE for Python/Fortran/C++ development we recommend:

    *   `Eclipse IDE for Scientific Computing <https://www.eclipse.org/downloads/packages/release/photon/rc2/eclipse-ide-scientific-computing>`_
        with the `PyDev <https://pydev.org>`_ plugin. This is an old time favorite of mine, although
        The learning curve is a bit steep and documentation could be better. Today, PyDev_ is beginning
        to lag behind for Python, but Eclipse is still very good for Fortran and C++.

    *   `PyCharm Community Edition <https://www.jetbrains.com/pycharm/download>`_. I only tried this one
        recently and was very soon convinced for python development. (Didn't go back to Eclipse once since
        then). I currently have insufficient experience for Fortran and C++ for making recommendations.

Setting up your local Development environment - step by step
------------------------------------------------------------

.. note::

   The steps below are only suitable on your local laptop or desktop. For working on the VSC
   clusters, a separate tutorial is provided (:ref:`tutorial-6`).

#.  Install pyenv: See
    `Managing Multiple Python Versions With pyenv <https://realpython.com/intro-to-pyenv/>`_
    for common install instructions on macos and Linux.

    .. note::
        Since Ubunty 20.10 the dependencies for pyenv_ can best be installed as shown in
        https://github.com/asdf-vm/asdf/issues/570 . The realpython page above is not up
        to date.

    If you're on Windows, consider using the fork `pyenv-win <https://github.com/pyenv-win/pyenv-win>`_.
    (Pyenv does not work on windows outside the Windows Subsystem for Linux).

#.  Install your favourite Python versions. E.g.::

        > pyenv install 3.8.0

#.  Install poetry_. The `recommended way <https://python-poetry.org/docs/#installation>`_
    for this is::

    > curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

    This approach will give you one single system-wide Poetry_ installation, which
    will automatically pick up the current Python version in your environment. Note,
    that as of Poetry_ 1.0.0, Poetry will also detect
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

#.  If you want to develop binary extensions in Fortran or C++, you will need a Fortran compiler or a C++
    compiler, respectively. For C++ binary extensions, also CMake and make must be on your system PATH.
    You can download CMake_ directly from `cmake.org <https://cmake.org/download/>`_.

    If you are on one of the VSC clusters, check "Tutorial 7 - Using micc projects on the VSC clusters".

#.  Install an IDE. For many years I have been using `Eclipse IDE for Scientific Computing`_
    with the `PyDev <https://pydev.org>`_ plugin,  but recently I became addicted to
    `PyCharm Community Edition`_. Both are available for MacOS, Linux and Windows.

#.  Create a git account at https://github.com>/join/. Also
    `create a personal access token <https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token>`_
    At point 7 check at least these boxes:

        * repo
        * read:org

    At point 9 copy the toke to the clipboard and paste it in :file:`~/.pat.txt`::

        > echo shift+ctrl+V > ~/.pat.txt

    Micc_ uses this file to automatically create a GitHub repo for your micc_ projects.

#.  Install ``git`` (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and
    the github cli ``gh`` (https://github.com/cli/cli#installation).

#.  Create your first micc_ project. The very first time, you will be asked to set some default
    values that identify you as a micc_ user. Replace the preset values by your own preferences::

        > micc -p my-first-micc-project create
        your full name [Engelbert Tijskens]: carl morck
        your e-mail address [engelbert.tijskens@uantwerpen.be]: carl.mork@q-series.dk
        your github username (leave empty if you do not have) [etijskens]: cmorck
        the initial version number of a new project [0.0.0]:
        default git branch [master]:

    The last two entries are generally ok. If you later want to change the entries, you can simply
    edit the file :file:`~/.et_micc/micc.json`.

You should be good to go now.

Setting up your cluster Development environment - step by step
--------------------------------------------------------------
For details see :ref:`Tutorial-6`

#.  On the cluster you must select the software packages you want to use manually by
    loading modules with the `module system <https://vlaams-supercomputing-centrum-vscdocumentation.readthedocs-hosted.com/en/latest/software/software_stack.html>`_
    The module system provides access to the many pre-installed software packages - including Python
    versions - that are especially built for HPC purposes and optimal performance. They are generally,
    much more performant than if you would have built them yourself. It is, therefor, discouraged to
    install pipx_ to your own Python versions.

#.  Install poetry_. The `recommended way <https://python-poetry.org/docs/#installation>`_
    for this is::

    > curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | /usr/bin/python

    (Make sure to use the system Python  ``/usr/bin/python`` for this. Otherwise you will run into
    trouble selecting a Python version for your project.)
    This approach will give you one single system-wide Poetry_ installation, which
    will automatically pick up the current Python version in your environment.

#. Configure your poetry_ installation::

        > poetry config virtualenvs.in-project true

    This ensures that running ``poetry install`` in a project directory will create a
    project's virtual environment in its own root directory, rather than somewhere in
    the Poetry_ configuration directories, where it is less accessible.

#.  For micc_ projects that are cloned from a git repository, we recommend install micc_ as a
    development dependency of your project::

        > cd path/to/myproject
        > poetry add --dev

    If you want to create a new project with micc_, you must install it first of course::

        > module load Python         # load your favourite Python module
        > pip install --user et-micc

    Without the ``--user`` flag pip_ would try to install in the cluster module, where you
    to not have access. The flag instructs pip_ to install in your home directory.

#.  If you want to develop binary extensions in Fortran or C++, you will need a Fortran compiler
    and/or a C++ compiler, respectively. In general, loading a Python module on the cluster,
    automatically also makes the compilers available that were used to compile the Python version.

    For C++ binary extensions, also CMake_ must be on your system PATH::

        > module load CMake

#.  If you need a full IDE, you must use one of the graphical environments on the cluster
    (see https://vlaams-supercomputing-centrum-vscdocumentation.readthedocs-hosted.com/en/latest/access/access_and_data_transfer.html#gui-applications-on-the-clusters)
    Unfortunately, there are different gui environments for the different VSC clusters.
    If you only want a graphical editor, you can use Eclipse Remote system explorer as a
    remote editor.

#.  Get a git account at `github <https://github.com>`_, install git if is is not pre-installed
    on your system, and configure it::

        > module load git                                   # for a more recent git version
        > git config --global user.email "you@example.com"
        > git config --global user.name "Your Name"

#.  Create your first micc_ project. The very first time, y ou will be asked to set some default
    values that identify you as a micc_ user. Replace the preset values by your own preferences::

        > micc -p my-first-micc-project create
        your full name [Engelbert Tijskens]: carl morck
        your e-mail address [engelbert.tijskens@uantwerpen.be]: carl.mork@q-series.dk
        your github username (leave empty if you do not have) [etijskens]: cmorck
        the initial version number of a new project [0.0.0]:
        default git branch [master]:

    The last two entries are generally ok. If you later want to change the entries, you can simply
    edit the file :file:`~/.et_micc/micc.json`.

You should be good to go now.

Productivity tip
~~~~~~~~~~~~~~~~
Create a bash script to set the environment for your project consistently over time, e.g.::

    #!/usr/bin/bash
    module load git
    module load CMake
    # load my favourite python:
    module load Python
    cd path/to/myproject
    # activate myproject's virtual environment:
    source .venv/bin/activate
