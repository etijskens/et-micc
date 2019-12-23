Tutorial 7 - Using micc projects on the VSC-clusters
====================================================

We distinguish to cases:

* installing a micc_-project for further development, and
* installing a micc_-project (in a virtual environment) for use in production runs.

.. note:: This tutorial uses the Leibniz cluster of the University of Antwerp as an
    example. The principles pertain, however, to all VSC clusters, and most probably
    also to other clusters using a module system for exposing its software stack.

7.1 Micc use on the cluster for developing code
-----------------------------------------------

Most differences between using  your local machine and using the cluster stem from
the fact that the cluster uses a *module* system for making software available to the
user, and less importantly, that the cluster uses a scheduler to run your compute jobs
in batch mode when the hardware you requested is available.

Most tools that are commonly used on the cluster are built for optimal performance and
pre-installed on the cluster. You need to make them available for execution by
``module load`` commands (for all the details see
`Using the module system <https://vlaams-supercomputing-centrum-vscdocumentation.readthedocs-hosted.com/en/latest/software/software_stack.html#using-the-module-system>`_).
Although the operating system also exposes some tools such as compilers, as they
are many versions behind and, consequentially, they are **not** fit for high performance
computing. As an example consider the ``git`` command. This is the git_ version exposed by
the operating system::

    > which git
    /usr/bin/git
    > git --version
    git version 1.8.3.1

When you load the git module you get version 2.13.3::

    > module load git
    > which git
    /apps/antwerpen/broadwell/centos7/git/2.13.3/bin/git

Though this is not the very latest git version, but it is definitely way ahead of 1.8.3.1.
Moreover, both versions differ in the major component of the version, which indicates that
they are not backward compatible.

As git is now available, we can clone the git repository of our ET-dot project in some
workspace directory (preferably somewhere on ``$VSC_DATA``) and ``cd`` into the project
directory::

    > cd $VSC_DATA/path/to/my/workspace
    > git clone https://github.com/etijskens/ET-dot
    Cloning into 'ET-dot'...
    remote: Enumerating objects: 116, done.
    remote: Counting objects: 100% (116/116), done.
    remote: Compressing objects: 100% (74/74), done.
    remote: Total 116 (delta 45), reused 100 (delta 29), pack-reused 0
    Receiving objects: 100% (116/116), 29.90 KiB | 0 bytes/s, done.
    Resolving deltas: 100% (45/45), done.
    > cd ET-dot

.. note::
    It is good practice to **clone git repositories in** ``$VSC_DATA``. Doing this in
    ``$VSC_HOME`` can easily consume all your file quota, and ``$VSC_SCRATCH`` is
    not backed up.

You will need also to load CMake if you want to build binary extension modules from C++
source code as the :py:mod:`dotc` module::

    > module load CMake

On our local machine we would now select a python version with pyenv_, and run
``poetry install`` to create a virtual environment and install :py:mod:`ET-dot`'s
dependencies. The pyenv_ part is again replaced by a ``module load`` command, e.g.::

    > module load leibniz/2019b
    > module load Python/3.7.4-intel-2019b

The first command selects all modules built with the Intel 2019b toolchain, and
the second makes Python 3.7.4 available together with a whole bunch of pre-installed
Python packages which are useful for high performance computing, such as numpy_, as
well as all their dependencies. To see them execute::

    > pip list
    Package            Version
    ------------------ ------------
    absl-py            0.7.1
    alabaster          0.7.12
    appdirs            1.4.3
    ...
    numpy              1.17.0
    ...

or::

    > conda list
    ???

The poetry_ part, requires - at least at the time of writing - some special attention.

7.1.1 Note about using Poetry on the cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
On our local machine we used poetry_ for

* virtual environment creation and management,
* installation of dependencies in a project's virtual environment, using the commands

  * ``poetry install``,
  * ``poetry update``,
  * ``poetry add`` and
  * ``poetry remove``,

* for publishing to PyPi_, with command ``poetry publish``.

