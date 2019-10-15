Adding a Python module
======================

Just as one can add binary extension modules to a package, one can add python modules.

.. code-block:: bash

   > micc module foo 
   
   [INFO]           [ Creating python module foo.py in Python package ET-dot.
   [INFO]               - python source in    ET-doc/et_doc/foo.py.
   [INFO]               - Python test code in ET-doc/tests/test_foo.py.
   [INFO]           ] done.

This adds a Python sub-module to the package, and a test script. The documentation 
for the sub-module is extracted from doc-strings of the functions and classes in 
the sub-module.   

As with ``micc create`` the default structure is that of a simple module, i.e. 
:file:`ET-doc/et_doc/foo.py`. If you want a package you can add the ``--package``
flag.

Adding a Python Command Line Interface
======================================
*Command Line Interface*s are Python scripts that you want to be installed as 
executable programs when a user installs your package.

As an example, assume that we need quite often to read two arrays from file and
compute their dot product, and that we want to execute this operation as:

.. code-block:: bash

   > dot-files file1 file2
   dot(file1,file2) = 123.456
   > 
   
Micc_ supports two kinds of CLIs based on click_, a very practical tool for building 
Python CLIs. The first one is for CLIs that execute a single task, the second one for
a command with sub-commands, like git_ or micc_ itself.




