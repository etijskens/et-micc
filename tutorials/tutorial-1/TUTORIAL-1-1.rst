1.1 Getting started with micc
-----------------------------
The first thing we need to start a new project is a project name. Ideally,
this project name is 

* descriptive
* unique
* short

Although one might think of even more requirements, satisfying these three
is already hard enough. 
E.g. *my_nifty_module* may possibly be unique, but it is neither descriptive,
neither short. On the other hand, *dot_product* is descriptive, reasonably
descriptive, but probably not unique. Even *my_dot_product* is probably not 
unique, and, in addition, confusing to any user that might want to adopt your
*my_dot_product*. A unique name - or at least one that has not been taken 
before - becomes really important when you want to publish your code for others
to use it. The standard place to publish Python code is the 
`Python Package Index <https://pypi.org>`_ where you find hundreds of thousands
of projects ready to be used. Even if you have only a few colleagues that may
want to use your code, you make their life easier when you publish your 
*my_nifty_module* at `PyPI <https://pypi.org>`_ as they will only need to type::

   > pip install my_nifty_module

(The name *my_nifty_module* is not used so far, but, please, choose a better name).
 Micc_ will help you publishing your work at `PyPI <https://pypi.org>`_  with 
 as little effort as possible.

So, let us call the project *ET-dot*. *ET* denote my initials, which helps 
to be unique, remains descriptive, and is certainly short. First, ``cd`` into a 
directory that you want to use as a workspace for storing your Python projects 
(I am using ``~/software/dev/workspace``). Then ask micc_ to create a project, 
like this:

.. code-block:: bash

   > cd ~/software/dev/workspace
   > micc -p ET-dot create

The ``-p`` option (which is short for ``--project-path``) tells micc_ where we 
want the project to be created. Here, we request a project directory :file:`ET-dot` in 
the current working directory, here :file:`~/software/dev/workspace`. This creates a 
project directory with, among quite a bit of other stuff, a Python module :file:`et_dot.py`

Let's take a look at the output of the *micc create* command: 
 
.. code-block:: bash

   > micc -p ET-dot create

   [INFO]           [ Creating project (ET-dot):
   [INFO]               Python module (et_dot): structure = (ET-dot/et_dot.py)
   [INFO]               [ Creating git repository
   [WARNING]                    > git push -u origin master
   [WARNING]                    (stderr)
                                remote: Repository not found.
                                fatal: repository 'https://github.com/etijskens/ET-dot/' not found
   [INFO]               ] done.
   [INFO]           ] done.
   >

The first line:
 
