Tutorial 6 - Using micc on the VSC-clusters
===========================================

As Micc_ is a command line tool, using micc on the VSC-clusters isn't too different
from using it on your local machine. However, on the VSC-clusters, e.g. *Leibniz*,
installation of software components is organized with the
`module <https://vscentrum.be/???>`_ system, so:

*   You can't manage your Python versions with pyenv_.
*   You must execute::

        > module load <some_python_version>

    to have a useful Python executable on your PATH. Note that the sytem Python
    is most definitely **not* fit for HPC purposes.
*   You can install pipx_ in your ``$VSC_USER`` or ``$VSC_DATA`` partition.

    todo: verify and document

*   You can use pipx_ to install micc_

    todo: document

*   Building documentation on the cluster is not very useful - as it cannot be
    viewed anyway - and should be avoided.

*   It is recommended to create a virtualenv


**test effect of removing poetry.lock***

6.1 Micc use on the cluster for developing code
----------------------------------------------------

All differences between using micc_ on your local machine and on the cluster stem from
the fact that the cluster uses a *module* system for making software available to the
user. Most tools that you want to use on the cluster should be selected through ``module``
commands (see
`Using the module system <https://vlaams-supercomputing-centrum-vscdocumentation.readthedocs-hosted.com/en/latest/software/software_stack.html#using-the-module-system>`_).
Although the operating system also exposes some tools such as compilers, as they
are many versions behind and, consequentially, they are **not** fit for high performance
computing. As an example consider the ``git`` command. It is expose by the operating system::

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

When working on our local machine, we would now select a Python version for the
project, e.g.::

    > pyenv local 3.7.5      # on your local machine

On the cluster, however we must select the python version you want to develop for among
the available Python cluster modules. If you are not familiar with the use of cluster
modules, you might want to consult `Using the module system`_. Below we use Python 3.7.4,
which is close to the 3.7.5 we use on our local machine::

    > module load leibniz/2019b             # use the intel-2019b toolchain
    > module load Python/3.7.4-intel-2019b
    > which python
    /apps/antwerpen/broadwell/centos7/Python/3.7.4-intel-2019b/bin/python
    > python --version
    Python 3.7.4

.. note:: As at the time of writing poetry_ doesn't play well with conda Python distributions,
    we are need to leave any conda Python distributions aside, *if* (and only if) we insist on
    using poetry_. This includes the Intel Python distribytions, which are also based on conda.

You might also load CMake if you want to build binary extension
modules from C++ source code:

    > module load CMake

Note that, in  general, loading a python cluster module (c.q. ``Python/3.7.4-intel-2019b``),
is not exactly comparable to what we achieve by selecting a python version with
``pyenv local 3.7.5`` on our local machine. The cluster module comes with a list of
pre-installed Python packages, which you can list by running::

    > pip list
    Package            Version
    ------------------ ------------
    absl-py                       0.7.1
    alabaster                     0.7.12
    appdirs                       1.4.3
    ...
    Click              7.0
    ...
    numpy              1.17.0
    ...
    pytest             5.0.1
    ...

Most of them are rather uninteresting because they are dependencies of other pre-installed
packages. Three of these pre-installed packages we have used already during our work with
micc_: Numpy_, Click_ and pytest_. We do not want to reinstall these modules for two reasons:

#.  That would be a waste of disk space and your file quota, and
#.  Number crunching modules like Numpy_ are built for High Performance Computing and compiler
    options have been selected with care as to squeeze out the last bit of performance of
    the hardware you will be running your code on.

That complicates our work with Micc_ a bit. On our local machine we could simply run
``poetry install`` to create a virtual environment and install all its dependencies. On the
cluster there are dependencies we do not want to install, for the two reasons above.

There are several ways to deal with this. If we insist on using Poetry_, we must refine the
dependencies requirements in a way that they are consistent with what the cluster environment
offers. That is certainly not impossible, but it can easily become overly complicated, when you
need to deal with various cluster environments. The easiest way - though mayb a bit quick and
dirty - is to create and manage the virtual environment yourself.


6.1.1 Quick and dirty approach
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Create a virtual environment ``.venv`` in the project root directory and activate it::

    > cd ET-dot
    > python -m venv .venv --system-site-packages
    > . .venv/bin/activate
    (.venv) >

The ``--system-site-packages`` flag ensures that the system site packages, i.e. the
pre-installed packages, are seen by the virtual environment. Let us see if we can run
the test script to find out if our environment is complete.

    > python -m pytest

Note that we need to run pytest_ as ``python -m pytest`` to make it see our virtual
environment. Just running ``pytest`` would not find our :py:mod:`et_dot`. Here is the
output::

    ============================================ test session starts =============================================
    platform linux -- Python 3.7.4, pytest-5.0.1, py-1.8.0, pluggy-0.12.0
    rootdir: /data/antwerpen/201/vsc20170/workspace/ET-dot
    plugins: xonsh-0.9.9
    collected 0 items / 3 errors

    =================================================== ERRORS ===================================================
    __________________________________ ERROR collecting tests/test_cpp_dotc.py ___________________________________
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
    ___________________________________ ERROR collecting tests/test_et_dot.py ____________________________________
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
    __________________________________ ERROR collecting tests/test_f2py_dotf.py __________________________________
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
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ========================================== 3 error in 0.35 seconds ===========================================


All three tests fail in more or less the same way. E.g in the last test there is first
a :py:exc:`ModuleNotFoundError`::

    E   ModuleNotFoundError: No module named 'et_dot.dotc'

