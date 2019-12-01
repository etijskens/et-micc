Tutorial 5 - Publishing your code
=================================
Publishing your code is an easy way to make your code available to other users.

5.1 Publishing to the Python Package Index
------------------------------------------
For this we rely on poetry_. If you do not have a PyPI_  account, create one and 
run this command in your project directory, e.g. :file:`et-foo`:

.. code-block::

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
      your project name is not already taken.
   #. immediately after your project is created, you publish it, as to reserve the
      name forever.

Now everyone can install the package in his current Python environment as::

   > pip install et-foo



5.2 Publishing packages with binary extension modules
-----------------------------------------------------
Packages with binary extension modules are published in exactly the same way. When Micc_
adds a binary extension module it adds a dependency on micc-build_. The binary extensions
are then build locally by running::

    (.venv) > micc-build

