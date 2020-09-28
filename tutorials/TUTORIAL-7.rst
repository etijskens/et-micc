This document walks you through the differences of using micc_ to manage your
python+C++/Fortran projects on the VSC clusters. If you are already familiar with
the use of HPC environments, the only relevant part of this tutorial is section
`7.2 Using Poetry on the cluster`_. Otherwise, it is recommended to go through
the entire tutorial.

.. note:: This tutorial uses the Leibniz cluster of the University of Antwerp for the
    examples. The principles pertain, however, to all VSC clusters, and most probably
    also to other clusters using a module system for exposing its software stack.

Tutorial 7 - Using micc projects on the VSC clusters
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

7.1 Using modules
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

You can list the loaded modules::

    > module list

You can unload a module::

    > module unload git
    > which git
    /usr/bin/git

The current ``git`` command is that of the OS again.

You can unload all modules::

    > module purge

To learn the details about the VSC clusters' module system, consult
`Using the module system <https://vlaams-supercomputing-centrum-vscdocumentation.readthedocs-hosted.com/en/latest/software/software_stack.html#using-the-module-system>`_.

7.2 Using Poetry on the cluster
-------------------------------

7.2.1 Installing Poetry
^^^^^^^^^^^^^^^^^^^^^^^
Poetry_ is, sofar, not available as a cluster module. You must install it yourself. The
installation method recommended by the `Poetry documentation <https://python-poetry.org/docs/#installation>`_
is also applicable on the cluster (even when the system Python version is still 2.7.x)::

    > module purge
    > curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

The ``module purge`` command ensures that the system Python is used for the Poetry_ installation.
This allows you to have a single poetry_ installation that works for all Python versions that you
might want to use. So, internally, poetry_ commands use the system Python which is always available,
but your projects can use any Python version that is made avaible by loading a cluster module, or,
that you installed yourself.

7.2.2 Using pre-installed Python packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
As the cluster modules generally come with pre-installed Python packages which are built
to achieve optimal performance in a HPC environment, e.g. Numpy_, Scipy_, ...) we do not want
``poetry install`` to reinstall these packages in your project's virtual environment. That
would lead to suboptimal performance, and waste disk space. Fortunately, there is a way to
tell Poetry_ that it must use pre-installed Python packages::

    > mkdir -p ~/.cache/pypoetry/virtualenvs/.venv
    > echo 'include-system-site-packages = true' > ~/.cache/pypoetry/virtualenvs/.venv/pyvenv.cfg'

(If the name of your project's virtual environment is not ``.venv``, replace it with the
name of your project's virtual environment).

7.3 Using micc_ on the cluster
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

TODO:

7.4 Using conda Python distributions
------------------------------------
You can set up your own Conda virtual environments on the cluster, just as we described
in `Tutorial 6 - Using conda python and conda virtual environments`_. The problem with that
approach is that it consumes a lot of your file quota due to the fact that it relies much
more on copies than the Python :py:mod:`venv` module. For that reason we do not recommend it.
If you, nevertheless, use this approach, make sure you set this up in the ``$VSC_DATA`` file
space, because if you do it in the ``$VSC_HOME`` file space, you will probably run out of file
quota before the virtual environment is ready.

.. note:: interesting links when investigating the above statement:

    * `University of Utah: Why are we moving away from a central Python installation? <https://www.chpc.utah.edu/documentation/software/python-anaconda.php>`_
    * https://www.epcc.ed.ac.uk/blog/2018/03/08/installing-python-packages-virtual-environments

There is, however, an alternative method which uses the PYTHONPATH environment variable to
extend the IntelPython3 cluster modules. It is a bit of a low-level hack, but it is not
overly complicated, and works well.

First, we select the toolchain::

    > module load leibniz/2019b
    The following have been reloaded with a version change:
      1) leibniz/supported => leibniz/2019b

Then we load an IntelPython version (which is a conda distribution optimized by Intel)::

    > module load IntelPython3/2019b.05
    > python --version
    Python 3.6.9 :: Intel Corporation

As usual it comes with a whole bu of pre-installed Python packages::

    > conda list
    # packages in environment at /apps/antwerpen/x86_64/centos7/intel-psxe/2019_update5/intelpython3:
    #
    asn1crypto                0.24.0                   py36_3    intel
    bzip2                     1.0.6                        18    intel
    certifi                   2018.1.18                py36_2    intel
    cffi                      1.11.5                   py36_3    intel
    chardet                   3.0.4                    py36_3    intel
    conda                     4.3.31                   py36_3    intel
    ...

Cd into our project's root directory::

    > cd $VSC_DATA/workspace/ET-dot

Here we create a directory that will serve as a surrogate for the a virtual environment::

    > mkdir .cenv

The name chosens is arbitrary of course, but it resembles the .venv we had above when using
the :py:mod:`venv` Python package. In fact, also the location is arbitrary, but the project
root directory is a familiar place for this.

