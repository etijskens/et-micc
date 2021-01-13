
This document walks you through the differences of using micc_ to manage your
python+C++/Fortran projects on the VSC clusters. If you are already familiar with
the use of HPC environments, the only relevant part of this tutorial is section
`6.2 Using Poetry on the cluster`_. Otherwise, it is recommended to go through
the entire tutorial.

.. note:: This tutorial uses the Leibniz cluster of the University of Antwerp for the
    examples. The principles pertain, however, to all VSC clusters, and most probably
    also to other clusters using a module system for exposing its software stack.

Tutorial 6 - Using micc projects on the VSC clusters
====================================================

Most differences between using your local machine or a cluster stem from
the fact that a cluster, typically, uses a *module* system for making software
available to the user on a login node (interactive mode) and to a compute node
(batch mode). In addition, the cluster uses a scheduler that determines when your
compute jobs are executed.

The tools we need are, typically:

* a modern Python version. As Python 2.7 is officially discontinued, that would
  probably be 3.7 or later.
* common Python packages for computing, like Numpy, scipy, matplotlib, ...
* compilers for C++ and/or Fortran, for compiling binary extensions.
* CMake, as the build system for C++ binary extensions.
* git, for version control, if we are developing code on the cluster.

6.1 Using modules
-----------------
The cluster's operating system exposes some of these tools, but, they lag
many versions behind and, although very reliable, they are **not** fit for
high performance computing purposes.

As an example consider the GCC C++ compiler ``g++``. Here is the ``g++`` version
exposed by the operating system (at the day of writing: August 2020)::

    > which g++
    /usr/bin/g++
    > g++ --version
    g++ (GCC) 4.8.5 20150623 (Red Hat 4.8.5-39)
    ...

Still at the day of writing, the latest GCC version is 6 major versions ahead of
that: 10.2! The OS g++ is very reliable for building operating system components
but it is not suited for building C++ binary extensions that must squeeze the last
bit of performance out of the cluster's hardware. Obviously, this old g++ can
impossibly be aware of modern hardware, and, consequentially, cannot generate
code that exploit all the modern hardware features introduced for improving
performance of scientific computations.

Similarly, the OS Python is 2.7.5, whereas 3.9 is almost released, and 2.7.x isn't
even officially supported anymore.

So as a rule of thumb:

    **Never use the tools provided by the operating system.**

As the preinstalled modules are built by VSC specialists for optimal performance on
the cluster hardware, this rule should be extended as:

    **Do not install your own tools (unless they are not performance critical, or, you are a specialist yourself).**

If you need some software package, a library, a Python module, or, whatever, which
is not available as a cluster module, especially, if it is performance critical, contact
your local VSC team and they will build and install it for you (and all other users).

The VSC Team has installed many software packages ready to be used for high performance
computing. In fact, they are built using the modern compilers and with optimal performance
in mind. Contrary to what you are used to on your personal computer where installed software
packages are immediately accessible, on the cluster an extra step must be taken to
make installed packages accessible.

If you are unsure whether a command is provided by the operating system or not, use the
linux ``which`` command::

    > which g++
    /usr/bin/g++

Typically, commands of the operating system are found in ``/usr/bin`` and should
usually not be used for high performance computing. Commands provided by some
cluster module are, typically, found in ``/apps/<vsc-site>/...``.

.. note::
   The ``which cmd`` command shows the path to the first ``cmd`` on the PATH
   environment variable.

So, how do we get access to the commands we are supposed to use?

HPC packages are installed as modules and to make
them accessible, they must be loaded. Loading a module means that your operating system
environment is modified such that it can find the software's executables, that is, the
directories containing its executables are added to the ``PATH`` variable. In additio,
other environment variables adjusted or added to make everything work smoothly.

E.g., to use a recent version of git_ we load the git module::

    > module load git
    > which git
    /apps/antwerpen/broadwell/centos7/git/2.13.3/bin/git
    > git --version
    git version 2.13.3

Before we loaded ``git``, the ``which`` command would have shown::

    > which git
    /usr/bin/git
    > git --version
    git version 1.8.3.1

A much older version, indeed.

You can search for modules containing e.g. the word ``gcc`` (case insensitive)::

    > module spider gcc
    ...

If you know the package name, you can list the available versions with ``module av``. Here are
the available Python versions (the command is case insensitive)::

    > module av python/

