Tutorial 1: a simple project
============================

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
`Micc <https://github.com/etijskens/et-micc>`_ will help you publishing your work at
`PyPI <https://pypi.org>`_  with as little effort as possible.

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

Modules and packages
^^^^^^^^^^^^^^^^^^^^

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
   Converting simple Python project ET-dot to general Python project.
   [WARNING]        Pre-existing files in /Users/etijskens/software/dev/workspace that would be overwritten:
   [WARNING]          /Users/etijskens/software/dev/workspace/ET-dot/docs/index.rst
      Aborting because 'overwrite==False'.
        Rerun the command with the '--backup' flag to first backup these files (*.bak).
        Rerun the command with the '--overwrite' flag to overwrite these files without backup.
      Aborting.
   [CRITICAL]       Exiting (-3) ...
   [WARNING]        It is normally ok to overwrite 'index.rst' as you are not supposed
                    to edit the '.rst' files in '/Users/etijskens/software/dev/workspace/ET-dot/docs.'
                    If in doubt: rerun the command with the '--backup' flag,
                      otherwise: rerun the command with the '--overwrite' flag,

Because we do not want to replace existing files inadvertently, this command will
always fail, unless you add either the ``--backup`` flag, in which case micc_ makes
a backup of all files it wants to replace, or the ``--overwrite``, in which case
those files will be overwritten. Micc_ will always produce a list of files it wants
to replace. Unless you deliberately modified one of the files in the list, you can
safely use ``--overwrite``. If you did, use the ``--backup`` flag and manually copy
the the changes from the :file:`.bak` file to the new file.

.. code-block:: bash

   > micc convert-to-package --overwrite
   Converting simple Python project ET-dot to general Python project.
   [WARNING]        '--overwrite' specified: pre-existing files in /Users/etijskens/software/dev/workspace will be overwritten WITHOUT backup:
   [WARNING]        overwriting /Users/etijskens/software/dev/workspace/ET-dot/docs/index.rst

The project path in in micc
^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Managing the Python version
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Your operating system typically comes with a Python version that is used OS tasks.
It is, obviously good practice to isolate your system Python from your own developments:
wrecking the system Python can indeed give you headaches. In addition, the system
Python is often still 2.7.x, which is about to retire in 2020. Using a more recent
Python version, or even several different Python versions may be very useful when
you are working on many different projects. That is offered conveniently by
`pyenv <https://github.com/pyenv/pyenv>`_. On my work laptop I usually keep the
latest minor recent Python versions, along with the Pythonversion that came with
the OS. At the time of writing that was:

.. code-block:: bash

   > pyenv versions
     system
     3.6.9
     3.7.5
   * 3.8.0 (set by /Users/etijskens/.pyenv/version)

The asterisk marks the default Python. You can set the default Python version as
``pyenv global <version>``. It is good practice not to make the system Python
default. In that way you cannot accidentally wreck your system Python.

Since Python 3.8.0 is the default Python, without any special measures, if you launch
Python, it will be 3.8.0. If you want to carry out the development of the ET-dot
project in another version, e.g. 3.7.5, you must set a local python version in the
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

Now, if you launch Python in the project-directory (or any of its subdirectories
that does not have its own :file:`.python-version`), it will be Python 3.7.5. In all
othern directories where ``pyenv local`` was not run, it will still be the default
Python 3.8.0.

Virtual environments
^^^^^^^^^^^^^^^^^^^^
For a more detailed introduction to virtual environments see
`Python Virtual Environments: A Primer <https://realpython.com/python-virtual-environments-a-primer/>`_.

When you are developing or using several Python projects it can become difficult
for a single Python environment to satisfy all the dependency requirements of these
projects simultaneously. Dependencies conflict can easily arise.
Python promotes and facilitates code reuse and as a consequence Python tools typically
depend on tens to hundreds of other modules. If toolA and toolB both need moduleC, but
each requires a different version of it, there is a conflict because it is impossible
to install two versions of the same module in a Python environment. The solution that
the Python community has come up with for this problem is the construction of *virtual
environments*, which isolates the dependencies of a single project to a single
environment.