.. code-block:: bash

   [INFO]           [ Creating project (ET-dot):

tells us that micc_ indeed created a Python project in project directory 
:file:`ET-dot`. The second line:
 
.. code-block:: bash

   [INFO]               Python module (et_dot): structure = (ET-dot/et_dot.py)

explains that inside our project directory micc_ created a 
Python module :file:`et_dot.py`. Note that the name of the module is perhaps
not exactly what you expected: it is named :file:`et_dot.py`, rather than 
:file:`ET-dot.py`. The reason why micc_ decided to rename the module, is that our 
project name :file:`ET-dot` does not comply with the 
`PEP8 module naming rules <https://www.python.org/dev/peps/pep-0008/#package-and-module-names>`_.
To make it compliant, micc_ replaced all capitals with lowercase, and all spaces ``' '``
and dashes ``'-'`` with underscores ``'_'``. If we had choosen a PEP8 compliant 
name for the project directory, the project directory and the module name would
be the same.

Finally, the lines 
 
.. code-block:: bash

   [INFO]               [ Creating git repository
   [WARNING]                    > git push -u origin master
   [WARNING]                    (stderr)
                                remote: Repository not found.
                                fatal: repository 'https://github.com/etijskens/ET-dot/' not found
   [INFO]               ] done.

tell us that micc created a `git <https://git-scm.com/>`_ repository. Git_ is a 
version control system that solves many practical problems related to the process of
software development, independent of whether your are the only developer, or there is
an entire team working on it from different places in the world. You find more 
information about how micc_ uses git_ in *Tutorial 4*.

1.1.1 Modules and packages
^^^^^^^^^^^^^^^^^^^^^^^^^^

A *Python module* is the simplest Python project we can create. It is meant for rather
small projects that fit in a single file. More complex projects have a *package*
structure, that is, a directory with the same name as the module, i.e. :file:`et_dot`,
containing a :file:`__init__.py` file. The :file:`__init__.py` file marks the 
directory as a Python *package* and contains the statements that are executed when
the module is imported. The *module* structure is the default structure. When creating
a project you can opt for a *package* structure by appending the flag ``-p`` or 
``--package`` to the ``micc create`` command: 

.. code-block:: bash

   > micc -p ET-dot create --package

   [INFO]           [ Creating project (ET-dot):
   [INFO]               Python package (et_dot): structure = (ET-dot/et_dot/__init__.py)
   ...
   [INFO]           ] done.

Alternatively, you can easily convert a *module* structure project to a *package* structure 
project at any time:

.. code-block:: bash

   > micc -p ET-dot convert-to-package
      
1.1.2 The project path in in micc
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The project path (``-p path``) is a parameter that is accepted by all micc_ commands.
Its default value is the current directory. So, once the project is created it is
convenient to ``cd`` into it and you can leave out the ``-p`` option:

.. code-block:: bash

   > micc -p ET-dot create
   ...
   > micc -p ET-dot info
   Project ET-dot located at /Users/etijskens/software/dev/workspace/ET-dot
     package: et_dot
     version: 0.0.0
     structure: et_dot.py (Python module)
   
   > cd ET-dot
   > micc info
   Project ET-dot located at /Users/etijskens/software/dev/workspace/ET-dot
     package: et_dot
     version: 0.0.0
     structure: et_dot.py (Python module)

The *micc info* command shows information about a project.

This is a bit more practical as you do not have to type the ``-p ET-dot`` at every
micc_ command. This approach works even with the ``micc create`` command. If you 
create an empty directory and ``cd`` into it, you can just run ``micc create``: 
project like this:

.. code-block:: bash

   > mkdir ET-dot
   > cd ET-dot
   > micc create
   [INFO]           [ Creating project (ET-dot):
   [INFO]               Python package (et_dot): structure = (ET-dot/et_dot/__init__.py)
   ...
   [INFO]           ] done.

.. warning:: 
   Micc_ refuses to create a new project in a non-empty directory.
   
.. note:: In the rest of the tutorial we assume that the current working directory
   is the project directory.
      
1.1.3 Virtual environments
^^^^^^^^^^^^^^^^^^^^^^^^^^
When you are developing or using several Python projects it can become difficult 
for a single Python environment to satisfy all the requirements of these projects.
Python promotes and facilitates code reuse and as a consequence Python tools typically
depend on tens to hundreds of other modules. If toolA and toolB both need moduleC, but
each requires a different version of it, there is a conflict because it is impossible 
to install two versions of the same module in a Python environment. The solution that 
the Python community has come up with for this problem is the construction of virtual 
environments. 
In addition and for the same reason, you might need different Python versions. That 
is taken care of by Pyenv_. On my laptop I have three different Python versions, along
with the Python version that came with the OS:

.. code-block:: bash

   > pyenv versions
     system
     3.6.9
     3.7.5
   * 3.8.0 (set by /Users/etijskens/.pyenv/version)   

Thus, I have the latest patch of the of 3.6, 3.7 and 3.8 (at the time of writing, at
least). I choose 3.8.0 as the default one (as marked by the '*' in front of it), 
because I want to profit from new developments. I abandoned 2.7 many years ago. You 
can set the default Python version as ``pyenv global <version>``. In this way i also keep 
my system Python version clean. 

Since Python 3.8.0 is the default Python, without any special measures, if I launch 
Python, it will be 3.8.0. If I want to carry out the development of the ET-dot 
project in another version, e.g. 3.7.5, I must set a local python version in the 
project directory:

.. code-block:: bash
   
   > cd ET-dot
   > pyenv local 3.7.5
   > pyenv version
   3.7.5 (set by /Users/etijskens/software/dev/ET-dot/.python-version)
   > pyenv versions
     system
     3.6.9
   * 3.7.5 (set by /Users/etijskens/software/dev/ET-dot/.python-version)
     3.8.0      

Now, if I launch Python in the project-directory, it will be Python 3.7.5, in all other 
directories where ``pyenv local`` was not run, it will still be the default Python
3.8.0. Also if we run ``poetry`` in the project directory, it will be the ``poetry`` 
installed in Python 3.7.5. 
   
To reduce the chances for dependency version conflicts, a *virtual environment* must 
be created for our project that isolates its dependencies from other projects. Poetry_ 
takes care of that for us. Run ``poetry install`` in the project directory and the 
project's dependencies will be installed in a fresh virtual environment in 
:file:`ET-dot/.venv`:

.. code-block:: bash
   
   > poetry install
   Creating virtualenv et-dot in /Users/etijskens/software/dev/ET-dot/.venv
   Updating dependencies
   Resolving dependencies... (0.8s)
   
   Writing lock file
   
   
   Package operations: 10 installs, 0 updates, 0 removals
   
     - Installing pyparsing (2.4.5)
     - Installing six (1.13.0)
     - Installing atomicwrites (1.3.0)
     - Installing attrs (19.3.0)
     - Installing more-itertools (7.2.0)
     - Installing packaging (19.2)
     - Installing pluggy (0.13.1)
     - Installing py (1.8.0)
     - Installing wcwidth (0.1.7)
     - Installing pytest (4.6.6)
     - Installing ET-dot (0.0.0)

The installed packages are all dependencies of pytest which we require for testing 
our code. The last package is ET-dot itself, which is installed in so-called 
*development mode*. This means that any changes in the source code are immediately 
visible in the virtual environment. Adding/removing dependencies is easily achieved 
by running ``poetry add some_module`` and ``poetry remove some_other_module``. 
Consult the `poetry documentation <https://poetry.eustace.io/docs/>`_ for details   

To use the just created virtual environment of our project, we must activate it:

.. code-block:: bash

   > chmod +x .venv/bin/activate 
   > source .venv/bin/activate
   (.venv) > 
   
The first command is to make the ``activate`` command executable, which it is not when
the environment is just created. This command must be executed only once. The second
command activates the :file:`.venv` virtual environment, as is made visible in the 
modified command prompt. You can verify that the active Python command is correct:

.. code-block:: bash

   (.venv) > which python
   /Users/etijskens/software/dev/ET-dot/.venv/bin/python
   (.venv)> python --version
   > python --version
   Python 3.7.5

.. note:: Whenever you see a command prompt like ``(.venv) >`` the local virtual environment
   of the project has been activated. If you want to try yourself, you must activate it too.

1.1.4 Modules and scripts
^^^^^^^^^^^^^^^^^^^^^^^^^
Note that micc_ always creates fully functional examples, complete with test code and 
documentation generation, so that you can inspect the files and see as much as 
possible how things are supposed to work. E.g. here is the :file`ET-dot/et_dot.py` module:

.. code-block:: python

   # -*- coding: utf-8 -*-
   """
   Package et_dot
   ==============
   
   A 'hello world' example.
   """
   __version__ = "0.0.0"
   
   
   def hello(who='world'):
       """'Hello world' method."""
       result = "Hello " + who
       return result

The module can be used right away. Open an interactive Python session and enter the 
following commands:

.. code-block:: bash
   
   > cd path/to/ET-dot
   > source .venv/bin/activate
   (.venv) > python
   Python 3.8.0 (default, Nov 25 2019, 20:09:24)
   [Clang 11.0.0 (clang-1100.0.33.12)] on darwin
   Type "help", "copyright", "credits" or "license" for more information.
   >>> import et_dot   
   >>> et_dot.hello()
   'Hello world'
   >>> et_dot.hello("student")
   'Hello student'
   >>>
   
**Productivity tip**

Using an interactive python session to verify that a module does indeed what 
you expect is a bit cumbersome. A quicker way is to modify the module so that it
can also behave as a script. Add the following lines to :file:`ET-dot/et_dot.py`
at the end of the file:

.. code-block:: python

   if __name__=="__main__":
      print(hello())
      print(hello("student"))
      
and execute it on the command line:

.. code-block:: bash
   
   (.venv) > python et_dot.py
   Hello world
   Hello student
      
The body of the ``if`` statement is only executed if the file is executed as
a script. When the file is imported, it is ignored.

While working on a single-file project it is sometimes handy to put your tests
the body of ``if __name__=="__main__":``, as below:

.. code-block:: python

   if __name__=="__main__":
      assert hello() == "Hello world"
      assert hello("student") == "Hello student"
      print("-*# success #*-")

The last line makes sure that you get a message that all tests went well if they
did, otherwise an :py:exc:`AssertionError` will be raised.
When you now execute the script, you should see:
      
.. code-block:: bash
   
   (.venv) > python et_dot.py
   -*# success #*-
   
When you develop your code in an IDE like `eclipse+pydev <https://www.pydev.org>`_ or 
`PyCharm <https://www.jetbrains.com/pycharm/>`_, you can even execute the file without
having to leave your editor and switch to a terminal. You can quickly code, test and 
debug in a single window. 

While this is a very productive way of developing, it is a bit on the *quick and dirty*
side. If the module code and the tests become more involved, however,the file will soon 
become cluttered with test code and a more scalable way to organise your tests is needed. 
Micc_ has already taken care of this.

1.1.5 Testing your code
^^^^^^^^^^^^^^^^^^^^^^^

When micc_ creates a new project, or when you add components to an existing project,
it immediately adds a test script for each component in the :file:`tests` directory. 
The test script for the :py:mod:`et_dot` module is in file :file:`ET-dot/tests/test_et_dot.py`. 
Let's take a look at the relevant section:

.. code-block:: python

   # -*- coding: utf-8 -*-
   """Tests for et_dot package."""

   import et_dot
   
   def test_hello_noargs():
       """Test for foo.hello()."""
       s = foo.hello()
       assert s=="Hello world"      
   
   def test_hello_me():
       """Test for foo.hello('me')."""
       s = foo.hello('me')
       assert s=="Hello me"
                
Tests like this are very useful to ensure that during development the changes to
your code do not break things. There are many Python tools for unit testing and test
driven development. Here, we use `Pytest <https://pytest.org/en/latest/>`_:

.. code-block:: bash

   > pytest
   =============================== test session starts ===============================
   platform darwin -- Python 3.7.4, pytest-4.6.5, py-1.8.0, pluggy-0.13.0
   rootdir: /Users/etijskens/software/dev/workspace/foo
   collected 2 items
   
   tests/test_foo.py ..                                                        [100%]
   
   ============================ 2 passed in 0.05 seconds =============================
             
The output shows some info about the environment in which we are running the tests,
the current working directory (c.q. the project directory, and the number of tests
it collected (2). *Pytest* looks for test methods in all :file:`test_*.py` or 
:file:`*_test.py` files in the current directory and accepts ``test`` prefixed methods 
outside classes and ``test`` prefixed methods inside ``Test`` prefixed classes as test 
methods to be executed.

If a test would fail you get a detailed report to help you find the cause of the
error and fix it. 

1.1.6 Debugging test code
^^^^^^^^^^^^^^^^^^^^^^^^^
When the report provided by pytest_ does not yield a clue on the 
cause of the failing test, you must use debugging and execute the failing test step
by step to find out what is going wrong where. From the viewpoint of pytest_, the 
files in the :file:`tests` directory are modules. Pytest_ imports them and collects
the test methods, and executes them. Micc_ makes every test module executable using 
the technique described in `1.1.4 Modules and scripts`_. At the end of every test file you 
will find some extra code 
   
.. code-block:: python

   if __name__ == "__main__":
       the_test_you_want_to_debug = test_hello_noargs
   
       print("__main__ running", the_test_you_want_to_debug)
       the_test_you_want_to_debug()
       print('-*# finished #*-')
       
On the first line of the ``if __name__ == "__main__":`` body, the variable 
:py:obj:`the_test_you_want_to_debug` is set to the name of some test method in our 
test file :file:`test_et_dot.py`, here :py:obj:`test_hello_noargs`. The variable  
:py:obj:`the_test_you_want_to_debug` is now just another variable pointing to the 
very same function object as :py:obj:`test_hello_noargs` and behaves exactly the 
same (see `Functions are first class objects <https://www.geeksforgeeks.org/first-class-functions-python/>`_).
The next statement prints a start message that tells you that ``__main__`` is running that
test method, after which the test method is called through the :py:obj:`the_test_you_want_to_debug`
variable, and finally another message is printed to let you know that the script finished. 
Here is the output you get when running this test file as a script:

.. code-block:: bash
  
   (.venv) > python tests/test_et_dot.py
   __main__ running <function test_hello_noargs at 0x1037337a0>
   -*# finished #*-
   
The execution of the test does not produce any output. Now you can use your favourite
Python debugger to execute this script and step into the :py:obj:`test_hello_noargs`
test method and from there into :py:obj:`foo.hello` to examine if everything goes as
expected. Thus, to debug a failing test, you assign its name to the 
:py:obj:`the_test_you_want_to_debug` variable and debug the script.
 
.. note::

   As test code is also code, it can contain bugs. More often than not, it happens
   that the code tested is correct, but the test is flawed. 

1.1.7 Generating documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can generate (using `sphinx <http://www.sphinx-doc.org/en/master/>`_)
the documentation for the project like this:

.. code-block:: bash

   > cd path/to/project_directory
   > micc docs --html --open
   
This will generate html documentation in :file:`docs/_build/html/index.html`
 and open it in your default browser (because of the ``--open`` option). It 
 will look like this:

.. image:: ../tutorials/tutorial-1/im1.png

If your expand the **API** tab on the left, you get to see the :py:mod:`et_dot`
module documentation, as it generated from the doc-strings:

.. image:: ../tutorials/tutorial-1/im2.png

A pdf can be generated as:

.. code-block:: bash

   > micc docs --pdf -o

This will generate a pdf and open it in your default pdf viewer (because of the
``-o`` option, which is short for ``--open``). You will find the result in 
:file:`docs/_build/latex/ET-dot.pdf`. 

Documentation is almost completely generated automatically from the doc-strings
in your code using sphinx_. Doc-strings are the text between triple double quote 
pairs in the examples above, e.g. ``"""This is a doc-string."""``. Important 
doc-strings are

* *module* doc-strings: at the beginning of the module
* *class* doc-strings: right after the ``class`` statement
* *method* doc-strings: right after a ``def`` statemen

Thus, if you take good care writing doc-strings, the documentation follows. 

The boilerplate code for documentation is in the ``docs`` directory. Touching 
those files is not recommended, and only rarely needed. Then there are a number 
of :file:`.rst` files with **capitalized** names in the project directory,

* :file:`README.rst` is assumed to contain an overview of the project,
* :file:`API.rst` describes the classes and methods of the project in detail,
* :file:`APPS.rst` describes command line interfaces or apps added to your project.
* :file:`AUTHORS.rst` list the contributors to the project
* :file:`HISTORY.rst` which should describe the changes that were made to the code.

The :file:`.rst` extenstion stands for the
`reStructuredText <https://devguide.python.org/documenting/#restructuredtext-primer>`_ 
format. It provide a simple and concise approach to formatting. 

If you add components to your project through micc_, care is taken that the 
:file:`.rst` files in the project directory and the :file:`docs` directory are
modified as necessary, so that sphinx_ is able find the doc-strings. Even for 
command line interfaces (CLI, or console scripts) based on 
`click <https://click.palletsprojects.com/en/7.x/>`_ the documentation is generated 
neatly from the :py:obj:`help` strings of options and the doc-strings of the commands.

1.1.8 The license file
^^^^^^^^^^^^^^^^^^^^^^
The project directory contains a :file:`LICENCE` file, a :file:`text` file
describing the licence applicable to your project. You can choose between 

* MIT license (default),
* BSD license,
* ISC license,
* Apache Software License 2.0,
* GNU General Public License v3 and
* Not open source. 

MIT license is a very liberal license and the default option. If you’re unsure which 
license to choose, you can use resources such as `GitHub’s Choose a License <https://choosealicense.com>`_

You can select the license file when you create the project:

.. code-block:: bash
   
   > cd some_empty_dir
   > micc create --license BSD

Of course, the project depends in no way on the license file, so it can 
be replaced manually at any time by the license you desire.
    
1.1.9 The Pyproject.toml file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The file :file:`pyproject.toml` (located in the project directory) is the 
modern way to describe the build system requirements of the project: 
`PEP 518 <https://www.python.org/dev/peps/pep-0518/>`_. Although most of 
this file's content is generated automatically by micc_ and poetry_ some
understanding of it is useful, consult https://poetry.eustace.io/docs/pyproject/.
  
1.1.10 The log file Micc.log
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The project directory also contains a log file :file:`micc.log`. All micc_ commands
that modify the state of the project leave a trace in this file, So you can look up 
what happened when to your project. Should you think that the log file has become
too big, or just useless, you can delete it manually, or add the ``--clear-log`` flag
before any micc_ subcommand, to remove it. If the subcommand alters the state of the
project, the log file will only contain the log messages from the last subcommand.

.. code-block:: bash

   > ll micc.log
   -rw-r--r--  1 etijskens  staff  34 Oct 10 20:37 micc.log
   
   > micc --clear-log info      
   Project bar located at /Users/etijskens/software/dev/workspace/bar
     package: bar
     version: 0.0.0
     structure: bar.py (Python module)
   
   > ll micc.log
   ls: micc.log: No such file or directory