which on Leibniz returns::

    ----------------------------------------------------- /apps/antwerpen/modules/centos7/software-broadwell/2019b -----------------------------------------------------
       Biopython/1.74-GCCcore-8.3.0-IntelPython3-2019b    Biopython/1.74-intel-2019b-Python-3.7.4 (D)    Python/3.7.4-intel-2019b (D)
       Biopython/1.74-intel-2019b-Python-2.7.16           Python/2.7.16-intel-2019b

    ----------------------------------------------------- /apps/antwerpen/modules/centos7/software-broadwell/2018b -----------------------------------------------------
       Python/2.7.15-intel-2018b    Python/3.6.8-intel-2018b    Python/3.7.0-intel-2018b    Python/3.7.1-intel-2018b

    ----------------------------------------------------- /apps/antwerpen/modules/centos7/software-broadwell/2018a -----------------------------------------------------
       Python/2.7.14-intel-2018a    Python/3.6.4-intel-2018a    Python/3.6.6-intel-2018a

    ----------------------------------------------------- /apps/antwerpen/modules/centos7/software-broadwell/2017a -----------------------------------------------------
       Biopython/1.68-intel-2017a-Python-2.7.13    pbs_python/4.6.0-intel-2017a-Python-2.7.13    Python/3.6.1-intel-2017a
       Biopython/1.68-intel-2017a-Python-3.6.1     Python/2.7.13-intel-2017a

      Where:
       D:  Default Module

    If you need software that is not listed, request it at hpc@uantwerpen.be

Please, mind the last line. If you need something that is not pre-installed, request it at mailto:hpc@antwerpen.be

You can unload a module::

    > module unload git
    > which git
    /usr/bin/git

The current ``git`` command is that of the OS again.

You can unload all modules::

    > module purge

To learn the details about the VSC clusters' module system, consult
`Using the module system <https://vlaams-supercomputing-centrum-vscdocumentation.readthedocs-hosted.com/en/latest/software/software_stack.html#using-the-module-system>`_.

6.2 Using Poetry on the cluster
-------------------------------

6.2.1 Installing Poetry
^^^^^^^^^^^^^^^^^^^^^^^
Poetry_ is, sofar, not available as a cluster module. You must install it yourself. The
installation method recommended by the poetry_documentation_ is also applicable on the
cluster (even when the system Python version is still 2.7.x)::

    > module purge
    > curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

The ``module purge`` command ensures that the system Python is used for the Poetry_ installation.
This allows you to have a single poetry_ installation that works for all Python versions that you
might want to use. So, internally, poetry_ commands use the system Python which is always available,
but your projects can use any Python version that is made avaible by loading a cluster module, or,
that you installed yourself.

6.2.2 Using pre-installed Python packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
As the cluster modules generally come with pre-installed Python packages which are built
to achieve optimal performance in a HPC environment, e.g. Numpy_, `Scipy <https://scipy.org/>`_,
...) we do not want ``poetry install`` to reinstall these packages in your project's virtual
environment. That would lead to suboptimal performance, and waste disk space. Fortunately,
there is a way to tell Poetry_ that it must use pre-installed Python packages::

    > mkdir -p ~/.cache/pypoetry/virtualenvs/.venv
    > echo 'include-system-site-packages = true' > ~/.cache/pypoetry/virtualenvs/.venv/pyvenv.cfg'

(If the name of your project's virtual environment is not ``.venv``, replace it with the
name of your project's virtual environment).

6.3 Using micc_ on the cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
First, we make sure to load a modern Python version for our project. The VSC clusters have many
Python versions available, and come in different flavours, depending on the toolchain that was
used to build them. On Leibniz, e.g., we would load::

    > module load leibniz/2019b     # unleashed all modules compiled with the intel-2019b toolchain
    > module load Python/3.7.4-intel-2019b

This module comes with a number of pre-installed Python package wich you can see using;;

    > ll $(dirname `which python`)/../lib/python3.7/site-packages

The above ``Python/3.7.4-intel-2019b`` is a good choice. Usually, loading a Python module
will automatically also make the C++ and Fortran compilers available that were used to compile
that Python module. They are, obviously, needed for building binary extensions from C++ and
Fortran code.

in addition, Micc_ relies on a number of other software package to do its work.

* Git_, our preferred  version control system. The system ``git`` is a bit old, hence::

    > module purge
    > git --version
    git version 1.8.3.1 # this is the system git
    > module load git
    > git --version
    git version 2.13.3

* For building binary extensions from C++ we need CMake_, hence::

    > cmake --version
    cmake version 2.8.12.2 # this is the system CMake
    > module load leibniz/2019b
    > module load CMake
    > cmake --version
    cmake version 3.11.1

* For building binary extensions from Fortran, we need f2py_, which is made available from
  Numpy_. Hence, we need to load a cluster Python module with Numpy_ pre-installed (please
  check `7.2.2 Using pre-installed Python packages`_ for this). The above loaded Python version
  is ok for that.

