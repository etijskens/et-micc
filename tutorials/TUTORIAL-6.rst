
.. _tutorial-6:

Tutorial 6 - Using micc projects on the VSC clusters
====================================================

This tutorial uses the Leibniz cluster of the University of Antwerp for the
examples. The principles pertain, however, to all VSC clusters, and most probably
also to other clusters using a module system for exposing its software stack.

Most differences between using your local machine or a cluster stem from these
facts:

    * a cluster is mainly a console based system accessed by the user on a login-node,
    * a *scheduler* determines when your compute jobs are executed on one or more
      compute-nodes,
    * a *module* system is used for making software available, both on the login-nodes
      and on the compute-nodes.

The cluster's module system has the largest impact, so let us look at this first.

6.1 Accessing the cluster
-------------------------
Accessing a login-node of a VSC_ cluster is detailed in the VSC_ documentation
`Logging in to a cluster <https://vlaams-supercomputing-centrum-vscdocumentation.readthedocs-hosted.com/en/latest/access/access_and_data_transfer.html#logging-in-to-a-cluster>`_.
By following the procedure, you get a console window (or a terminal, or a command prompt)
connected to one of the login-nodes of the cluster::

    > ssh -i path/to/my_key my_vsc_userid@login1-leibniz.hpc.uantwerpen.be
    Last login: Wed Jan 13 08:52:51 2021 from 91.179.29.29

    --------------------------------------------------------------------

    Welcome to LEIBNIZ !

    Useful links:
      https://vscdocumentation.readthedocs.io
      https://vscdocumentation.readthedocs.io/en/latest/antwerp/tier2_hardware.html
      https://www.uantwerpen.be/hpc

    Questions or problems? Do not hesitate and contact us:
      hpc@uantwerpen.be

    Happy computing!
    >

6.2 Using clusterr modules
--------------------------
The module system of the VSC_ clusters is explained in the VSC documentation
`Using the module system <https://vlaams-supercomputing-centrum-vscdocumentation.readthedocs-hosted.com/en/latest/software/software_stack.html#using-the-module-system>`_.

HPC packages are installed as modules (yet another kind of module) and to make
them accessible, they must be loaded. Loading a module means that your operating system's
environment is modified such that it can find the software's executables, that is, the
directories containing its executables are added to the ``PATH`` variable. In addition,
other environment variables adjusted or added to make everything work smoothly.

E.g., to use a recent version of git_ we ``load`` the git module::

    > module load git
    > which git
    /apps/antwerpen/broadwell/centos7/git/2.13.3/bin/git
    > git --version
    git version 2.13.3
    >

The ``which <cmd>`` command prints the location of the first occurrence of ``<cmd>`` on
the system path. Typically, commands of the operating system are found in ``/usr/bin``. Commands
provided by some cluster module are, typically, found in ``/apps/<vsc-site>/...``.

By not specifying a version in the ``module load`` command, we get the default git
module, which is usually the most recent installed version, in this case version 2.13.3.

Note that the operating system of the login-node also exposes a git version. If we
run the last two commands without the git module loaded, this is the result::

    > module unload git
    > which git
    /usr/bin/git
    > git --version
    git version 1.8.3.1
    >

This is a much older version. The login-node's operating system exposes several tools
we might need, like git, but also compilers, like ``g++``::

    > which g++
    /usr/bin/g++
    > g++ --version
    g++ (GCC) 4.8.5 20150623 (Red Hat 4.8.5-39)
    ...

The operating system tools usually lag many versions behind their current latest version,
e.g. the current latest ``g++`` version is  10.2! Although the operating system ``g++``
is very reliable for building operating system components, it is not suited for building
C++ programs and librariees that must squeeze the last bit of performance out of the
cluster's hardware. Obviously, this old g++ can impossibly be aware of modern hardware,
and, consequentially, cannot generate code that exploit all the modern hardware features
introduced for improving the performance of scientific computations. So as a rule of thumb:

    **Never use the tools provided by the operating system for building HPC software.**

The VSC Team has installed many software packages ready to be used for high performance
computing. In fact, they are built using the modern compilers and with optimal performance
in mind. Contrary to what you are used to on your personal computer where installed software
packages are immediately accessible, on the cluster an extra step must be taken to
make installed packages accessible.


You can search for modules containing e.g. the word ``gcc`` (case insensitive)::

    > module spider gcc
    ...

If you know the package name, you can list the available versions with ``module av``. Here are
the available Python versions (the command is case insensitive)::

    > module av python/
    ...

You can ``unload`` a module::

    > module unload git
    > which git
    /usr/bin/git

The current ``git`` command is that of the OS again.

You can unload all modules::

    > module purge

6.2 Using Micc on the cluster
-------------------------------
The tools we need as micc users are, typically:

* a modern Python version, e.g. 3.7 or later.
* common Python packages for computing, like numpy, scipy, matplotlib, ...
* Poetry, for dependency resolution, publishing to PyPI_ and virtual environment creation
* compilers for C++ and/or Fortran, for compiling binary extensions.
* CMake, as the build system for C++ binary extensions.
* git, for version control, if we are developing code on the cluster.

