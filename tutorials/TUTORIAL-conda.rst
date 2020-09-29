Tutorial 6 - Anaconda Python distributions
==========================================

.. warning::

   This subject hasn't settled. There are unresolved issues for using IntelPython modules on
   the cluster

This tutorial is about using micc_ with `Anaconda Python distributions <https://www.anaconda.com>`_.

Here are some reasons to use `Anaconda Python distributions`_:

* Anaconda is popular because it brings many of the tools used in data science and machine
  learning with just one install, so it’s great for having a short and simple setup.

* Some Python packages provided by conda are optimized for performance, e.g. Numpy is using
  Intel MKL (Math Kernel Library) for some of its functionality.

* Then there is the Intel Python distribution which also uses conda. It provides highly
  performance optimized packages.

.. warning::

   Poetry_ works well with `Anaconda Python distributions`_, provided they are installed
   in a location where you have read/write access. So, on your local machine there is no
   problem. Also on the cluster, everything works as expected as long as you are installing
   your own Anaconda Python distribution. This is, however, **NOT** recommended as the
   performance of your Anaconda Python distribution and the installed packages will be
   suboptimal and not up to HPC standards. Poetry_, at the time of writing (10/2020), does
   NOT work well with pre-installed Anaconda Python distributions, such as the Intel Python
   distribution, which is based on `conda <https://docs.conda.io/en/latest/>`_. The obvious
   workaround is to manually create a virtual conda environment and use ``conda install package``
   (or ``pip install package`` if package is not available as a conda package. However, for
   some obscure reason ``pip install`` refuses to install in the activated virtual environment,
   and instead aborts trying to install into the module path where the user has no write access.

6.1 Installing an Anaconda Python distribution
----------------------------------------------
**Not recommended on the cluster**

To install an Anaconda Python distribution follow the instructions at
https://docs.conda.io/projects/conda/en/latest/user-guide/install. We do not recommend
the installation of a complete Anaconda Python distribution, as this takes up a lot of
disk space with packages you will never use. Instead, install
`Miniconda <https://docs.conda.io/projects/conda/en/latest/glossary.html#miniconda-glossary>`_,
a minimal Python distribution with only a few indispensable packages. You can add the
packages you need to the distribution itself, or to any virtual environment based on it,
using ``conda install``.

6.2 Manually creating a virtual conda environment
-------------------------------------------------

The `Intel  distribution for Python <https://software.intel.com/content/www/us/en/develop/tools/distribution-for-python.html>`_ is based on `conda <https://docs.conda.io/en/latest/>`_
is in fact an Anaconda Python distribution optimised by Intel engineers for HPC purposes.
It is  pre-installed on the cluster as module IntelPython3.
To use it with on the cluster with micc_, we need ::

    > module load leibniz/2020a      # toolchain selection
    > module load IntelPython3/2020a
    > module load intel/2019b
    > module load CMake
    > module load git
    > python --version
    Python 3.7.7 :: Intel(R) Corporation

We first ``cd`` into our project directory::

    > cd path/to/ET-dot

Conda Python distributions have their own way of creating and managing virtual environments
but the principle is the same
(see`Conda tasks <https://conda.io/projects/conda/en/latest/user-guide/tasks/index.html>`_).
We can now create a virtual conda environment. We choose a different name :file:`.cenv37`, so it
can live next an other virtual environment::

    > conda create -p ./.cenv37 python=3.7
    > conda init bash                # only first time
    > source ~/.bashrc               # only first time
    > module load leibniz/2020a      # we must reload our modules
    > module load IntelPython3/2020a
    > module load intel/2019b
    > module load CMake
    > module load git
    > python --version
    Python 3.7.7 :: Intel(R) Corporation

The name chosen is arbitrary of course, but it resembles the .venv we got (by default) with
poetry_, and the ``37`` is to distinguish different environments for different Python
versions. In fact, also the location, which was specified with ``-p ./.cenv37`` is arbitrary,
but the project root directory is a familiar place for this and compliant with our earlier
approach using virtual environments created with ``poetry install``. Alternatively, you might
want to use the environment for other projects too, in which case you might locate it in a
different place.

This is the output generated::

    Collecting package metadata (current_repodata.json): done
    Solving environment: done

    ## Package Plan ##

      environment location: /scratch/antwerpen/201/vsc20170/et-dot/.cenv37

      added / updated specs:
        - python=3.7


    The following NEW packages will be INSTALLED:

      _libgcc_mutex      pkgs/main/linux-64::_libgcc_mutex-0.1-main
      ca-certificates    pkgs/main/linux-64::ca-certificates-2020.7.22-0
      certifi            pkgs/main/linux-64::certifi-2020.6.20-py37_0
      ld_impl_linux-64   pkgs/main/linux-64::ld_impl_linux-64-2.33.1-h53a641e_7
      libedit            pkgs/main/linux-64::libedit-3.1.20191231-h14c3975_1
      libffi             pkgs/main/linux-64::libffi-3.3-he6710b0_2
      libgcc-ng          pkgs/main/linux-64::libgcc-ng-9.1.0-hdf63c60_0
      libstdcxx-ng       pkgs/main/linux-64::libstdcxx-ng-9.1.0-hdf63c60_0
      ncurses            pkgs/main/linux-64::ncurses-6.2-he6710b0_1
      openssl            pkgs/main/linux-64::openssl-1.1.1h-h7b6447c_0
      pip                pkgs/main/linux-64::pip-20.2.2-py37_0
      python             pkgs/main/linux-64::python-3.7.9-h7579374_0
      readline           pkgs/main/linux-64::readline-8.0-h7b6447c_0
      setuptools         pkgs/main/linux-64::setuptools-49.6.0-py37_1
      sqlite             pkgs/main/linux-64::sqlite-3.33.0-h62c20be_0
      tk                 pkgs/main/linux-64::tk-8.6.10-hbc83047_0
      wheel              pkgs/main/noarch::wheel-0.35.1-py_0
      xz                 pkgs/main/linux-64::xz-5.2.5-h7b6447c_0
      zlib               pkgs/main/linux-64::zlib-1.2.11-h7b6447c_3

    Proceed ([y]/n)? y

    Preparing transaction: done
    Verifying transaction: done
    Executing transaction: done
    #
    # To activate this environment, use
    #
    #     $ conda activate /scratch/antwerpen/201/vsc20170/et-dot/.cenv37
    #
    # To deactivate an active environment, use
    #
    #     $ conda deactivate

We must install dependencies ourselves::

    > conda install pytest
    ...
There is no conda installer for micc_, so, we must ``pip install it``::

    > pip install micc

As mentioned at the end, we can activate the environment with the command::

    > conda activate /Users/etijskens/software/dev/ET-dot/.cenv37
    > (/Users/etijskens/software/dev/ET-dot/.cenv37)

.. note::
    The command ``conda activate .cenv37/`` would have worked too, but not
    ``conda activate .cenv37``, as ``conda`` will consider ``.cenv37`` to be
    a named environment (an environment created with ``conda create --name <envname>``
    and look it up in its default directory.

Conda provides hundreds of popular packages, which are often better optimised than the
general purpose packages on PyPI_. You install them using conda install::

    > conda install numpy
    Collecting package metadata (current_repodata.json): done
    Solving environment: done

    ## Package Plan ##

      environment location: /Users/etijskens/software/dev/workspace/ET-dot/.cenv37

      added / updated specs:
        - numpy


    The following NEW packages will be INSTALLED:

      blas               pkgs/main/osx-64::blas-1.0-mkl
      intel-openmp       pkgs/main/osx-64::intel-openmp-2019.4-233
      libgfortran        pkgs/main/osx-64::libgfortran-3.0.1-h93005f0_2
      mkl                pkgs/main/osx-64::mkl-2019.4-233
      mkl-service        pkgs/main/osx-64::mkl-service-2.3.0-py37hfbe908c_0
      mkl_fft            pkgs/main/osx-64::mkl_fft-1.0.15-py37h5e564d8_0
      mkl_random         pkgs/main/osx-64::mkl_random-1.1.0-py37ha771720_0
      numpy              pkgs/main/osx-64::numpy-1.17.4-py37h890c691_0
      numpy-base         pkgs/main/osx-64::numpy-base-1.17.4-py37h6575580_0
      six                pkgs/main/osx-64::six-1.13.0-py37_0


    Proceed ([y]/n)? y

    Preparing transaction: done
    Verifying transaction: done
    Executing transaction: done

Clearly, this numpy adds some performance optimized components from Intel like  blas,
intel-openmp, mkl etc. It is important to use ``conda install`` for such packages as
``pip install`` or ``poetry install`` would install different a different Numpy.

Finally, we run ``poetry install`` to install the remaining dependencies (we remove
:file:`poetry.lock` to allow poetry to choose the most recent version)::

    (/Users/etijskens/software/dev/workspace/ET-dot/.cenv37) > rm poetry.lock
    (/Users/etijskens/software/dev/workspace/ET-dot/.cenv37) > poetry install
    Updating dependencies
    Resolving dependencies... (2.4s)

    Writing lock file


    Package operations: 49 installs, 0 updates, 0 removals

      - Installing chardet (3.0.4)
      - Installing idna (2.8)
      - Installing markupsafe (1.1.1)
      - Installing pyparsing (2.4.5)
      - Installing python-dateutil (2.8.1)
      - Installing pytz (2019.3)
      - Installing urllib3 (1.25.7)
      - Installing alabaster (0.7.12)
      - Installing arrow (0.15.4)
      - Installing babel (2.7.0)
      - Installing docutils (0.15.2)
      - Installing imagesize (1.1.0)
      - Installing jinja2 (2.10.3)
      - Installing more-itertools (8.0.2)
      - Installing packaging (19.2)
      - Installing pygments (2.5.2)
      - Installing requests (2.22.0)
      - Installing snowballstemmer (2.0.0)
      - Installing sphinxcontrib-applehelp (1.0.1)
      - Installing sphinxcontrib-devhelp (1.0.1)
      - Installing sphinxcontrib-htmlhelp (1.0.2)
      - Installing sphinxcontrib-jsmath (1.0.1)
      - Installing sphinxcontrib-qthelp (1.0.2)
      - Installing sphinxcontrib-serializinghtml (1.1.3)
      - Installing binaryornot (0.4.4)
      - Installing click (7.0)
      - Installing future (0.18.2)
      - Installing jinja2-time (0.2.0)
      - Installing pbr (5.4.4)
      - Installing poyo (0.5.0)
      - Installing sphinx (2.3.0)
      - Installing whichcraft (0.6.1)
      - Installing zipp (0.6.0)
      - Installing cookiecutter (1.6.0)
      - Installing importlib-metadata (1.3.0)
      - Installing semantic-version (2.8.3)
      - Installing sphinx-click (2.3.1)
      - Installing sphinx-rtd-theme (0.4.3)
      - Installing tomlkit (0.5.8)
      - Installing walkdir (0.4.1)
      - Installing atomicwrites (1.3.0)
      - Installing attrs (19.3.0)
      - Installing et-micc (0.10.13)
      - Installing pluggy (0.13.1)
      - Installing py (1.8.0)
      - Installing pybind11 (2.4.3)
      - Installing wcwidth (0.1.7)
      - Installing et-micc-build (0.10.13)
      - Installing pytest (4.6.8)
      - Installing ET-dot (1.0.0)

Clearly, Numpy is not in the install list. The numpy we installed with conda is still
available:

    (/Users/etijskens/software/dev/workspace/ET-dot/.cenv37) > conda list
    # packages in environment at /Users/etijskens/software/dev/workspace/ET-dot/.cenv37:
    #
    # Name                    Version                   Build  Channel
    ...
    et-dot                    1.0.0                     dev_0    <develop>
    et-micc                   0.10.13                  pypi_0    pypi
    et-micc-build             0.10.13                  pypi_0    pypi
    ...
    intel-openmp              2019.4                      233
    ...
    libgfortran               3.0.1                h93005f0_2
    ...
    mkl                       2019.4                      233
    mkl-service               2.3.0            py37hfbe908c_0
    mkl_fft                   1.0.15           py37h5e564d8_0
    mkl_random                1.1.0            py37ha771720_0
    ...
    numpy                     1.17.4           py37h890c691_0
    numpy-base                1.17.4           py37h6575580_0
    ...

Notice the last Channel column, which describes from where the packages come.
The ``pypi`` entries where installed from PyPI_ during the ``poetry install``
command. The <develop> entry refers our current project ET-dot which was installed
in 'development' mode, meaning that modification to the :file:`.py` files are
immediately seen by the environment.

Run ``pytest`` to verify that everything is working fine::

    (/Users/etijskens/software/dev/workspace/ET-dot/.cenv37) > python -m pytest
    ========================================= test session starts ==========================================
    platform darwin -- Python 3.7.5, pytest-4.6.8, py-1.8.0, pluggy-0.13.1
    rootdir: /Users/etijskens/software/dev/workspace/ET-dot
    collected 9 items

    tests/test_cpp_dotc.py .                                                                         [ 11%]
    tests/test_et_dot.py .......                                                                     [ 88%]
    tests/test_f2py_dotf.py .                                                                        [100%]

    =========================================== warnings summary ===========================================
    .cenv37/lib/python3.7/site-packages/cookiecutter/repository.py:19
      /Users/etijskens/software/dev/workspace/ET-dot/.cenv37/lib/python3.7/site-packages/cookiecutter/repository.py:19: DeprecationWarning: Flags not at the start of the expression '\n(?x)\n((((git|hg)\\+)' (truncated)
        """)

    -- Docs: https://docs.pytest.org/en/latest/warnings.html
    ================================ 9 passed, 1 warnings in 23.77 seconds =================================

This was all run in a fresh ``git clone`` of *ET-dot*, without the binary extensions. That
there are no errors implies that the auto-build feature was succesfully engaged to build
the binary extensions :file:`et_dot/dotf` and :file:`et_dot/dotc`.

.. note::
    Poetry_ **always** uses `pip <https://pip.pypa.io/en/stable/>`_ for its installs, even in a conda environment.
    This may perhaps change in the future, as Poetry_ evolves, but for the time being
    it is the user's responsibility to ``conda install`` the modules he needs from the
    conda ecosystem.

6.2 Intel distribution for Python
---------------------------------
The `Intel Python <https://software.intel.com/en-us/distribution-for-python>`_ distribution
is also based on conda. It contains many popular packages for high performance computing,
data analytics, machine learning and artificial intelligence. The 2020 release announces:

*   Faster machine learning with scikit-learn key algorithms accelerated with Intel DAAL
*   Help address the needs of data scientists to harness Intel DAAL capabilities with a
    Python API using daal4py package improvements
*   Speed up pandas and NumPy with a compiler-based framework: High Performance Analytics
    Toolkit (HPAT)
*   Includes the latest TensorFlow and Caffe libraries that are optimized for Intel®
    architecture

To create a conda environment for the *Intel distribution for Python* follow these
instructions:

Cd into your project root directory::

    > cd path/to/ET-dot

and create the environment:

    > conda create -p ./.idp -c intel intelpython3_core python=3
    Collecting package metadata (current_repodata.json): done
    Solving environment: done

    ## Package Plan ##

      environment location: /Users/etijskens/software/dev/workspace/ET-dot/.idp

      added / updated specs:
        - intelpython3_core
        - python=3


    The following NEW packages will be INSTALLED:

      bzip2              intel/osx-64::bzip2-1.0.8-0
      certifi            intel/osx-64::certifi-2019.9.11-py37_0
      icc_rt             intel/osx-64::icc_rt-2020.0-intel_166
      intel-openmp       intel/osx-64::intel-openmp-2020.0-intel_166
      intelpython        intel/osx-64::intelpython-2020.0-1
      intelpython3_core  intel/osx-64::intelpython3_core-2020.0-0
      libffi             intel/osx-64::libffi-3.2.1-11
      mkl                intel/osx-64::mkl-2020.0-intel_166
      mkl-service        intel/osx-64::mkl-service-2.3.0-py37_0
      mkl_fft            intel/osx-64::mkl_fft-1.0.15-py37ha68da19_3
      mkl_random         intel/osx-64::mkl_random-1.1.0-py37ha68da19_0
      numpy              intel/osx-64::numpy-1.17.4-py37ha68da19_4
      numpy-base         intel/osx-64::numpy-base-1.17.4-py37_4
      openssl            intel/osx-64::openssl-1.1.1d-0
      pip                intel/osx-64::pip-19.1.1-py37_0
      python             intel/osx-64::python-3.7.4-3
      pyyaml             intel/osx-64::pyyaml-5.1.1-py37_0
      scipy              intel/osx-64::scipy-1.3.2-py37ha68da19_0
      setuptools         intel/osx-64::setuptools-41.0.1-py37_0
      six                intel/osx-64::six-1.12.0-py37_0
      sqlite             intel/osx-64::sqlite-3.29.0-0
      tbb                intel/osx-64::tbb-2020.0-intel_166
      tbb4py             intel/osx-64::tbb4py-2020.0-py37_intel_0
      tcl                intel/osx-64::tcl-8.6.4-24
      tk                 intel/osx-64::tk-8.6.4-29
      wheel              intel/osx-64::wheel-0.31.0-py37_3
      xz                 intel/osx-64::xz-5.2.4-h1de35cc_7
      yaml               intel/osx-64::yaml-0.1.7-2
      zlib               intel/osx-64::zlib-1.2.11-h1de35cc_7


    Proceed ([y]/n)? y

    Preparing transaction: done
    Verifying transaction: done
    Executing transaction: done
    #
    # To activate this environment, use
    #
    #     $ conda activate /Users/etijskens/software/dev/workspace/ET-dot/.idp
    #
    # To deactivate an active environment, use
    #
    #     $ conda deactivate

.. note::
    If you haven't installed a conda Python distribution before, the fastest way to obtain conda
    is to install
    `Miniconda <https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html>`_.

As before, you can now activate the environment::

    > conda activate .idp/
    (/Users/etijskens/software/dev/workspace/ET-dot/.idp) >

We do not recommend to use ``poetry install`` to install the project`s dependencies. (The
Intel distribution for Python, apparently, uses distutils instead of pip for its distributions,
wich causes problems). Rather, install them manually::

    (/Users/etijskens/software/dev/workspace/ET-dot/.idp) > pip install et-micc-build
    ...
    (/Users/etijskens/software/dev/workspace/ET-dot/.idp) > pip install pytest
    ...

Finally, run the tests:

    > python -m pytest
    ============================= test session starts ==============================
    platform darwin -- Python 3.7.4, pytest-5.3.2, py-1.8.0, pluggy-0.13.1
    rootdir: /Users/etijskens/software/dev/workspace/ET-dot
    collected 9 items

    tests/test_cpp_dotc.py .                                                 [ 11%]
    tests/test_et_dot.py .......                                             [ 88%]
    tests/test_f2py_dotf.py .                                                [100%]

    ============================== 9 passed in 4.50s ===============================


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

