.. highlight:: shell

.. _micc: https://micc.readthedocs.io
.. _micc-build: https://micc.readthedocs.io

************
Installation
************

It is recommended to install micc_ system-wide with `pipx <https://github.com/pipxproject/pipx>`_.

.. code-block:: console

    > pipx install et-micc
    
Upgrading to a newer version is done as:

.. code-block:: console

    > pipx upgrade et-micc

To install micc in your current Python environment, run this command in your terminal:

.. code-block:: console

    > pip install et-micc

Debugging ``micc`` and ``micc-build``
-------------------------------------
To test/debug micc_ or micc-build_ on a specific project, run:

.. code-block:: console

    (.venv)> path/to/et-micc/symlink-micc.sh

As indicated, the projects virtual environmentmust be activated. The current working
directory is immaterial, though. This command replaces the package folders ``et_micc``
and ``et_micc_build`` in the projects virtual environment's ``site-packages`` folder
with symbolic links to the project module directories ``et-micc/et_micc`` and
``et-micc-build/et_micc_build``, so that any changes in those are immediately visible
in the project your are working on.

If the project's virtual environment does not contain the package folders, you get a
warning and the suggestion to first install them. Note, that unless micc-build_ is a
dependency of your project (because it has binary extensions), micc_ is usually not
in the ``site-packages`` folder (it is usually installed system-wide).

Productivity tip: put a symbolic link to symlink-micc.sh somewhere on the path.