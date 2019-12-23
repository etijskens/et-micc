Tutorial 6 - Using conda Python and conda virtual environments
==============================================================

This tutorial is about using micc_ with conda virtual environments on your local machine.

Here are some reasons to use conda environments:

* Anaconda is popular because it brings many of the tools used in data science and machine
  learning with just one install, so it’s great for having short and simple setup.

* Some Python packages provided by conda are optimized for performance, e.g. Numpy is using
  Intel MKL (Math Kernel Library) for some of its functionality.

* Then there is the Intel Python distribution which also uses conda. It provides highly
  performance optimized packages.

6.1 Miniconda
-------------
If you haven't installed miniconda on your local machine, you can follow the instructions
on the `miniconda installation page <https://docs.conda.io/en/latest/miniconda.html>`_.

Conda Python distributions have their own way of creating and managing virtual environments
but the principle is the same
(see`Conda tasks <https://conda.io/projects/conda/en/latest/user-guide/tasks/index.html>`_).

Cd to our project::

    > cd path/to/ET-dot

and create a virtual conda environment. We choose a different name :file:`.cenv`, so the two
can live next to each other::

    > conda create -p ./cenv37 python=3.7

The name chosen is arbitrary of course, but it resembles the .venv we got (by default) with
poetry_, and the ``37`` is to distinguish different environments for different Python
versions. In fact, also the location, which was specified with ``-p ./cenv37`` is arbitrary,
but the project root directory is a familiar place for this and compliant with our earlier
approach using virtual environments created with ``poetry install``. Alternatively, you might
want to use the environment for other projects too, in which case you might locate it in a
different place.

This is the output generated::

    Collecting package metadata (current_repodata.json): done
    Solving environment: done

    ## Package Plan ##

      environment location: /Users/etijskens/software/dev/ET-dot/.cenv37

      added / updated specs:
        - python=3.7


    The following packages will be downloaded:

        package                    |            build
        ---------------------------|-----------------
        certifi-2019.11.28         |           py37_0         156 KB
        libcxx-4.0.1               |       hcfea43d_1         947 KB
        libcxxabi-4.0.1            |       hcfea43d_1         350 KB
        libedit-3.1.20181209       |       hb402a30_0         136 KB
        libffi-3.2.1               |       h475c297_4          37 KB
        ncurses-6.1                |       h0a44026_1         732 KB
        openssl-1.1.1d             |       h1de35cc_3         3.4 MB
        pip-19.3.1                 |           py37_0         1.9 MB
        python-3.7.5               |       h359304d_0        18.1 MB
        readline-7.0               |       h1de35cc_5         316 KB
        setuptools-42.0.2          |           py37_0         645 KB
        sqlite-3.30.1              |       ha441bb4_0         2.4 MB
        tk-8.6.8                   |       ha441bb4_0         2.8 MB
        xz-5.2.4                   |       h1de35cc_4         239 KB
        zlib-1.2.11                |       h1de35cc_3          90 KB
        ------------------------------------------------------------
                                               Total:        32.1 MB

    The following NEW packages will be INSTALLED:

      ca-certificates    pkgs/main/osx-64::ca-certificates-2019.11.27-0
      certifi            pkgs/main/osx-64::certifi-2019.11.28-py37_0
      libcxx             pkgs/main/osx-64::libcxx-4.0.1-hcfea43d_1
      libcxxabi          pkgs/main/osx-64::libcxxabi-4.0.1-hcfea43d_1
      libedit            pkgs/main/osx-64::libedit-3.1.20181209-hb402a30_0
      libffi             pkgs/main/osx-64::libffi-3.2.1-h475c297_4
      ncurses            pkgs/main/osx-64::ncurses-6.1-h0a44026_1
      openssl            pkgs/main/osx-64::openssl-1.1.1d-h1de35cc_3
      pip                pkgs/main/osx-64::pip-19.3.1-py37_0
      python             pkgs/main/osx-64::python-3.7.5-h359304d_0
      readline           pkgs/main/osx-64::readline-7.0-h1de35cc_5
      setuptools         pkgs/main/osx-64::setuptools-42.0.2-py37_0
      sqlite             pkgs/main/osx-64::sqlite-3.30.1-ha441bb4_0
      tk                 pkgs/main/osx-64::tk-8.6.8-ha441bb4_0
      wheel              pkgs/main/osx-64::wheel-0.33.6-py37_0
      xz                 pkgs/main/osx-64::xz-5.2.4-h1de35cc_4
      zlib               pkgs/main/osx-64::zlib-1.2.11-h1de35cc_3


    Proceed ([y]/n)? y


    Downloading and Extracting Packages
    readline-7.0         | 316 KB    | ##################################### | 100%
    libffi-3.2.1         | 37 KB     | ##################################### | 100%
    pip-19.3.1           | 1.9 MB    | ##################################### | 100%
    sqlite-3.30.1        | 2.4 MB    | ##################################### | 100%
    zlib-1.2.11          | 90 KB     | ##################################### | 100%
    libedit-3.1.20181209 | 136 KB    | ##################################### | 100%
    xz-5.2.4             | 239 KB    | ##################################### | 100%
    setuptools-42.0.2    | 645 KB    | ##################################### | 100%
    libcxx-4.0.1         | 947 KB    | ##################################### | 100%
    tk-8.6.8             | 2.8 MB    | ##################################### | 100%
    python-3.7.5         | 18.1 MB   | ##################################### | 100%
    certifi-2019.11.28   | 156 KB    | ##################################### | 100%
    openssl-1.1.1d       | 3.4 MB    | ##################################### | 100%
    ncurses-6.1          | 732 KB    | ##################################### | 100%
    libcxxabi-4.0.1      | 350 KB    | ##################################### | 100%
    Preparing transaction: done
    Verifying transaction: done
    Executing transaction: done
    #
    # To activate this environment, use
    #
    #     $ conda activate /Users/etijskens/software/dev/ET-dot/.cenv37
    #
    # To deactivate an active environment, use
    #
    #     $ conda deactivate

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
:file:`poetsry.lock` to allow poetry to choose the most recent version)::

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
    Poetry_ **always** uses pip_ for its installs, even in a conda environment.
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