Next, we use pip_ to install et-micc-build into :file:`.cenv`::

    > pip install -t .cenv et-micc-build
    Collecting et-micc-build==0.10.13
      Using cached https://files.pythonhosted.org/packages/1f/41/a3c2ca300f735742f7183127afaf302e3c9875ff14dedf1cf14b1850774e/et_micc_build-0.10.13-py3-none-any.whl
    ...
    Successfully installed MarkupSafe-1.1.1 Pygments-2.5.2 alabaster-0.7.12 arrow-0.15.4
    babel-2.7.0 binaryornot-0.4.4 certifi-2019.11.28 chardet-3.0.4 click-7.0 cookiecutter-1.6.0
    docutils-0.15.2 et-micc-0.10.13 et-micc-build-0.10.13 future-0.18.2 idna-2.8 imagesize-1.1.0
    jinja2-2.10.3 jinja2-time-0.2.0 numpy-1.17.4 packaging-19.2 pbr-5.4.4 poyo-0.5.0 pybind11-2.4.3
    pyparsing-2.4.5 python-dateutil-2.8.1 pytz-2019.3 requests-2.22.0 semantic-version-2.8.3
    setuptools-42.0.2 six-1.13.0 snowballstemmer-2.0.0 sphinx-2.3.0 sphinx-click-2.3.1
    sphinx-rtd-theme-0.4.3 sphinxcontrib-applehelp-1.0.1 sphinxcontrib-devhelp-1.0.1
    sphinxcontrib-htmlhelp-1.0.2 sphinxcontrib-jsmath-1.0.1 sphinxcontrib-qthelp-1.0.2
    sphinxcontrib-serializinghtml-1.1.3 tomlkit-0.5.8 urllib3-1.25.7 walkdir-0.4.1
    whichcraft-0.6.1

Note, that Numpy_ 1.17.4 is installed too, which we wanted to avoid because it is not optimised
for the cluster. Because we are not installing into the environment's :file:`site-packages`
directory, pip does not cross-check if the packages are already available there and there
is no flag to make it do that. Hence, we must **manually remove numpy**::

    > rm -rf .cenv/numpy*\

We must also install pytest_ as it is not in the Intel Python distribution, nor is it a
dependency of micc-build_.

    > pip install -t .cenv pytest

Now set the ``PYTHONPATH`` environment variable to the :file:`.cenv` directory and export it::

    > export PYTHONPATH=$PWD/.cenv

.. note:: The ``PYTHONPATH`` environment variable is retained for the duration of the terminal
    session only.