Creating virtual environments
"""""""""""""""""""""""""""""
Since Python 3.3 Python comes with a :py:mod:`venv` module for the creation of
virtual environments::

   > python -m venv my_virtual_environment

This creates a directory :file:`my_virtual_environment` containing a complete and
isolated Python environment. This virtual environment can be activated sa::

   > source my_virtual_environment/bin/activate
   (my_virtual_environment) >

Activating a virtual environment modifies the command prompt to remind you constantly
that you are working in a virtual environment. The virtual environment is based on the
current Python - by preference set by pyenv_. If you install new packages, they will
be installed in the virtual environment only. The virtual environment can be deactivated
by running ::

   (my_virtual_environment) > deactivate
   >

Creating virtual environments with Poetry
"""""""""""""""""""""""""""""""""""""""""
Poetry_ uses the above mechanism to manage virtual environment on a per project
basis, and can install all the dependencies of that project, as specified in the
:file:`pyproject.toml` file, using the ``install`` command. Since our project does
not have a virtual environment yet, `Poetry <https://python-poetry.org>`_  creates
one, named :file:`.venv`, and installs all dependencies in it. We first choose the
Python version to use for the project::

   > pyenv local 3.7.5
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

If the virtual environment already exists, or if some virtual environment is activated
(not necessarily that of the project itself - be warned), that virtual environment is
reused and all installations pertain to that virtual environment.

To use the just created virtual environment of our project, we must activate it::

   > source .venv/bin/activate
   (.venv) > which python
   /Users/etijskens/software/dev/ET-dot/.venv/bin/python
   (.venv)> python --version
   > python --version
   Python 3.7.5

The location of the virtual environment's Python and its version are as expected.

.. note:: Whenever you see a command prompt like ``(.venv) >`` the local virtual environment
   of the project has been activated. If you want to try yourself, you must activate it too.

To deactivate a script just run ``deactivate``::

   (.venv) > deactivate
   > which python
   /Users/etijskens/.pyenv/shims/python

The ``(.venv)`` notice disappears, and the active python is no longer that in the
virtual environment.

If something is wrong with a virtual environment, you can simply delete it::

   > rm -rf .venv

and create a new one. Sometimes it is necessary to delete the :file:`poetry.lock` as well::

   > rm poetry.lock

Modules and scripts
^^^^^^^^^^^^^^^^^^^
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

Testing your code
^^^^^^^^^^^^^^^^^

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

Debugging test code
^^^^^^^^^^^^^^^^^^^
When the report provided by pytest_ does not yield a clue on the
cause of the failing test, you must use debugging and execute the failing test step
by step to find out what is going wrong where. From the viewpoint of pytest_, the
files in the :file:`tests` directory are modules. Pytest_ imports them and collects
the test methods, and executes them. Micc_ makes every test module executable using
the technique described in `Modules and scripts`_. At the end of every test file you
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

Generating documentation
^^^^^^^^^^^^^^^^^^^^^^^^
Documentation is extracted from the source code using `Sphinx <http://www.sphinx-doc.org/en/master/>`_.
It is almost completely generated automatically from the doc-strings in your code. Doc-strings are the
text between triple double quote pairs in the examples above, e.g. ``"""This is a doc-string."""``.
Important doc-strings are:

* *module* doc-strings: at the beginning of the module. Provides an overview of what the
  module is for.
