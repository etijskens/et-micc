Tutorial 6 - Using conda Python and conda virtual environments
==============================================================

Conda_ Python distributions have there own way of creating and managing virtual environments
but the principle is the same
(see`Conda tasks <https://conda.io/projects/conda/en/latest/user-guide/tasks/index.html>`_).
Just as above you must load the necessary cluster modules, create a conda virtual environment,
activate it and install the Python packages you need in that virtual environment. First, we
select the toolchain::

    > module load leibniz/2019b
    The following have been reloaded with a version change:
      1) leibniz/supported => leibniz/2019b

Then we load an IntelPython version (which is a conda distribution optimized by Intel)::

    > module load IntelPython3/2019b.05
    > python --version
    Python 3.6.9 :: Intel Corporation

Cd to our project::

    > cd $VSC_DATA/path/to/ET-dot

Create a virtual conda environment. We choose a different name :file:`cenv`, so the two
can live next to each other::

    > conda create -p ./cenv

There is no need for a ``--system-site-packages`` flag, as that is the deault policy.
Then acitvate the virtual environment::

    > source activate /data/antwerpen/201/vsc20170/workspace/ET-dot/cenv
    (./cenv.) >




...

As, at the time of writing, Poetry_ is not playing well with conda virtual environments, your are
advised not to install poetry_, to avoid problems.