Run pytest to see if everything is working::

    > python -m pytest
    ========================================================== test session starts ==========================================================
    platform linux -- Python 3.6.9, pytest-5.3.2, py-1.8.0, pluggy-0.13.1
    rootdir: /data/antwerpen/201/vsc20170/workspace/ET-dot
    collected 8 items / 1 error / 7 selected

    ================================================================ ERRORS =================================================================
    ________________________________________________ ERROR collecting tests/test_cpp_dotc.py ________________________________________________
    tests/test_cpp_dotc.py:10: in <module>
        cpp = et_dot.dotc
    E   AttributeError: module 'et_dot' has no attribute 'dotc'
    ------------------------------------------------------------ Captured stdout ------------------------------------------------------------
    [ERROR]
        Binary extension module 'bar{get_extension_suffix}' could not be build.
        Any attempt to use it will raise exceptions.

    ...
    ------------------------------------------------------------ Captured stderr ------------------------------------------------------------
    [INFO] [ Building cpp module 'dotc':
    [INFO]           Building using default build options.
    [DEBUG]          [ > cmake -D PYTHON_EXECUTABLE=/apps/antwerpen/x86_64/centos7/intel-psxe/2019_update5/intelpython3/bin/python -D pybind11_DIR=/data/antwerpen/201/vsc20170/workspace/ET-dot/.cenv/et_micc_build/cmake_tools ..
    [DEBUG]              (stdout)
                           -- The CXX compiler identification is GNU 4.8.5
                           -- Check for working CXX compiler: /usr/bin/c++
                           -- Check for working CXX compiler: /usr/bin/c++ -- works
                           -- Detecting CXX compiler ABI info
                           -- Detecting CXX compiler ABI info - done
                           -- Detecting CXX compile features
                           -- Detecting CXX compile features - done
                           -- Found PythonInterp: /apps/antwerpen/x86_64/centos7/intel-psxe/2019_update5/intelpython3/bin/python (found version "3.6.9")
                           -- Found PythonLibs: /apps/antwerpen/x86_64/centos7/intel-psxe/2019_update5/intelpython3/lib/libpython3.6m.so
                           -- Performing Test HAS_CPP14_FLAG
                           -- Performing Test HAS_CPP14_FLAG - Failed
                           -- Performing Test HAS_CPP11_FLAG
                           -- Performing Test HAS_CPP11_FLAG - Success
                           -- Performing Test HAS_FLTO
                           -- Performing Test HAS_FLTO - Success
                           -- LTO enabled
                           -- Configuring done
                           -- Generating done
                           -- Build files have been written to: /data/antwerpen/201/vsc20170/workspace/ET-dot/et_dot/cpp_dotc/_cmake_build
    [DEBUG]          ] done.
    [DEBUG]          [ > make
    [WARNING]            > make
    [WARNING]            (stdout)
                         Scanning dependencies of target dotc
                         [ 50%] Building CXX object CMakeFiles/dotc.dir/dotc.cpp.o
    [WARNING]            (stderr)
                         /data/antwerpen/201/vsc20170/workspace/ET-dot/et_dot/cpp_dotc/dotc.cpp:8:31: fatal error: pybind11/pybind11.h: No such file or directory
                          #include <pybind11/pybind11.h>
                                                        ^
                         compilation terminated.
                         make[2]: *** [CMakeFiles/dotc.dir/dotc.cpp.o] Error 1
                         make[1]: *** [CMakeFiles/dotc.dir/all] Error 2
                         make: *** [all] Error 2
    [DEBUG]          ] done.
    [INFO] ] done.
    [INFO] [ Building f2py module 'dotf':
    [INFO]           Building using default build options.
    _f2py_build/src.linux-x86_64-3.6/dotfmodule.c:144:12: warning: ‘f2py_size’ defined but not used [-Wunused-function]
     static int f2py_size(PyArrayObject* var, ...)
                ^
    [DEBUG]          [ > ln -sf /data/antwerpen/201/vsc20170/workspace/ET-dot/et_dot/f2py_dotf/dotf.cpython-36m-x86_64-linux-gnu.so /data/antwerpen/201/vsc20170/workspace/ET-dot/et_dot/dotf.cpython-36m-x86_64-linux-gnu.so
    [DEBUG]          ] done.
    [INFO] ] done.
    =========================================================== warnings summary ============================================================
    /user/antwerpen/201/vsc20170/data/workspace/ET-dot/.cenv/past/builtins/misc.py:45
      /user/antwerpen/201/vsc20170/data/workspace/ET-dot/.cenv/past/builtins/misc.py:45: DeprecationWarning: the imp module is deprecated in favour of importlib; see the module's documentation for alternative uses
        from imp import reload

    /user/antwerpen/201/vsc20170/data/workspace/ET-dot/.cenv/cookiecutter/repository.py:19
      /user/antwerpen/201/vsc20170/data/workspace/ET-dot/.cenv/cookiecutter/repository.py:19: DeprecationWarning: Flags not at the start of the expression '\n(?x)\n((((git|hg)\\+)' (truncated)
        """)

    -- Docs: https://docs.pytest.org/en/latest/warnings.html
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ===================================================== 2 warnings, 1 error in 6.40s ======================================================

Inspecting the output shows us that we are half way: the f2py module :py:mod:`dotf` was built,
but the cpp module :py:mod:`dotc` failed to build because the pybind11 include files could not
be found. Although ``pybind11-2.4.3`` appears in the output of ``pip install -t .cenv et-micc-build``
above, it only installs the python components (which we don't need) and not the include files
(which we do need). This is not to difficult to solve. First clone the pybind11 git repo
somewhere in ``$VSC_DATA``. We choose to do that in the parent directory of ET-dot::

    > git clone https://github.com/pybind/pybind11.git
    Cloning into 'pybind11'...
    remote: Enumerating objects: 38, done.
    remote: Counting objects: 100% (38/38), done.
    remote: Compressing objects: 100% (30/30), done.
    remote: Total 11291 (delta 14), reused 12 (delta 3), pack-reused 11253
    Receiving objects: 100% (11291/11291), 4.22 MiB | 2.32 MiB/s, done.
    Resolving deltas: 100% (7612/7612), done.


Next, we must tell our ET-dot project where it can find the pybind11_ include files. Cd into the
:file:`_cmake_build` directory and edit the :file:`CMakeCache.txt` file::

    > cd ET-dot/et_dot/cpp_dotc/_cmake_build
    > vim CMakeCache.txt                        # or whatever editor you like...
    ...

There should be a ``CMAKE_CXX_FLAGS:STRING`` entry which must be set to ``-I``, followed
by the exact path of the :file:`pybind11/include/` directory::

    //Flags used by the CXX compiler during all build types.
    CMAKE_CXX_FLAGS:STRING=-I/data/antwerpen/201/vsc20170/workspace/pybind11/include/

.. note::This must be

Finally, running pytest_ again, we see that all our problems are solved::

    > python -m pytest
    ================================================ test session starts =================================================
    platform linux -- Python 3.6.9, pytest-5.3.2, py-1.8.0, pluggy-0.13.1
    rootdir: /data/antwerpen/201/vsc20170/workspace/ET-dot
    collected 9 items

    tests/test_cpp_dotc.py .                                                                                       [ 11%]
    tests/test_et_dot.py .......                                                                                   [ 88%]
    tests/test_f2py_dotf.py .                                                                                      [100%]

    ================================================= 9 passed in 0.25s ==================================================