We do **not** recommend using Poetry_ for installing dependencies on the cluster. The
main reason for this is that poetry masks any pre-installed Python packages that are made
available by the cluster software stack. Every Python distribution on the cluster comes
with a such set of pre-installed packages that are important for high performance computing,
and are built (compiled) to squeeze out the last bit of performance out of the hardware on
which they will run. Typical examples are Numpy_, `Scipy <https://www.scipy.org>`_,
`pandas <https://pandas.pydata.org>`_, ... ``Poetry install`` will install equally
functional packages which are built for running on many different hardwares, rather than for
optimal performance. By using ``poetry install`` performances will be sacrificed. In addition,
re-installing these packages consumes a lot of your file quota.

To avoid trouble, we thus recommend to **not** install poetry_ on the cluster. If you
want to publish your package, ``commit`` the changes to the git repository, ``push`` them
to github_, fetch the latest version on your local machine and use ``poetry publish --build``
to publish.

7.1.2 Virtual environments and dependencies on the cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If we can't use Poetry_ for creating virtual environments and installing dependencies,
we need some alternative way to achieve this. Fortunately, just doing this by hand is not
too difficult.

Creating a virtual environment in the project root directory is simple::

    > python -m venv .venv --system-site-packages

This command uses the :py:mod:`venv` package to create a virtual environment named ``.venv``.
The ``--system-site-packages`` flag ensures that the virtual environment also sees all the
pre-installed Python packages. The environment name is in fact arbitrary, but we choose to
use the same name as Poetry_ would use. The environment name is also the name of the directory
containing the virtual environment::

    > tree .venv
    .venv
    ├── bin
    │   ├── activate
    │   ├── activate.csh
    │   ├── activate.fish
    │   ├── easy_install
    │   ├── easy_install-3.7
    │   ├── pip
    │   ├── pip3
    │   ├── pip3.7
    │   ├── python -> /apps/antwerpen/broadwell/centos7/Python/3.7.4-intel-2019b/bin/python
    │   └── python3 -> python
    ├── include
    ├── lib
    │   └── python3.7
    │       └── site-packages
    │           ├── easy_install.py
    │           ├── pip
    │           │   ├── __init__.py
    │           │   ├──

This virtual environment can be activated by executing::

    > source .venv/bin/activate
    (.venv) >

As on our local machine the command prompt contains a small notice as to the activated
virtual environment. If in doubt you can always inspect the full path of the python
executable::

    (.venv) > which python
    /data/antwerpen/201/vsc2017/workspace/ET-dot/.venv/bin/python

To install the dependencies needed by the ET-dot project, we have two options,
a quick and dirty approach and a systematic approach. Let's be systematic first,
and checking the ``[tool.poetry.dependencies]`` section of the project's
:file:`pyproject.toml` file, ::

    (.venv) > cat pyproject.toml
    ...
    [tool.poetry.dependencies]
    python = "^3.7"
    et-micc-build = "^0.10.10"

    [tool.poetry.dev-dependencies]
    pytest = "^4.4.2"

    ...

The ``[tool.poetry.dependencies]`` section tells us that the our project depends on
micc-build_, so we install it with pip_, which is the standard Python install tool::

    (.venv) > pip install et-micc-build
    Collecting et-micc-build
      Downloading https://files.pythonhosted.org/packages/aa/00/d95e6cf3b584c1921655258ed4d5a51120ba0ad158e6ee9c0122b2ccd0b2/et_micc_build-0.10.11-py3-none-any.whl
    ...

As we did not specify a version, it will install the latest version of micc-build_ as
well as all its dependencies, but contrary to ``poetry install``, it will **only** install
packages for which the version specification is **not** met. E.g. the system site packages
of the :file:`Python/3.7.4-intel-2019b` module contain Numpy 1.17.0 which satisfies the
version specification by micc-build_ and thus Numpy is not installed, as is clear from the
output::

    ...
    Requirement already satisfied: numpy<2.0.0,>=1.17.0 in /apps/antwerpen/broadwell/centos7/Python/3.7.4-intel-2019b/lib/python3.7/site-packages/numpy-1.17.0-py3.7-linux-x86_64.egg (from et-micc-build) (1.17.0)
    ...

This is exactly the behavior we were looking for to avoid masking the system site packages.

