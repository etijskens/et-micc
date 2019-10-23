Tutorial 5 - Publishing your code
=================================
Publishing your code is an easy way to make your code available to other users.

Publishing to the Python Packag Index
-------------------------------------
For this we rely on poetry_. If you do not have a PyPI_  account, create one and 
run this command in your project directory, c.q. :py:mod:`et-foo`:

.. code-block::

   > poetry publish --build
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
    
.. note:: It is crucial that your project name is not already taken.\

Now everyone can install the package in his current Python environment as::

.. code-block::

   > pip install et-foo

Unfortunately poetry_ (v0.12.17 at the time of writing) is not yet capable of 
publishing code with binary extension modules. Here is a workaround.

Workaround for publishing packages with binary extension modules
----------------------------------------------------------------
The workaround is based on a putting your code in a git_ repository and 
pushing your code onto a github_ repository. The above package :py:mod:`et-foo`
is available at https://github.com/etijskens/et-foo. Interested users can install 
the code in their current Python environment by executing the following commands:

.. code-block::

   > cd path/to/interesting/git-repos
   > git clone https://github.com/etijskens/et-foo
   > cd et-foo
   > micc build
   > make install
   > micc dev-install
   
Here, the last step can be replaced by a move/copy/symlink of all :file:`.so` files
into the directory :file:`site-packages/et_foo`. The former version has the advantage
that all changes you make to the source code are immediately available in the installed
version.