* *class* doc-strings: right after the ``class`` statement: explains what the class is for.
  (Usually, the doc-string of the __init__ method is put here as well, as dunder methods
  (starting and ending with a double underscore) are not automatically considered by sphinx_.

* *method* doc-strings: right after a ``def`` statement.

According to `pep-0287 <https://www.python.org/dev/peps/pep-0287/>`_ the recommended format for
Python doc-strings is `restructuredText <http://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_.
E.g. a typical method doc-string looks like this:

  .. code-block:: python

     def hello_world(who='world'):
         """Short (one line) description of the hello_world method.

         A detailed and longer description of the hello_world method.
         blablabla...

         :param str who: an explanation of the who parameter. You should
             mention its default value.
         :returns: a description of what hello_world returns (if relevant).
         :raises: which exceptions are raised under what conditions.
         """

Here, you can find some more `examples <http://queirozf.com/entries/python-docstrings-reference-examples>`_.

Thus, if you take good care writing doc-strings, helpfule documentation follows automatically.

Micc sets up al the necessary components for documentation generation in sub-directory
:file:`et-dot/docs/`. There, you find a :file:`Makefile` that provides a simple interface
to Sphinx_. Here is the workflow that is necessary to build the documentation:

.. code-block:: bash

      > cd path/to/et-dot
      > source .venv/bin/activate
      (.venv) > cd docs
      (.venv) > make <documentation_format>

Let's explain the steps


#. ``cd`` into the project directory::

      > cd path/to/et-dot
      >

#. Activate the project's virtual environment::

      > source .venv/bin/activate
      (.venv) >

#. ``cd`` into the docs subdirectory::

      (.venv) > cd docs
      (.venv) >

   Here, you will find the :file:`Makefile` that does the work::

      (.venv) > ls -l
      total 80
      -rw-r--r--  1 etijskens  staff  1871 Dec 10 11:24 Makefile
      ...

To see a list of possible documentation formats, just run ``make`` without arguments::

      (.venv) > make
      Sphinx v2.2.2
      Please use `make target' where target is one of
        html        to make standalone HTML files
        dirhtml     to make HTML files named index.html in directories
        singlehtml  to make a single large HTML file
        pickle      to make pickle files
        json        to make JSON files
        htmlhelp    to make HTML files and an HTML help project
        qthelp      to make HTML files and a qthelp project
        devhelp     to make HTML files and a Devhelp project
        epub        to make an epub
        latex       to make LaTeX files, you can set PAPER=a4 or PAPER=letter
        latexpdf    to make LaTeX and PDF files (default pdflatex)
        latexpdfja  to make LaTeX files and run them through platex/dvipdfmx
        text        to make text files
        man         to make manual pages
        texinfo     to make Texinfo files
        info        to make Texinfo files and run them through makeinfo
        gettext     to make PO message catalogs
        changes     to make an overview of all changed/added/deprecated items
        xml         to make Docutils-native XML files
        pseudoxml   to make pseudoxml-XML files for display purposes
        linkcheck   to check all external links for integrity
        doctest     to run all doctests embedded in the documentation (if enabled)
        coverage    to run coverage check of the documentation (if enabled)
      (.venv) >

#. To build documentation in html format, enter::

      (.venv) > make html
      ...
      (.venv) >

   This will generation documentation in :file:`et-dot/docs/_build/html`. Note that
   **it is essential that this command executes in the project's virtual environment**.
   You can view the documentation in your favorit browser:

        (.venv) > open _build/html/index.html

   Here is a screenshot:

   .. image:: ../tutorials/im1-1.png

   If your expand the **API** tab on the left, you get to see the :py:mod:`et_dot`
   module documentation, as it generated from the doc-strings:

   .. image:: ../tutorials/im1-2.png

#. To build documentation in .pdf format, enter::

      (.venv) > make latexpdf

   This will generation documentation in :file:et-dot/docs/_build/latex/et-dot.pdf`. Note that
   **it is essential that this command executes in the project's virtual environment**.
   You can view it in your favorite pdf viewer::

        (.venv) > open _build/latex/et-dot.pdf
        (.venv) >

.. note:: When building documentation by running the :file:`docs/Makefile`, it is
   verified that the correct virtual environment is activated, and that the needed
   Python modules are installed in that environment. If not, they are first installed
   using `pip install`. These components are not becoming dependencies of the project.
   If needed you can add dependencies using the ``poetry add`` command.

The boilerplate code for documentation generation is in the ``docs`` directory, just as
if it were generated by hand using ``sphinx-quickstart``. (In fact, it was generated using
``sphinx-quickstart``, but then turned into a
`Cookiecutter <https://github.com/audreyr/cookiecutter-pypackage>`_ template.)
those files is not recommended, and only rarely needed. Then there are a number
of :file:`.rst` files with **capitalized** names in the **project directory**:

* :file:`README.rst` is assumed to contain an overview of the project,
* :file:`API.rst` describes the classes and methods of the project in detail,
* :file:`APPS.rst` describes command line interfaces or apps added to your project.
* :file:`AUTHORS.rst` list the contributors to the project
* :file:`HISTORY.rst` which should describe the changes that were made to the code.

The :file:`.rst` extenstion stands for reStructuredText_. It iss a simple and concise
approach to text formatting.

If you add components to your project through micc_, care is taken that the
:file:`.rst` files in the project directory and the :file:`docs` directory are
modified as necessary, so that sphinx_ is able find the doc-strings. Even for
command line interfaces (CLI, or console scripts) based on
`click <https://click.palletsprojects.com/en/7.x/>`_ the documentation is generated
neatly from the :py:obj:`help` strings of options and the doc-strings of the commands.

The license file
^^^^^^^^^^^^^^^^
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

The Pyproject.toml file
^^^^^^^^^^^^^^^^^^^^^^^
The file :file:`pyproject.toml` (located in the project directory) is the
modern way to describe the build system requirements of the project:
`PEP 518 <https://www.python.org/dev/peps/pep-0518/>`_. Although most of
this file's content is generated automatically by micc_ and poetry_ some
understanding of it is useful, consult https://poetry.eustace.io/docs/pyproject/.

The :file:`pyproject.toml` file is rather human-readable::

   > cat pyproject.toml
   [tool.poetry]
   name = "ET-dot"
   version = "1.0.0"
   description = "<Enter a one-sentence description of this project here.>"
   authors = ["Engelbert Tijskens <engelbert.tijskens@uantwerpen.be>"]
   license = "MIT"

   readme = 'README.rst'

   repository = "https://github.com/etijskens/ET-dot"
   homepage = "https://github.com/etijskens/ET-dot"

   keywords = ['packaging', 'poetry']

   [tool.poetry.dependencies]
   python = "^3.7"
   et-micc-build = "^0.10.10"

   [tool.poetry.dev-dependencies]
   pytest = "^4.4.2"

   [tool.poetry.scripts]

   [build-system]
   requires = ["poetry>=0.12"]
   build-backend = "poetry.masonry.api"

The log file Micc.log
^^^^^^^^^^^^^^^^^^^^^
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

Adjusting micc to your needs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Micc_ is based on a series of additive Cookiecutter_ templates which generate the
boilerplate code. If you like, you can tweak these templates in the
:file:`site-packages/et_micc/templates` directory of your micc_ installation. When you
``pipx`` installed micc_, that is typically something like:

   :file:`~/.local/pipx/venvs/et-micc/lib/pythonX.Y/site-packages/et_micc`,

where :file`pythonX.Y` is the python version you installed micc_ with.

1.2 Your first project
----------------------

Let's start with a simple problem: a Python module that computes the
`dot product of two arrays <https://en.wikipedia.org/wiki/Dot_product>`_.
Admittedly, this not a very rewarding goal, as there are already many Python
packages, e.g. Numpy_, that solve this problem in an elegant and efficient way.
However, because the dot product is such a simple concept in linear algebra,
it allows us to illustrate the usefulness of Python as a language for High
Performance Computing, as well as the capabilities of Micc_.

If you haven't carried out the steps in `1.1 Getting started with micc`_, set up a new
project (you are of course encouraged to change the project name as to make it unique) :

.. code-block:: bash

    > micc -p ET-dot create
    [INFO]           [ Creating project (ET-dot):
    [INFO]               Python module (et_dot): structure = (ET-dot/et_dot.py
    [INFO]               [ Creating git repository
    [WARNING]                    > git push -u origin master
    [WARNING]                    (stderr)
                                 remote: Repository not found.
                                 fatal: repository 'https://github.com/etijskens/ET-dot/' not found
    [INFO]               ] done.
    [WARNING]            Run 'poetry install' in the project directory to create a virtual environment and install its dependencies.
    [INFO]           ] done.
    > cd ET-dot

Next, we create a virtual environment for the project and activate it:

.. code-block:: bash

    > poetry install
    Creating virtualenv et-dot in /Users/etijskens/software/dev/workspace/tmp/ET-dot/.venv
    Updating dependencies
    Resolving dependencies... (0.8s)

    Writing lock file


    Package operations: 10 installs, 0 updates, 0 removals

      - Installing pyparsing (2.4.5)
      - Installing six (1.13.0)
      - Installing atomicwrites (1.3.0)
      - Installing attrs (19.3.0)
      - Installing more-itertools (8.0.2)
      - Installing packaging (19.2)
      - Installing pluggy (0.13.1)
      - Installing py (1.8.0)
      - Installing wcwidth (0.1.7)
      - Installing pytest (4.6.7)
      - Installing ET-dot (0.0.0)
    > source .venv/bin/activate
    (.venv) >

Open module file :file:`et_dot.py` in your favourite editor and change it as follows:

.. code-block:: python

   # -*- coding: utf-8 -*-
   """
   Package et_dot
   ==============
   Python module for computing the dot product of two arrays.
   """
   __version__ = "0.0.0"

   def dot(a,b):
       """Compute the dot product of *a* and *b*.

       :param a: a 1D array.
       :param b: a 1D array of the same length as *a*.
       :returns: the dot product of *a* and *b*.
       :raises: ArithmeticError if ``len(a)!=len(b)``.
       """
       n = len(a)
       if len(b)!=n:
           raise ArithmeticError("dot(a,b) requires len(a)==len(b).")
       d = 0
       for i in range(n):
           d += a[i]*b[i]
       return d

We defined a :py:meth:`dot` method with an informative doc-string that describes
the parameters, the return value and the kind of exceptions it may raise.

We could use the dot method in a script as follows:

.. code-block:: python

   from et_dot import dot

   a = [1,2,3]
   b = [4.1,4.2,4.3]
   a_dot_b = dot(a,b)

.. note::
   This dot product implementation is naive for many reasons:

   * Python is very slow at executing loops, as compared to Fortran or C++.
   * The objects we are passing in are plain Python :py:obj:`list`s. A :py:obj:`list`
     is a very powerfull data structure, with array-like properties, but it is not
     exactly an array. A :py:obj:`list` is in fact an array of pointers to Python
     objects, and therefor list elements can reference anything, not just a numeric value
     as we would expect from an array. With elements being pointers, looping over the
     array elements implies non-contiguous memory access, another source of inefficiency.
   * The dot product is a subject of Linear Algebra. Many excellent libraries have been
     designed for this purpose. Numpy_ should be your starting
     point because it is well integrated with many other Python packages. There is also
     `Eigen <http://eigen.tuxfamily.org/index.php?title=Main_Page>`_
     a C++ library for linear algebra that is neatly exposed to Python by
     pybind11_.

In order to verify that our implementation of the dot product is correct, we write a
test. For this we open the file ``tests/test_et_dot.py``. Remove the original tests,
and add a new one:

.. code-block:: python

    import et_dot

    def test_dot_aa():
        a = [1,2,3]
        expected = 14
        result = et_dot.dot(a,a)
        assert result==expected

Save the file, and run the test. Pytest_ will show a line for every test source file.
On each such line a ``.`` will appear for every successfull test, and a ``F`` for a
failing test.

.. code-block:: bash

   (.venv) > pytest
   =============================== test session starts ===============================
   platform darwin -- Python 3.7.4, pytest-4.6.5, py-1.8.0, pluggy-0.13.0
   rootdir: /Users/etijskens/software/dev/workspace/ET-dot
   collected 1 item

   tests/test_et_dot.py .                                                      [100%]

   ============================ 1 passed in 0.08 seconds =============================
   (.venv) >

.. note:: If the project's virtual environment is not activated, the command ``pytest``
    will generally not be found.

Great! our test succeeded. Let's increment the project's version (``-p`` is short for ``--patch``,
and requests incrementing the patch component of the version string)::

    (.venv) > micc version -p
    [INFO]           (ET-dot)> micc version (0.0.0) -> (0.0.1)


Obviously, our test tests only one particular case.
A clever way of testing is to focus on properties. From mathematics we now that
the dot product is commutative. Let's add a test for that.

.. code-block:: python

    import random

    def test_dot_commutative():
        # create two arrays of length 10 with random float numbers:
        a = []
        b = []
        for _ in range(10):
            a.append(random.random())
            b.append(random.random())
        # do the test
        ab = et_dot.dot(a,b)
        ba = et_dot.dot(b,a)
        assert ab==ba

You can easily verify that this test works too. We increment the version string again::

    (.venv) > micc version -p
    [INFO]           (ET-dot)> micc version (0.0.1) -> (0.0.2)

There is however a risk in using
arrays of random numbers. Maybe we were just lucky and got random numbers that satisfy
the test by accident. Also the test is not reproducible anymore. The next time we run
pytest_ we will get other random numbers, and may be the test will fail. That would
represent a serious problem: since we cannot reproduce the failing test, we have no way
finding out what went wrong. For random numbers we can fix the seed at the beginning of
the test. Random number generators are deterministic, so fixing the seed makes the code
reproducible. To increase coverage we put a loop around the test.

.. code-block:: python

   def test_dot_commutative_2():
       # Fix the seed for the random number generator of module random.
       random.seed(0)
       # choose array size
       n = 10
       # create two arrays of length n with with zeros:
       a = n * [0]
       b = n * [0]
       # repetion loop:
       for r in range(1000):
           # fill a and b with random float numbers:
           for i in range(n):
               a[i] = random.random()
               b[i] = random.random()
           # do the test
           ab = et_dot.dot(a,b)
           ba = et_dot.dot(b,a)
           assert ab==ba

Again the test works. Another property of the dot product is that the dot product
with a zero vector is zero.

.. code-block:: python

   def test_dot_zero():
       # Fix the seed for the random number generator of module random.
       random.seed(0)
       # choose array size
       n = 10
       # create two arrays of length n with with zeros:
       a = n * [0]
       zero = n * [0]
       # repetion loop (the underscore is a placeholder for a variable dat we do not use):
       for _ in range(1000):
           # fill a with random float numbers:
           for i in range(n):
               a[i] = random.random()
           # do the test
           azero = et_dot.dot(a,zero)
           assert azero==0

This test works too. Furthermore, the dot product with a vector of ones is the sum of
the elements of the other vector:

.. code-block:: python

   def test_dot_one():
       # Fix the seed for the random number generator of module random.
       random.seed(0)
       # choose array size
       n = 10
       # create two arrays of length n with with zeros:
       a = n * [0]
       one = n * [1.0]
       # repetion loop (the underscore is a placeholder for a variable dat we do not use):
       for _ in range(1000):
           # fill a with random float numbers:
           for i in range(n):
               a[i] = random.random()
           # do the test
           aone = et_dot.dot(a,one)
           expected = sum(a)
           assert aone==expected

Success again. We are getting quite confident in the correctness of our implementation. Here
is another test:

.. code-block:: python

   def test_dot_one_2():
       a1 = 1.0e16
       a   = [a1 ,1.0,-a1]
       one = [1.0,1.0,1.0]
       expected = 1.0
       result = et_dot.dot(a,one)
       assert result==expected

Clearly, it is a special case of the test above the expected result is the sum of the elements
in ``a``, that is ``1.0``. Yet it - unexpectedly - fails. Fortunately pytest_ produces a readable
report about the failure:

.. code-block:: bash

   > pytest
   ================================= test session starts ==================================
   platform darwin -- Python 3.7.4, pytest-4.6.5, py-1.8.0, pluggy-0.13.0
   rootdir: /Users/etijskens/software/dev/workspace/ET-dot
   collected 6 items

   tests/test_et_dot.py .....F                                                      [100%]

   ======================================= FAILURES =======================================
   ____________________________________ test_dot_one_2 ____________________________________

       def test_dot_one_2():
           a1 = 1.0e16
           a   = [a1 , 1.0, -a1]
           one = [1.0, 1.0, 1.0]
           expected = 1.0
           result = et_dot.dot(a,one)
   >       assert result==expected
   E       assert 0.0 == 1.0

   tests/test_et_dot.py:91: AssertionError
   ========================== 1 failed, 5 passed in 0.17 seconds ==========================
   >

Mathematically, our expectations about the outcome of the test are certainly correct. Yet,
pytest_ tells us it found that the result is ``0.0`` rather than ``1.0``. What could possibly
be wrong? Well our mathematical expectations are based on our - false - assumption that the
elements of ``a`` are real numbers, most of which in decimal representation are characterised
by an infinite number of digits. Computer memory being finite, however, Python (and for that
matter all other programming languages) uses a finite number of bits to approximate real
numbers. These numbers are called *floating point numbers* and their arithmetic is called
*floating point arithmetic*.  *Floating point arithmetic* has quite different properties than
real number arithmetic. A floating point number in Python uses 64 bits which yields
approximately 15 representable digits. Observe the consequences of this in the Python statements
below:

.. code-block:: python

   >>> 1.0 + 1e16
   1e+16
   >>> 1e16 + 1.0 == 1e16
   True
   >>> 1.0 + 1e16 == 1e16
   True
   >>> 1e16 + 1.0 - 1e16
   0.0

There are several lessons to be learned from this:

* The test does not fail because our code is wrong, but because our mind is used to reasoning
  about real number arithmetic, rather than *floating point arithmetic* rules. As the latter
  is subject to round-off errors, tests sometimes fail unexpectedly.  Note that for comparing
  floating point numbers the the standard library provides a :py:meth:`math.isclose` method.
* Another silent assumption by which we can be mislead is in the random numbers. In fact,
  :py:meth:`random.random` generates pseudo-random numbers **in the interval ``[0,1[``**, which
  is quite a bit smaller than ``]-inf,+inf[``. No matter how often we run the test the special
  case above that fails will never be encountered, which may lead to unwarranted confidence in
  the code.

So, how do we cope with the failing test? Here is a way using :py:meth:`math.isclose`:

.. code-block:: python

   import math

   def test_dot_one_2():
       a1 = 1.0e16
       a   = [a1 , 1.0, -a1]
       one = [1.0, 1.0, 1.0]
       expected = 1.0
       result = et_dot.dot(a,one)
       # assert result==expected
       assert math.isclose(result, expected, abs_tol=10.0)

This is a reasonable solution if we accept that when dealing with numbers as big as ``1e19``,
an absolute difference of ``10`` is negligible.

Another aspect that should be tested is the behavior of the code in exceptional circumstances.
Does it indeed raise :py:exc:`ArithmeticError` if the arguments are not of the same length?
Here is a test:

.. code-block:: python

   import pytest

   def test_dot_unequal_length():
       a = [1,2]
       b = [1,2,3]
       with pytest.raises(ArithmeticError):
           et_dot.dot(a,b)

Here, :py:meth:`pytest.raises` is a *context manager* that will verify that :py:exc:`ArithmeticError`
is raise when its body is executed.

.. note:: A detailed explanation about context managers see
   https://jeffknupp.com/blog/2016/03/07/python-with-context-managers//

Note that you can easily make :meth:`et_dot.dot` raise other
exceptions, e.g. :exc:`TypeError` by passing in arrays of non-numeric types:

.. code-block:: python

   >>> et_dot.dot([1,2],[1,'two'])
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/Users/etijskens/software/dev/workspace/ET-dot/et_dot.py", line 23, in dot
       d += a[i]*b[i]
   TypeError: unsupported operand type(s) for +=: 'int' and 'str'
   >>>

Note that it is not the product ``a[i]*b[i]`` for ``i=1`` that is wreaking havoc, but
the addition of its result to ``d``.

At this point you might notice that even for a very simple and well defined function
as the dot product the amount of test code easily exceeds the amount of tested code
by a factor of 5 or more. This is not at all uncommon. As the tested code here is an
isolated piece of code, you will probably leave it alone as soon as it passes the tests
and you are confident in the solution. If at some point, the :py:meth:`dot` would fail
you should write a test that reproduces the error and improve the solution so that it
passes the test.

When constructing software for more complex problems, there will very soon be many
interacting components and running the tests after modifying one of the components
will help you assure that all components still play well together, and spot problems
as soon as possible.

At this point we want to produce a git tag of the project::

    (.venv) > micc tag
    [INFO] Creating git tag v0.0.7 for project ET-dot
    [INFO] Done.

The tag is a label for the current code base of our project.

1.3 Improving efficiency
------------------------
There are times when a correct solution - i.e. a code that solves the problem correctly -
is sufficient. Very often, however, there are constraints on the time to solution, and
the computing resources (number of cores and nodes, memory, ..) are requested to be used
efficiently. Especially in scientific computing and high performance computing, where
compute tasks may run for many days using hundreds of compute nodes and resources are
to be shared with many researchers, using the resources efficiently is of utmost importance.

However important efficiency may be, it is nevertheless a good strategy for developing a
new piece of code, to start out with a simple, even naive implementation in Python, neglecting
all efficiency considerations, but focussing on correctness. Python has a reputation of being
an extremely productive programming language. Once you have proven the correctness of this first
version it can serve as a reference solution to verify the correctness of later efficiency
improvements. In addition, the analysis of this version can highlight the sources of
inefficiency and help you focus your attention to the parts that really need it.

Timing your code
^^^^^^^^^^^^^^^^
The simplest way to probe the efficiency of your code is to time it: write a simple script
and record how long it takes to execute. Let us first look at the structure of a Python script.

Here's a script (using the above structure) that computes the dot product of two long arrays
of random numbers.

.. code-block:: python

   """file ET_dot/prof/run1.py"""
   import random
   from et_dot import dot

   def random_array(n=1000):
       """Initialize an array with n random numbers in [0,1[."""
       # Below we use a list comprehension (a Python idiom for creating a list from an iterable object).
       a = [random.random() for i in range(n)]
       return a

   if __name__=='__main__':
       a = random_array()
       b = random_array()
       print(dot(a,b))
       print('-*# done #*-')

We store this file, which we rather simply called :file:`run1.py`, in a directory :file:`prof`
in the project directory where we intend to keep all our profiling work.
You can execute the script from the command line (with the project directory as the current
working directory:

.. code-block:: bash

   (.venv) > python ./prof/run1.py
   251.08238559724717
   -*# done #*-

.. note:: As our script does not fix the random number seed, every run has a different outcome.

We are now ready to time our script. There are many ways to achieve this. Here is a
`particularly good introduction <https://realpython.com/python-timer/>`_. The
`et-stopwatch project <https://pypi.org/project/et-stopwatch/>`_ takes this a little
further. We add it as a development dependency of our project::

    (.venv) > poetry add et_stopwatch -D
    Using version ^0.3.0 for et_stopwatch
    Updating dependencies
    Resolving dependencies... (0.2s)
    Writing lock file
    Package operations: 1 install, 0 updates, 0 removals
      - Installing et-stopwatch (0.3.0)
    (.venv) >

.. note:: A development dependency is a package that is not needed for using the package
    at hand, bit only needed for developing it.

Using the :py:class:`Stopwatch` class to time pieces of code is simple:

.. code-block:: python

   """file ET_dot/prof/run1.py"""
   from et_micc.stopwatch import Stopwatch

   ...

   if __name__=='__main__':
       with Stopwatch(name="init"):
           a = random_array()
           b = random_array()
       with Stopwatch(name="dot "):
           dot(a,b)
       print('-*# done #*-')

When the script is exectuted the two print statements will print the duration of the
initalisation of *a* and *b* and of the computation of the dot product of *a* and *b*.
Finally, upon exit the :py:obj:`Stopwatch` will print the total time.

.. code-block:: bash

   (.venv) > python ./prof/run1.py
   init: 0.000281 s
   dot : 0.000174 s
   -*# done #*-
   >

Note that the initialization phase took longer than the computation. Random number
generation is rather expensive.

Comparing to Numpy
^^^^^^^^^^^^^^^^^^
As said earlier, our implementation of the dot product is rather naive. If you want
to become a good programmer, you should understand that you are probably not the
first researcher in need of a dot product implementation. For most linear algebra
problems, `Numpy <https://numpy.org>`_ provides very efficient implementations.
Below the :file:`run1.py` script adds timing results for the Numpy_ equivalent of
our code.

.. code-block:: python

   """file ET_dot/prof/run1.py"""
   import numpy as np

   ...

   if __name__=='__main__':
       with Stopwatch(name="et init"):
           a = random_array()
           b = random_array()
       with Stopwatch(name="et dot "):
           dot(a,b)

       with Stopwatch(name="np init"):
           a = np.random.rand(1000)
           b = np.random.rand(1000)
       with Stopwatch(name="np dot "):
           np.dot(a,b)

       print('-*# done #*-')

Obviously, to run this script, we must first install Numpy_ (again as a development
dependency)::

    (.venv) > poetry add numpy -D
    Using version ^1.18.1 for numpy
    Updating dependencies
    Resolving dependencies... (1.5s)
    Writing lock file
    Package operations: 1 install, 0 updates, 0 removals
      - Installing numpy (1.18.1)
    (.venv) >

Here are the results of the modified script:

.. code-block:: bash

   (.venv) > python ./prof/run1.py
   et init: 0.000252 s
   et dot : 0.000219 s
   np init: 7.8e-05 s
   np dot : 3.2e-05 s
   -*# done #*-
   >

Obviously, Numpy_ does significantly better than our naive dot product implementation.
The reasons for this improvement are:

*   Numpy_ arrays are contiguous data structures of floating point numbers, unlike Python's
    :py:class:`list`. Contiguous memory access is far more efficient.
*   The loop over Numpy_ arrays is implemented in a low-level programming languange.
    This allows to make full use of the processors hardware features, such as *vectorization*
    and *fused multiply-add* (FMA).

Conclusion
^^^^^^^^^^
There are three important generic lessons to be learned from this tutorial:

#.  Always start your projects with a simple and straightforward implementation which
    can be easily be proven to be correct. Write test code for proving correctness.

#.  Time your code to understand which parts are time consuming and which not. Optimize
    bottlenecks first and do not waste time optimizing code that does not contribute
    significantly to the total runtime. Optimized code is typically harder to read and
    may become a maintenance issue.

#.  Before you write code, in this case our dot product implementation, spent some time
    searching the internet to see what is already available. Especially in the field of
    scientific and high performance computing there are many excellent libraries available
    which are hard to beat. Use your precious time for new stuff.