which tells us that the binary extension :py:mod:`dotc` is not found. This is logical
because it hasn't been built. (You can verify that there are no :file:`.so` files by
running ``ls -l et_dot``.) The auto-build feature should normally take care of that.
The error gives rise to another :py:exc:`ModuleNotFoundError`::

    E   ModuleNotFoundError: No module named 'et_micc_build'

which tells us that micc-build_ is not installed in our virtual environment, which is
indeed necessary for engaging the auto-build feature. So we install it::

    (.venv) > pip install et-micc-build
    Collecting et-micc-build
    ...
    Requirement already satisfied: numpy<2.0.0,>=1.17.0 in /apps/antwerpen/broadwell/centos7/Python/3.7.4-intel-2019b/lib/python3.7/site-packages/numpy-1.17.0-py3.7-linux-x86_64.egg (from et-micc-build) (1.17.0)
    ...
    Requirement already satisfied: click<8.0,>=7.0 in /apps/antwerpen/broadwell/centos7/Python/3.7.4-intel-2019b/lib/python3.7/site-packages/Click-7.0-py3.7.egg (from et-micc==0.10.10->et-micc-build) (7.0)(.venv) >
    ...

As you can see micc-build_ depends on numpy_ and Click_, but pip finds these packages in
the pre-installed system site packages, and does noet reinstall them. This is exactly the
behavior we were looking for.

Next, we run the tests again::

    > python -m pytest
    ============================================ test session starts =============================================
    platform linux -- Python 3.7.4, pytest-5.0.1, py-1.8.0, pluggy-0.12.0
    rootdir: /data/antwerpen/201/vsc20170/workspace/ET-dot
    plugins: xonsh-0.9.9
    collected 9 items

    tests/test_cpp_dotc.py .                                                                               [ 11%]
    tests/test_et_dot.py .......                                                                           [ 88%]
    tests/test_f2py_dotf.py .                                                                              [100%]

    ============================================== warnings summary ==============================================
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
    ==================================== 9 passed, 4 warnings in 9.89 seconds ====================================

This time all tests succeed, implying that the auto-build feature has done its work. If your code
needs other packages, you will continue to have :py:exc:`ModuleNotFoundError`s. Each time you
``pip install`` the missing package, and run the test until no more :py:exc:`ModuleNotFoundError`s
arise.

THe output does show a number of :py:obj:`DeprecationWarning`s. These tell you that some
dependencies of the code use deprecated constructs, which may disappear in future releases.
They are certainly not an imminent treat to our code. Since you are not the maintainer of
those packages, you cannot do anything about the, and must hope that the maintainers do fix
this in time.

This is a simple and quick approach to get your environment ready to run the code without
:py:exc:`ModuleNotFoundError`s. It is working most of the time. Sometimes, however, you will
need to install a specific version of a packages, because the latest version has bugs,
or because it broke backward compatibility. This can be achieved as::

    > pip install package_needed==version_string

What about Poetry_? We used poetry_ on our local machine only for virtual environment and
dependency management, using the commands ``poetry install``, ``poetry update``, ``poetry add``
and ``poetry remove``, and for publishing to PyPi_, with command ``poetry publish``. Since on
the cluster we did the virtual environment and dependency management manually, and pubishing is
easily performed on our local machine, doing without poetry_ on the cluster is not too much of
a problem.

If we plan on continuing the development of the ET-dot package on the cluster, having micc_
available might come in handy. We can just install it with pip_. Perhaps to your surprise,
it already is::

    (.venv) > pip install et-micc
    Requirement already satisfied: et-micc in ./.venv/lib/python3.7/site-packages (0.10.10)
    ...

The reason is simply that micc_ is a dependency of micc-build_, which we installed to build
the binary extension modules :py:mod:`dotf` and :py:mod:`dotc`, and as a consequence it was
installed with micc-build_.

It is important to note how the approach is different from using micc_ on your local
machine:

*   A cluster module is loaded to select the active Python version. A few other tools,
    such as git_ and CMake_ are made available by loading cluster modules too.
*   A virtual environment is created **manually** and activated. (we have choosen to
    locate the virtual environment in the project root directory, but that location is,
    in fact, immaterial).
*   All missing dependencies are installed **manually** with ``pip``, not with poetry_
    as this may use
*   If micc_ is not a dependency of the project, it must be manually installed in the
    project's virtual environment

*   Poetry_ is installed in this virtual environment and used to install the project's
    dependencies by running ``poetry install``.
The procedure can be easily put into a bash script :file:`micc-setup`, and stored in
some directory which is on your PATH::

    #!/bin/bash
    # this is file micc-setup
    # load the modules needed
    module load leibniz/2019b
    module load Python/3.7.4-intel-2019b
    module load git
    module load CMake
    module list

    if [ -d  ".venv" ]
    then
        echo "Virtual environment present: .venv"
        source .venv/bin/activate
    else
        # create new virtual environment
        python -m venv .venv --system-site-packages
        source .venv/bin/activate
        pip install poetry==1.0.0b9
        pip install et-micc
        poetry install
    fi

When run in the project root directory, this script loads the needed modules and
activates the project's virtual environment :file:`.venv` if it exists. Otherwise, it
will create it and install poetry_, micc_ and the dependencies of the project.
You must ``source`` this script in the project root directory. If you do not ``source`` the
script, the environment will be correctly setup, but the virtual environment will not be
activated when after the script terminates, nor will the modules be loaded.

This :file:`micc-setup` script work for every project, but the modules loaded are
hardcoded.


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

