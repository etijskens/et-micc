.. _tutorial-5:

Tutorial 5 - Publishing your code
=================================
Publishing your code is an easy way to make your code available to other users.

5.1 Publishing to the Python Package Index
------------------------------------------
Poetry_ provides really easy interface to publishing your code to the Python Package
Index (PyPI_). If you do not have a PyPI_  account, create one and
run this command in a project directory, say :file:`et-foo`::

   > cd path/to/et-foo
   > source .venv/bin/activate
   (.venv) > poetry publish --build
   Building et-foo (0.1.0)
    - Building sdist
    - Built et-foo-0.1.0.tar.gz
   
    - Building wheel
    - Built et_foo-0.1.0-py3-none-any.whl

   Publishing et-foo (0.1.0) to PyPI
   Username: etijskens
   Password:
   
    - Uploading et-foo-0.1.0.tar.gz 100%
    - Uploading et_foo-0.1.0-py3-none-any.whl 100%

    
.. note:: It is crucial that your project name is not already taken. For this reason,
   we recommend that

   #. before you create a project that you might want to publish, you check wether
      your project name is not already taken. This is easily done by adding the
      ``--publish`` flag when creating a project. If the name is taken you get a
      warning and the project is not created.
   #. immediately after your project is created, you publish the empty, as to reserve
      the name forever.

After the project is published, everyone can install the package in his current Python
environment as::

    > pip install et-foo
    ...

5.2 Publishing packages with binary extension modules
-----------------------------------------------------
Packages with binary extension modules are published in exactly the same way. That is,
perhaps surprisingly, as a Python-only project. When you ``pip install`` a Micc_ project
the package directory will end up in the :file:`site-packages` directory of the Python
environment in which you install. The source code directories of the binary extensions
modules are installed with the package, but without the binary extensions themselves.
These must be compiled locally. Fortunately that happens automatically, at least if the
binary extension were added to the package by Micc_. When Micc_ adds a binary extension
to a project, two things happen:

* a dependency on micc-build_ is added to the project, and
* in the top-level module :py:mod:`<package_name>/__init__.py` a :py:obj:`try-except`
  block is added that tries to import the binary extension and in case of failure
  (:py:exc:`ModuleNotFoundError`) will attempt to build it using the machinery provided
  by micc-build_. This will usually succeed, provided the necessary compilers are available
  and there are no syntax errors.

As an example, let us create a project *foo* with a binary extension module *bar* written
in C++

.. code-block:: bash

   > micc -p Foo create
   > cd Foo
   > micc add bar --cpp

This creates this :file:`Foo/foo/__init__.py`:

.. code-block:: python

   # -*- coding: utf-8 -*-
   """
   Package foo
   ===========

   Top-level package for foo.
   """

   __version__ = 0.0.0

   try:
       import foo.bar
   except ModuleNotFoundError as e:
       # Try to build this binary extension:
       from pathlib import Path
       import click
       from et_micc_build.cli_micc_build import auto_build_binary_extension
       msg = auto_build_binary_extension(Path(__file__).parent, 'bar')
       if not msg:
           import foo.bar
       else:
           click.secho(msg, fg='bright_red')

   def hello(who='world'):
       ...

If the first ``import foo.bar`` fails, the ``except`` block imports the method
:py:meth:`auto_build_binary_extension` and executes it to build the binary extension
module :py:mod:`bar`. If the build succeeds, the :py:obj:`msg` string is empty and
:py:mod:`foo.bar` is imported at last, otherwise the error message :py:obj:`msg`
is printed.

5.4 Publishing your documentation on readthedocs.org
----------------------------------------------------
Publishing your documentation to `Readthedocs <https://readthedocs.org>`_ relieves the users of your
code from having to build documentation themselves. Making it happen is very easy. First, make sure
the git repository of your code is pushed on Github_. Second, create a Readthedocs_ account if you
do not already have one. Then, go to your Readthedocs_ page, go to *your projects* and hit import
project. After filling in the fields, the documentation will be rebuild automatically and published
every time you push your code to the Github_ remote repository.

.. note:: Sphinx must be able to import your project in order to extract the documentation.
    If your codes depend on Python modules other than the standard library, this will fail and
    the documentation will not be built. You can add the necessary dependencies to
    :file:`<your-project>/docs/requirements.txt`.