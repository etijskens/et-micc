Tutorial 3: Adding Python components
====================================

Adding a Python module
----------------------

Just as one can add binary extension modules to a package, one can add python modules.

.. code-block:: bash

   > micc add foo --py 
   
   [INFO]           [ Adding python module foo.py to project ET-dot.
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
--------------------------------------
*Command Line Interfaces* are Python scripts that you want to be installed as 
executable programs when a user installs your package.

As an example, assume that we need quite often to read two arrays from file and
compute their dot product, and that we want to execute this operation as:

.. code-block:: bash

   > dot-files file1 file2
   dot(file1,file2) = 123.456
   > 
   
Micc_ supports two kinds of CLIs based on click_, a very practical tool for building 
Python CLIs. The first one is for CLIs that execute a single task, the second one for
a command with sub-commands, like git_ or micc_ itself. The single task case default,
so we can create it like:

.. code-block:: bash

   > micc app dot-files 
   [INFO]           [ Adding CLI dot-files without sub-commands to project ET-dot.
   [INFO]               - Python source file ET-dot/et_dot/cli_dot-files.py.
   [INFO]               - Python test code   ET-dot/tests/test_cli_dot-files.py.
   [INFO]           ] done.

For a CLI with sub-commands one should add the flag ``--sub-commands``.

The source code :file:`ET-dot/et_dot/cli_dot-files.py` should be modified as:

.. code-block:: python

   # -*- coding: utf-8 -*-
   """Command line interface dot-files (no sub-commands)."""
   
   import sys
   
   import click
   import numpy as np
   
   from et_dot.dotf import dotf
   
   @click.command()
   @click.argument('file1')
   @click.argument('file2')
   @click.option('-v', '--verbosity', count=True
                , help="The verbosity of the CLI."
                , default=1
                )
   def main(file1,file2,verbosity):
       """Command line interface dot-files.
       
       A 'hello' world CLI example.
       """
       a = np.genfromtxt(file1, dtype=np.float64, delimiter=',')
       b = np.genfromtxt(file2, dtype=np.float64, delimiter=',')
       ab = dotf(a,b)
       if verbosity>1:
           print(f"dot-files({file1},{file2}) = {ab}")
       else:
           print(ab)
   
   if __name__ == "__main__":
       sys.exit(main())  # pragma: no cover
       
Here's how to use it from the command line (without installing):

.. code-block:: bash
 
   > cat file1.txt
   1,2,3,4,5
   > cat file2.txt
   2,2,2,2,2
   > python et_dot/cli_dot_files.py file1.txt file2.txt
   30.0
   > python et_dot/cli_dot_files.py file1.txt file2.txt -vv
   dot-files(file1.txt,file2.txt) = 30.0
   
When installing this package, an executable :file:`dot-files` will be installed in 
the :file"`bin` directory of the current Python environment. The modules will be
installed in the current Python environment's site-packages as usual.

Testing CLIs is a bit more complex than testing modules, but Click_ provides some tools 
for `Testing click applications <https://click.palletsprojects.com/en/7.x/testing/>`_. 
Here is the test code:

.. code-block:: python

   #!/usr/bin/env python
   # -*- coding: utf-8 -*-
   
   from click.testing import CliRunner
   
   from et_dot.cli_dot_files import main
      
   def test_main():
       runner = CliRunner()
       result = runner.invoke(main, ['file1.txt','file2.txt'])
       print(result.output)
       ab = float(result.output[0:-1])
       assert ab==30.0
   
Finally, we run pytest_:

.. code-block:: bash

   > pytest
   ================================= test session starts =================================
   platform darwin -- Python 3.7.4, pytest-4.6.5, py-1.8.0, pluggy-0.13.0
   rootdir: /Users/etijskens/software/dev/workspace/ET-dot
   collected 10 items
   
   tests/test_cli_dot-files.py .                                                   [ 10%]
   tests/test_cpp_dotc.py .                                                        [ 20%]
   tests/test_et_dot.py .......                                                    [ 90%]
   tests/test_f2py_dotf.py .                                                       [100%]
   
   ================================== 10 passed in 0.33 seconds ==========================   

Installing packages with Python components
------------------------------------------
This is automated using ``make``. The project directory contains a :file:`Makefile` that
holds some commands that build on other tools that micc_, notably poetry_.

To install your package in the current Python environment:

.. code-block::
  
   > make install
   
To uninstall your package in the current Python environment:

.. code-block::
  
   > make uninstall
   
To reinstall (after source code modifications) your package in the current Python 
environment:

.. code-block::
  
   > make install
   
There is also a micc_ command that allows to install a package in your current 
Python environment in development mode. Any modyfications to the source code 
are immediately visible in the installed package, exept, of course for code 
modifications to the source of binary extension modules, which must be built first:

.. code-block::
  
   > make [re]install
   > micc dev-install
   
and to uninstall:

.. code-block::
  
   > micc dev-uninstall
   > make uninstall