and, of course

* micc, and
* micc-build

6.2.1 Python and Python packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On Leibniz, two different Python distributions are available, each in several versions.
There is the standard Python distribution from python.org:

* Python/2.7.13-intel-2017a
* Python/2.7.14-intel-2018a
* Python/2.7.15-intel-2018b
* Python/2.7.16-intel-2019b
* Python/3.6.1-intel-2017a
* Python/3.6.4-intel-2018a
* Python/3.6.6-intel-2018a
* Python/3.6.8-intel-2018b
* Python/3.7.0-intel-2018b
* Python/3.7.1-intel-2018b
* Python/3.7.4-intel-2019b
* Python/3.8.3-intel-2020a

Each module specifies the Python version, and the compiler suite used to compile it.
E.g. Python/3.8.3-intel-2020a is Python version 3.8.3 compiled with the Intel compiler
suite 2020a. There is also the Intel Python distribution which has been compiled by
Intel specialists.

* IntelPython2/2019b -> Python 2.7.16
* IntelPython3/2019b -> Python 3.6.9
* IntelPython3/2020a -> Python 3.7.7

In most cases these cluster modules come with a whole bunch of preinstalled Python
packages useful for HPC, e.g. Numpy, scipy, and many others. For some the Python
packages are in a separate module:

* IntelPython3-Packages/2019b
* IntelPython3-Packages/2020a-intel-2020a

So to use the most recent Intel Python available with the packages, we must load::

    > module load IntelPython3-Packages/2020a-intel-2020a
    > module list

    Currently Loaded Modules:
      1) leibniz/supported             5) IntelPython3/2020a             9) HDF5/1.10.6-intel-2020a-MPI
      2) GCCcore/9.3.0                 6) baselibs/2020a-GCCcore-9.3.0  10) buildtools/2020a
      3) binutils/2.34-GCCcore-9.3.0   7) Tcl/8.6.10-intel-2020a        11) IntelPython3-Packages/2020a-intel-2020a
      4) intel/2020a                   8) SQLite/3.31.1-intel-2020a

6.2.2 Using Poetry
^^^^^^^^^^^^^^^^^^

Poetry_ is, sofar, not available as a cluster module. If you insist on having it, you have
to install it yourself. On a VSC cluster this can best be done like this::

    > module load IntelPython3
    > export POETRY_HOME=$VSC_DATA/.poetry
    > curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
    > source /data/antwerpen/201/vsc20170/.poetry/env

This installs poetry_ in your $VSC_DATA file system, rather than  in :file:`$HOME/.poetry/bin`
where it would consume to much of your file quota. If the system's Python is Python 3.x, rather
than 2.7.x, the first line is not necessary. The last line makes sure the current shell can use
``poetry`` right away.

A more serious problem is that, so far, Poetry doesn't play well with the system site-packages.
There are two issues:

#.  ``poetry install`` fails unless we create the virtual environment ourselves wiht the
    ``--system-site-packages`` flag. Poetry will then use :file:`.venv` (if it is activated)
    to install the dependencies::

        > python -m venv .venv --system-site-packages
        > source .venv/bin/activate
        (.venv) > poetry install
        ...