An interesting side effect is that, since micc_ is a dependency of micc-build_, micc_ is now
installed in our virtual environment, and thus can be used to assist the further development
of the project::

    (.venv) > which micc
    /data/antwerpen/201/vsc20170/workspace/ET-dot/.venv/bin/micc
    (.venv) > micc --version
    micc, version 0.10.11

As micc-build_ is the only dependency, we can verify that everything works fine by running
``pytest``::

    (.venv) > python -m pytest

.. note:: just running ``pytest`` will fail because then ``pytest`` cannot see our virtual
    environment and will fail to import :py:mod:`et_dot`.

Here is the result::

    ========================================== test session starts ==========================================
    platform linux -- Python 3.7.4, pytest-5.0.1, py-1.8.0, pluggy-0.12.0
    rootdir: /data/antwerpen/201/vsc20170/workspace/ET-dot
    plugins: xonsh-0.9.9
    collected 9 items

    tests/test_cpp_dotc.py .                                                                          [ 11%]
    tests/test_et_dot.py .......                                                                      [ 88%]
    tests/test_f2py_dotf.py .                                                                         [100%]

    =========================================== warnings summary ============================================
    /apps/antwerpen/broadwell/centos7/Python/3.7.4-intel-2019b/lib/python3.7/site-packages/future-0.17.1-py3.7.egg/past/translation/__init__.py:35
      /apps/antwerpen/broadwell/centos7/Python/3.7.4-intel-2019b/lib/python3.7/site-packages/future-0.17.1-py3.7.egg/past/translation/__init__.py:35: DeprecationWarning: the imp module is deprecated in favour of importlib; see the module's documentation for alternative uses
        import imp

    /apps/antwerpen/broadwell/centos7/Python/3.7.4-intel-2019b/lib/python3.7/site-packages/future-0.17.1-py3.7.egg/past/types/oldstr.py:5
      /apps/antwerpen/broadwell/centos7/Python/3.7.4-intel-2019b/lib/python3.7/site-packages/future-0.17.1-py3.7.egg/past/types/oldstr.py:5: DeprecationWarning: Using or importing the ABCs from 'collections' instead of from 'collections.abc' is deprecated, and in 3.8 it will stop working
        from collections import Iterable

    /apps/antwerpen/broadwell/centos7/Python/3.7.4-intel-2019b/lib/python3.7/site-packages/future-0.17.1-py3.7.egg/past/builtins/misc.py:4
      /apps/antwerpen/broadwell/centos7/Python/3.7.4-intel-2019b/lib/python3.7/site-packages/future-0.17.1-py3.7.egg/past/builtins/misc.py:4: DeprecationWarning: Using or importing the ABCs from 'collections' instead of from 'collections.abc' is deprecated, and in 3.8 it will stop working
        from collections import Mapping

    .venv/lib/python3.7/site-packages/cookiecutter/repository.py:19
      /data/antwerpen/201/vsc20170/workspace/ET-dot/.venv/lib/python3.7/site-packages/cookiecutter/repository.py:19: DeprecationWarning: Flags not at the start of the expression '\n(?x)\n((((git|hg)\\+)' (truncated)
        """)

    -- Docs: https://docs.pytest.org/en/latest/warnings.html
    ================================= 9 passed, 4 warnings in 11.04 seconds =================================

Except for some ``DeprecationWarning`` warnings which are out of our reach, all tests succeed. Note,
however, that if we hadn't loaded the CMake module, building the :py:mod:`dotc` binary extension
would fail with and error telling that CMake cannot be found.

The second, quick and dirty approach, avoids checking the project's :file:`pyproject.toml`
file and runs ``python -m pytest`` right away, which (if we hadn't already installed micc-build_)
would fail all three tests::

    > python -m pytest
    ========================================== test session starts ==========================================
    platform linux -- Python 3.7.4, pytest-5.0.1, py-1.8.0, pluggy-0.12.0
    rootdir: /data/antwerpen/201/vsc20170/workspace/ET-dot
    plugins: xonsh-0.9.9
    collected 0 items / 3 errors

    ================================================ ERRORS =================================================
    ________________________________ ERROR collecting tests/test_cpp_dotc.py ________________________________
    ImportError while importing test module '/data/antwerpen/201/vsc20170/workspace/ET-dot/tests/test_cpp_dotc.py'.
    Hint: make sure your test modules/packages have valid Python names.
    Traceback:
    et_dot/__init__.py:10: in <module>
        import et_dot.dotc
    E   ModuleNotFoundError: No module named 'et_dot.dotc'

    During handling of the above exception, another exception occurred:
    tests/test_cpp_dotc.py:9: in <module>
        import et_dot.dotc as cpp
    et_dot/__init__.py:15: in <module>
        from et_micc_build.cli_micc_build import auto_build_binary_extension
    E   ModuleNotFoundError: No module named 'et_micc_build'
    _________________________________ ERROR collecting tests/test_et_dot.py _________________________________
    ImportError while importing test module '/data/antwerpen/201/vsc20170/workspace/ET-dot/tests/test_et_dot.py'.
    Hint: make sure your test modules/packages have valid Python names.
    Traceback:
    et_dot/__init__.py:10: in <module>
        import et_dot.dotc
    E   ModuleNotFoundError: No module named 'et_dot.dotc'

    During handling of the above exception, another exception occurred:
    tests/test_et_dot.py:10: in <module>
        import et_dot
    et_dot/__init__.py:15: in <module>
        from et_micc_build.cli_micc_build import auto_build_binary_extension
    E   ModuleNotFoundError: No module named 'et_micc_build'
    _______________________________ ERROR collecting tests/test_f2py_dotf.py ________________________________
    ImportError while importing test module '/data/antwerpen/201/vsc20170/workspace/ET-dot/tests/test_f2py_dotf.py'.
    Hint: make sure your test modules/packages have valid Python names.
    Traceback:
    et_dot/__init__.py:10: in <module>
        import et_dot.dotc
    E   ModuleNotFoundError: No module named 'et_dot.dotc'

    During handling of the above exception, another exception occurred:
    tests/test_f2py_dotf.py:8: in <module>
        import et_dot.dotf as f90
    et_dot/__init__.py:15: in <module>
        from et_micc_build.cli_micc_build import auto_build_binary_extension
    E   ModuleNotFoundError: No module named 'et_micc_build'
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ======================================== 3 error in 0.34 seconds ========================================

All three tests fail in more or less the same way. E.g in the last test there is first
a :py:exc:`ModuleNotFoundError`::

    E   ModuleNotFoundError: No module named 'et_dot.dotc'

which tells us that the binary extension :py:mod:`dotc` is not found. This is logical
because it hasn't been built. (You can verify that there are no :file:`.so` files by
running ``ls -l et_dot``.) The auto-build feature should normally take care of that.
The error gives rise to another :py:exc:`ModuleNotFoundError`::

    E   ModuleNotFoundError: No module named 'et_micc_build'

which tells us that micc-build_ is not installed in our virtual environment, which is
indeed necessary for engaging the auto-build feature. So we ``pip install`` it::

    (.venv) > pip install et-micc-build
    Collecting et-micc-build
    ...

and run the tests again to see that they succeed, meaning that the binary modules were
built, and that the auto-build feature was successfully engaged.

If the project needs other packages, you would continue to have :py:exc:`ModuleNotFoundError`
exceptions.
Each time you] ``pip install`` the missing package, and run the test until no more
:py:exc:`ModuleNotFoundError` exceptions arise and you are good to go.

A bash script for creating and activating the virtual environment may be practical,
e.g. :file:`micc-setup`, stored in some directory which is on your system PATH::

    #!/bin/bash
    # This is file micc-setup

    # load the modules needed
    module load leibniz/2019b
    module load Python/3.7.4-intel-2019b
    module load CMake
    module list

    if [ -d  ".venv" ]
    then
        echo "Virtual environment present: '.venv'"
        echo "Activating '.venv' ..."
        source .venv/bin/activate
    else
        # create new virtual environment
        python -m venv .venv --system-site-packages
        source .venv/bin/activate
        pip install et-micc
    fi

If most of your projects have binary extensions, you might choose to
``pip install et-micc-build`` on the second but last line.
When run in the project root directory, this script loads the needed modules and
activates the project's virtual environment :file:`.venv` if it exists, and, otherwise,
create it and install micc_. The dependencies of the project you must install yourself.

You must ``source`` this script in the project root directory. If you do not ``source`` the
script, the environment will be correctly setup, but the virtual environment will not be
activated when after the script terminates, nor will the modules be loaded::

    > cd path/to/ET-dot
    > source micc-setup

    Currently Loaded Modules:
      1) leibniz/2019b                  9) SQLite/3.29.0-intel-2019b
      2) GCCcore/8.3.0                 10) HDF5/1.8.21-intel-2019b-MPI
      3) binutils/2.32-GCCcore-8.3.0   11) METIS/5.1.0-intel-2019b-i32-fp64
      4) intel/2019b                   12) SuiteSparse/4.5.6-intel-2019b-METIS-5.1.0
      5) baselibs/2019b-GCCcore-8.3.0  13) Python/3.7.4-intel-2019b
      6) Tcl/8.6.9-intel-2019b         14) git/2.13.3
      7) X11/2019b-GCCcore-8.3.0       15) CMake/3.11.1
      8) Tk/8.6.9-intel-2019b
    Virtual environment present: '.venv'
    Activating '.venv' ...
    (.venv) >

This :file:`micc-setup` script work for every project, but the modules loaded are
hardcoded. You can of course elaborate on this very simple script.

7.2 Using a micc_ project as a dependency
-----------------------------------------
To use a micc_ project such as ET-dot in an other project, say *foo*, is simple. Create a
virtual environment in *foo* and use ``pip install``. Using the micc-setup script whe
wrote before::

    > cd path/to/foo
    > source micc-setup

    The following have been reloaded with a version change:
      1) leibniz/supported => leibniz/2019b


    Currently Loaded Modules:
      1) leibniz/2019b
      2) GCCcore/8.3.0
      3) binutils/2.32-GCCcore-8.3.0
      4) intel/2019b
      5) baselibs/2019b-GCCcore-8.3.0
      6) Tcl/8.6.9-intel-2019b
      7) X11/2019b-GCCcore-8.3.0
      8) Tk/8.6.9-intel-2019b
      9) SQLite/3.29.0-intel-2019b
     10) HDF5/1.8.21-intel-2019b-MPI
     11) METIS/5.1.0-intel-2019b-i32-fp64
     12) SuiteSparse/4.5.6-intel-2019b-METIS-5.1.0
     13) Python/3.7.4-intel-2019b
     14) git/2.13.3
     15) CMake/3.11.1
    Creating  new virtual environment '.venv'
    Activating '.venv' ...
    Installing micc ...
    Collecting et-micc
      ...
    (.venv) > pip install git+https://github.com/etijskens/ET-dot
    Collecting git+https://github.com/etijskens/ET-dot
      Cloning https://github.com/etijskens/ET-dot to /tmp/pip-req-build-i1ta63e3
      Installing build dependencies ... done
      Getting requirements to build wheel ... done
      Installing backend dependencies ... done
        Preparing wheel metadata ... done
    Collecting et-micc-build<0.11.0,>=0.10.10 (from et-dot==1.0.0)
      ...

Note that we installed *ET-dot* directly from github_. If we had published it to
PyPi_, ``pip install ET-dot`` would have been sufficient.

7.2.1 Using virtual environments in batch jobs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Using project *foo* in a batch job is exactly the same as on the command line. You
must load the cluster modules you need, and activate the environment. Here is an example
(PBS) job script, assuming that foo.py is a python script that imports :py:mod:`et_dot` ::

    #!/usr/bin/env bash
    #PBS -l nodes=1:ppn=1
    #PBS -l walltime=00:05:00
    #PBS -l pmem=1gb

    cd $VSC_DATA/path/to/foo
    # load necessary cluster modules and activate virtual environment
    source micc-setup
    # run python script
    python foo.py

7.3 Using conda Python distributions
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

Now set the ``PYTHONPATH`` environment variable ot the :file:`.cenv` directory and export it::

    > export PYTHONPATH=$PWD/.cenv

.. note:: The ``PYTHONPATH`` environment variable is retained for the duration of the terminal
    session.

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

