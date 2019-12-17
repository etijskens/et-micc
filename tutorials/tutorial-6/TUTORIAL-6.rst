Tutorial 6 - Using micc projects on the VSC-clusters
====================================================

We distinguish to cases:

* installing a micc_-project for further development, and
* installing a micc_project (in a virtual environment) for use in production runs.

.. note:: This tutorial uses the Leibniz cluster of the University of Antwerp as an
    example. The principles pertain, however, to all VSC clusters, and most probably
    also to other clusters using a module system for exposing its software stack.

6.1 Micc use on the cluster for developing code
----------------------------------------------------

Most differences between using  your local machine and using the cluster stem from
the fact that the cluster uses a *module* system for making software available to the
user, and less importantly, that the cluster uses scheduler to run your compute jobs
in batch mode.

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

When you load the git module you get version 2.13.2::

    > module load git
    > which git
    /apps/antwerpen/broadwell/centos7/git/2.13.3/bin/git

Though this is not the very latest git version, but it is definitely way ahead of 1.8.3.1.
Moreover, both versions differ in the major component of the version, which indicates that
they are not backward compatible.

As git is now available, we can clone the git repository of our ET-dot project in some
workspace directory (preferably somewhere on $VSC_DATA) and ``cd`` into the project
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

.. note:: It is good practice to **clone git repositories in $VSC_DATA** . Doing this in
    $VSC_HOME can easily consume all your file quota, and $VSC_SCRATCH is not backed up.

You might also load CMake if you want to build binary extension modules from C++ source code:

    > module load CMake

On our local machine we would now select a python version with pyenv_, and run
``poetry install`` to create a virtual environment and install :py:mod:`ET-dot`'s
dependencies. The pyenv_ part is again replaced by a ``module load`` command, e.g.::

    > module load leibniz/2019b
    > module load Python/3.7.4-intel-2019b

The first command selects all modules built with the Intel 2019b toolchain, and
the second makes Python 3.7.4 available together with a whole bunch of pre-installed
Python packages which are useful for high performance computing, such as numpy_, as
well as all the dependencies of these HPC modules. To see them execute::

    > pip list
    Package            Version
    ------------------ ------------
    absl-py            0.7.1
    alabaster          0.7.12
    appdirs            1.4.3
    ...
    numpy              1.17.0
    ...

The poetry_ part, requires - at least at the time of writing - some special attention.

6.1.1 Note about using Poetry on the cluster
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
which they will run. Typical examples are Numpy_, Scipy_, Pandas_, ... ``Poetry install``
will install equally functional packages which are built for running on many different
hardwares, rather for optimal performance. By using ``poetry install`` performances will
be sacrificed. In addition, re-installing these packages consume a lot of your file quota.

To avoid trouble, we thus recommend to **not** install poetry_ on the cluster. If you
want to publish your package, ``commit`` the changes to the git repository, ``push`` them
to github_, fetch the latest version on your local machine and use ``poetry publish --build``
to publish.

6.1.2 Virtual environments and dependencies on the cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If we can't use Poetry_, we need some alternative way of creating virtual environments,
and installing dependencies.

Creating a virtual environment in the project root directory is simple::

    > python -m venv .venv --system-site-packages

This command uses the :py:mod:`venv` package to create a virtual environment named `.venv`.
The --system-site-packages ensures that the virtual environment also sees all the pre-installed
Python packages. The environment name is in fact arbitrary, but we choose to use the same
name as Poetry_ would use. The environment name is also the name of the directory containing
the virtual environment::

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

As on our local machine the command prompt is modified to notify you which virtual
environment is activated.

To install the dependencies needed by the ET-dot project, we have two options,
a quick and dirty approach and a systematic approach. The systematic approach consists
of checking the project's :file:`pyproject.toml` file::

    (.venv) > cat pyproject.toml
    [tool.poetry]
    name = "ET-dot"
    version = "1.0.0"
    description = "<Enter a one-sentence description of this project here.>"
    authors = ["Engelbert Tijskens <engelbert.tijskens@uantwerpen.be>"]
    license = "MIT"

    readme = 'README.rst'

    repository = "https://github.com/etijskens/ET-dot"
    homepage = "https://github.com/etijskens/ET-dot"

    keywords = ['packaging', 'poetry']

    [tool.poetry.dependencies]
    python = "^3.7"
    et-micc-build = "^0.10.10"

    [tool.poetry.dev-dependencies]
    pytest = "^4.4.2"

    [tool.poetry.scripts]

    [build-system]
    requires = ["poetry>=0.12"]
    build-backend = "poetry.masonry.api"

The section ``[tool.poetry.dependencies]`` tells us that the our project depends on
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

Except for some ``DeprecationWarning``s which are out of our reach, all tests succeed. Note,
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

If the project needs other packages, you would continue to have :py:exc:`ModuleNotFoundError`s.
Each time you] ``pip install`` the missing package, and run the test until no more
:py:exc:`ModuleNotFoundError`s arise and you are good to go.

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


Using conda Python distributions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
`Conda <https://conda.io/en/latest/>`_ Python distributions have there own way of creating and
managing virtual environments (see
`Conda tasks <https://conda.io/projects/conda/en/latest/user-guide/tasks/index.html>`_). Just as
above you must create a conda virtual environment, activate it and install the Python packages you
need in that virtual environment.

...

As, at the time of writing, Poetry_ is not playing well with conda virtual environments, your are
advised not to install poetry_, to avoid problems.