#.  The second issue is that poetry will install newer versions of the system site packages
    (in :file:`.venv` if it finds any. In general that will cause no problems. However, some of
    the system site packages have been built with special attention to performance because they
    are heavily used for scientific computation. One such package is numpy, which is a dependency
    of micc-build. E.g. the above :file:`IntelPython3` module has numpy 1.18.5 pre-installed as a
    system site package. Unfortunately, ``poetry install`` ignores its presence and installs a more
    recent version (c.q. 1.20.1), but this lack the performance optimisation features of the pre-
    installed version. To make use of the pre-installed numpy, we must manually remove the newer
    version installed in the virtual environment::

        > pip uninstall numpy

    This will remove numpy 1.20.1, and any references to numpy will now make use of the pre-installed
    numpy 1.18.5.

Admittedly, this approach is not very elegant, but it is expected that the poetry_ developers
will solve this problem some day. If the approach above does not suit you, you can go on without
using poetry, as explained below. The consequences of refraining from Poetry_ are not to hard:

* we must create our virtual environments ourselves,
* we must manually install required Python modules that are not available in the system
  site packages,
* and we cannot publish.

Although the latter seems very restrictive, if you put your project on github, you can always
check out the project on a desktop or laptop to publish it with Poetry. For the other two issues
a simple workaround is presented below:

6.2.3 Manual management of virtual environments and dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Since for this we cannot rely on poetry, we must do it manually. This command::

    > python -m venv .venv --system-site-packages

creates a virtual environment :file:`.venv` in the current working directory (typically
a project directory). The ``--system-site-packages`` flag ensures that system site packages
will be found by the ``python`` command. Otherwise, you will not be able to import numpy,
e.g.. As usual the virtual environment is activated as:

    > source .venv/bin/activate
    (.venv) >

With the ``IntelPython3`` and associated packages loaded as above::

    (.venv) > python
    Python 3.7.7 (default, Jun 26 2020, 05:10:03)
    [GCC 7.3.0] :: Intel(R) Corporation on linux
    Type "help", "copyright", "credits" or "license" for more information.
    Intel(R) Distribution for Python is brought to you by Intel Corporation.
    Please check out: https://software.intel.com/en-us/python-distribution
    >>> import numpy as np
    >>> np.__version__
    '1.18.5'
    >>> np.__file__
    '/apps/antwerpen/x86_64/centos7/intel-psxe/2020.02/intelpython3/lib/python3.7/site-packages/numpy/__init__.py'
    >>>

Note that the ``python`` executable ``/data/antwerpen/201/vsc20170/workspace/ET-dot/.venv/bin/python``
is in fact a soft link to the python of the cluster module ``IntelPython3/2020a``. By
using soft links the virtual environment takes up very little disk space and very little
time to be created.

6.2.4 Installing dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Installing the dependencies of our project without Poetry_, is easily achieved using
``pip install``. If you follow the recommended workflow and first develop your project
on your own machine (where you can use poetry_), and then port it to the cluster,
things are really easy:

    #. develop your project on your own personal computer.
    #. when everything works, push your code to the project's remote github repo.
    #. clone the github repo on the cluster in your :file:`$VSC_DATA` filesystem.
    #. create a virtual environment as detailed above in your project directory on
       the cluster, and activate it.
    #. check the :file:`pyproject.toml` file for the dependencies and development
       dependencies and run ``pip install`` for each of them.

You are now ready to test your project on the cluster.

Being lazy, there is a quick and dirty way as well. Just run your python code as is,
and when you get an ``ImportError``, run ``pip install`` for the missing Python package.

Starting the development of your project on the cluster is not recommended, because
you can easily forget to update :file:`pyproject.toml` when adding dependencies.
Porting the project to your own machine will then not have the correct dependencies.

Having a system-wide ``micc`` on the cluster is not very practical. We recommend to
``pip install micc-build`` or at least ``pip install micc`` (if you do not need to
build binary extension modules) in your project's virtual environment. To use micc
then, you must, obviously, activate the virtual environment.

6.2.5 Access to compilers
^^^^^^^^^^^^^^^^^^^^^^^^^
For building binary extension modules from Fortran micc-build needs access to a Fortran
compiler and a C compiler as well. For C++ binary extension modules access to a C++
compiler is needed. The above loaded ``IntelPython3/2020a`` module was compiled with the
Intel 2020a compiler toolchain so we must load::

    (.venv) > module load intel/2020a
    (.venv) > which ifort
    /apps/antwerpen/x86_64/centos7/intel-psxe/2020.04/compilers_and_libraries_2020.4.304/linux/bin/intel64/ifort
    (.venv) > which icc
    /apps/antwerpen/x86_64/centos7/intel-psxe/2020.04/compilers_and_libraries_2020.4.304/linux/bin/intel64/icc
    (.venv) > which icpc
    /apps/antwerpen/x86_64/centos7/intel-psxe/2020.04/compilers_and_libraries_2020.4.304/linux/bin/intel64/icpc
    (.venv) >

6.2.6 CMake
^^^^^^^^^^^
CMake is available as a cluster module::

    > module load CMake
    > module list

    Currently Loaded Modules:
      1) leibniz/supported
      2) GCCcore/9.3.0
      3) binutils/2.34-GCCcore-9.3.0
      4) IntelPython3/2020a
      5) intel/2020a
      6) baselibs/2020a-GCCcore-9.3.0
      7) Tcl/8.6.10-intel-2020a
      8) SQLite/3.31.1-intel-2020a
      9) HDF5/1.10.6-intel-2020a-MPI
      10) buildtools/2020a
      11) IntelPython3-Packages/2020a-intel-2020a
      12) CMake/3.11.1

6.2.6 Git
^^^^^^^^^
As said, git too is available as a cluster module::

    > module load git
    > module list

    Currently Loaded Modules:
      1) leibniz/supported
      2) GCCcore/9.3.0
      3) binutils/2.34-GCCcore-9.3.0
      4) IntelPython3/2020a
      5) intel/2020a
      6) baselibs/2020a-GCCcore-9.3.0
      7) Tcl/8.6.10-intel-2020a
      8) SQLite/3.31.1-intel-2020a
      9) HDF5/1.10.6-intel-2020a-MPI
      10) buildtools/2020a
      11) IntelPython3-Packages/2020a-intel-2020a
      12) CMake/3.11.1
      13) git/2.13.3

6.2.7 A remark on the order of things
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The first step when starting a cluster session on a login-node should always be to
load all modules you need, followed by activating the virtual environment of your
project. It is easy to forget things, so we recommend to put a bash script in your
project directory that does this. E.g.::

    # setup.sh script
    module load git
    module load CMake
    module load IntelPython3/2020a
    module load IntelPython3-Packages/2020a-intel-2020a
    module load intel/2020a
    module list
    source .venv/bin/activate

As the script must be ``source``-d (to expose the loaded modules in your shell,
and to activate the virtual environment), it is better
not to make it executable, so you cannot forget to source it. (To ``source`` a
script, it must not be executable).
