Tutorial 1: Getting started with micc
=====================================

.. note::

   These tutorials focus not just on how to use micc_. Rather they describe a workflow
   for how you might set up a python project and develop it using best practises, with
   the help of micc_.

   All tutorial sections start with the bare essentials, which should get you
   up and running. They are often followed by more detailed subsections that
   provide useful background information that is needed for intermediate or
   advanced usage. These sections have an explicit *[intermediate]* or
   *[advanced]* tag in the title, e.g. :ref:`modules-and-packages` and they are
   indented. Background sections can be skipped on first reading, but the user
   is encouraged to read them at some point. The tutorials are rather extensive
   as they interlaced with many good practices advises.

Micc_ wants to provide a practical interface to the many aspects of managing a
Python project: setting up a new project in a standardized way, adding documentation,
version control, publishing the code to PyPI_, building binary extension modules in C++
or Fortran, dependency management, ... For all these aspect there are tools available,
yet i found myself struggling get everything right and looking up the details each time.
Micc_ is an attempt to wrap all the details by providing the user with a standardized
yet flexible workflow for managing a Python project. Standardizing is a great way to
increase productivity. For many aspects the tools used by Micc_ are completely hidden
from the user, e.g. project setup, adding components, building binary extensions, ...
For other aspects Micc_ provides just the necessary setup for you to use other tools
as you need them. Learning to use the following tools is certainly beneficial:

* Poetry_: for dependency management, virtual environment creation, and
  publishing the project to PyPI_ (and a lot more, if you like). Although
  extremely handy on a desktop machine or a laptop, it does not play well with
  the module system that is used on the VSC clusters for accessing applications.
  A workaround is provided in Tutorial 6.

* Git_: for version control. Its use is optional
  but highly recommended. See Tutorial 4 for some git_ coverage.

* Pytest_: for (unit) testing. Also optional and also highly recommended.

* Sphinx_: for building documentation. Optional but recommended.

The basic commands for these tools are covered in these tutorials.

.. _micc-setup:

1.0 Micc setup
--------------

Before micc can be used it must be setup to specify some preferences. Most entries
have sensible default entries, but your name, email address and github user name
have to be provided by you, if they are to make any sense, obviously. The github
username is needed if you want to be able to push your commits to github (see
:ref:`tutorial-4` for details).

Run ``micc setup`` to set the preferences::

    > micc setup
    your full name [first-name last-name]: Engelbert Tijskens
    your e-mail address [your.email@whatev.er]: engelbert.tijskens@uantwerpen.be
    your github username (leave empty if you do not have one,
      or create one at https://github.com/join) [your-github-username]: etijskens
    the initial version number of a new project [0.0.0]:
    default git branch [master]:
    default minimal Python version [3.7]:
    Html theme for sphinx documentation [sphinx_rtd_theme]:
    Choose default license (MIT license, BSD license, ISC license, Apache Software License 2.0, GNU General Public License v3, Not open source) [MIT license]:
    python file extension [py]:
    Done

    If you want to change your preferences, edit the default entries in file
        /Users/etijskens/.et_micc/micc.json
    Note that these changes will only affect NEW projects. Existing projects will be unaffected.

You can always change your settings by running ``micc setup --force``.

You may want to correct your entries, but not that changes will only affect NEW projects,
not existing ones.


.. _create-proj:

1.1 Creating a project with micc
--------------------------------
Creating a new project with micc_ is simple::

    > micc create path/to/my_first_project

This creates a new project *my_first_project* in folder ``path/to``.
Note that the directory  ``path/to/my_first_project`` must either not exist,
or be empty.

Typically, the new project is created in the current working directory:

    .. code-block:: bash

       > cd path/to
       > micc create my_first_project
       [INFO]           [ Creating project (my_first_project):
       [INFO]               Python module (my_first_project): structure = (my_first_project/my_first_project.py)
       ...
       [INFO]           ] done.

If you have setup micc with a Github account, and created a personal access token
(see :ref:`tutorial-4`), this will also create a public remote repository at Github.
If you do not want a public remote repo, or no remote repo at all, you must add
``--remote=private``, or ``--remote=none`` to the ``micc create`` command.

After creating the project, we ``cd`` into the project directory because then any further
micc_ commands will then automatically act on the project in the current working directory::

       > cd my_first_project

To apply a micc_ command to a project that is not in the current working directory
see :ref:`micc-project-path`.

The above command creates a project for a simple Python *module*, that is, the
project directory will contain - among others - a file ``my_first_project.py`` in
which represents the Python module::

    my_first_project          # the project directory
    └── my_first_project.py   # the Python module, this is where your code goes

When some client code imports this module:

    .. code-block:: python

        import my_first_module

Python reads and executes the code in ``my_first_module.py``. (Typically, this registers
the methods and classes defined in the module file. Also some variables, may be set up).

Note that the name of the Python module name is (automatically) taken from the project name
that with gave in the ``micc create`` command. If you want project and module names to
differ from each other, check out the :ref:`project-and-module-naming` section.

The module project type above is suited for problems that can be solved with a single
Python file (``my_first_project.py`` in the above case). For more complex problems a
*package* structure is more appropriate. To learn more about the use of Python modules
vs packages, check out the :ref:`modules-and-packages` section below.

.. _modules-and-packages:

1.1.1. Modules and packages [intermediate]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    A *Python module* is the simplest Python project we can create. It is meant for rather
    small projects that conveniently fit in a single (Python) file. More complex projects
    require a *package* structure. They are created by adding the ``--package`` flag on the
    command line::

        > micc create my_first_project --package
        [INFO]           [ Creating project (my_first_project):
        [INFO]               Python package (my_first_project): structure = (my_first_project/my_first_project/__init__.py)
        [INFO]               [ Creating git repository
                               ...
        [INFO]               ] done.
        [WARNING]            Run 'poetry install' in the project directory to create a virtual environment and install its dependencies.
        [INFO]           ] done.

    The output shows a different file structure of the project than for a module. Instead
    of the file ``my_first_project.py`` there is a directory ``my_first_project``, containing
    a ``__init__.py`` file. So, the structure of a package project looks like this::

        my_first_project          # the project directory
        └── my_first_project      # the package directory
            └── __init__.py       # the file where your code goes

    Typically, the package directory will contain several other Python files that together
    make up your Python package. When some client code imports a module with a package
    structure,

    .. code-block:: python

        import my_first_module

    Python reads the code in ``my_first_module/__init__.py`` and executes it. The
    ``my_first_module/__init__.py`` file is the equivalent of the ``my_first_module.py``
    in a module structure.

    The distinction between a module structure and a package structure is also important
    when you publish the module. When installing a Python package with a module structure,
    only the ``my_first_project.py`` will be installed, while with the package structure
    the entire ``my_first_project`` directory will be installed.

    If you created a projected with a module structure and discover over time that its
    complexity has grown beyond the limits of a simple module, you can easily convert
    it to a *package* structure project at any time. First ``cd`` into the project
    directory and run::

       > cd my_first_project
       > micc convert-to-package
       [INFO]           Converting Python module project my_first_project to Python package project.
       [WARNING]        Pre-existing files that would be overwritten:
       [WARNING]          /Users/etijskens/software/dev/workspace/p1/docs/index.rst
       Aborting because 'overwrite==False'.
         Rerun the command with the '--backup' flag to first backup these files (*.bak).
         Rerun the command with the '--overwrite' flag to overwrite these files without backup.

    Because we do not want to replace existing files inadvertently, this command will
    always fail, unless you add either the ``--backup`` flag, in which case micc_ makes
    a backup of all files it wants to replace, or the ``--overwrite`` flag, in which case
    those files will be overwritten. Micc_ will always produce a list of files it wants
    to replace. You can safely use ``--overwrite``, unless you deliberately modified one
    of the files in the list (which is rarely needed). If you did change one of the listed
    files, however, use the ``--backup`` flag and manually copy the the changes from the :file:`.bak`
    file to the new file.

    .. code-block:: bash

       > micc convert-to-package --overwrite
       Converting simple Python project my_first_project to general Python project.
       [WARNING]        '--overwrite' specified: pre-existing files will be overwritten WITHOUT backup:
       [WARNING]        overwriting /Users/etijskens/software/dev/workspace/ET-dot/docs/index.rst

    and run the ``info`` command to verify the result:

    .. code-block:: bash

       > micc info
       Project my_first_project located at /Users/etijskens/software/dev/workspace/my_first_project
         package: my_first_project
         version: 0.0.0
         structure: my_first_project/__init__.py (Python package)

.. _project-and-module-naming:

1.1.2 What's in a name [intermediate]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    The name you choose for your project has many consequences. Ideally, a project
    name is:

    * descriptive,
    * unique,
    * short.

    Although one might think of even more requirements, such as being easy to type,
    satisfying these three is already hard enough.
    E.g. *my_nifty_module* may possibly be unique, but it is neither descriptive,
    neither short. On the other hand, *dot_product* is descriptive, reasonably
    short, but probably not unique. Even *my_dot_product* is probably not
    unique, and, in addition, confusing to any user that might want to adopt *your*
    *my_dot_product*. A unique name - or at least a name that has not been taken
    before - becomes really important when you want to publish your code for others
    to use it. The standard place to publish Python code is the
    `Python Package Index <https://pypi.org>`_, where you find hundreds of thousands
    of projects, many of which are really interesting and of high quality. Even if
    there are only a few colleagues that you want to share your code with, you make
    their life (as well as yours) easier when you publish your *my_nifty_module* at
    PyPI_. To install your ``my_nifty_module`` they will only need to type::

       > pip install my_nifty_module

    while having internet access, obviously. The name *my_nifty_module* is not used
    so far, but nevertheless we recommend to choose a better name. Micc_ will help
    you publishing your code at PyPI_  with as little effort as possible (see
    :ref:`tutorial-5`), provided your name has not been used sofar. Note that
    the ``micc create`` command has a ``--publish`` flag that checks if the name you
    want to use for your project is still available on PyPI_, and, if not, refuses to
    create the project and asks you to use another name for your project::

        > micc create oops --publish
        [ERROR]
            The name 'oops' is already in use on PyPI.
            The project is not created.
            You must choose another name if you want to publish your code.

    As there are indeed hundreds of thousands of Python packages published on PyPI_,
    finding a good name has become quite hard. Personally, I often use a simple and
    short descriptive name, prefixed by my initials, ``et-``, which usually makes
    the name unique. E.g ``et-oops`` does not exist. This has the additional advantage
    that all my published modules are grouped in the alphabetic PyPI_ listing.

    Another point of attention is that although in principle project names can be anything
    supported by your OS file system, as they are just the name of a directory, micc_
    insists that module and package names comply with the
    `PEP8 module naming rules <https://www.python.org/dev/peps/pep-0008/#package-and-module-names>`_.
    Micc_ derives the package (or module) name from the project name as follows:

    * capitals are replaced by lower-case
    * hyphens``'-'`` are replaced by underscores ``'_'``

    If the resulting module name is not PEP8 compliant, you get an informative error
    message::

        > micc create 1proj
        [ERROR]
        The project name (1proj) does not yield a PEP8 compliant module name:"
          The project name must start with char, and contain only chars, digits, hyphens and underscores."
          Alternatively, provide an explicit module name with the --module-name=<name>"

    The last line indicates that you can specify an explicit module name, unrelated to
    the project name. In that case PEP8 compliance is not checked. The responsability
    then is all yours.

.. _first-steps:

1.2 First steps in project management (using micc)
--------------------------------------------------

.. _micc-project-path:

1.2.1. The project path in micc [intermediate]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    All micc_ commands accept the global ``--project-path=<path>`` parameter. Global
    parameters appear before the subcommand name. E.g. the command::

        > micc --project-path path/to/my_first_project info
        Project my_first_project located at path/to/my_first_project.
          package: my_first_project
          version: 0.0.0
          structure: my_first_project.py (Python module)

    prints some info on the project at ``path/to/my_first_project``. This can conveniently be
    abbreviated as::

        > micc -p path/to/my_first_project info

    Even the ``create`` command accepts the global ``--project-path=<path>`` parameter::

        > micc -p path/to/my_second_project create

    will create project ``my_second_project`` in the specified location. The command is
    identical to::

        > micc create path/to/my_second_project

    The default value for the project path is the current working directory, so::

        > micc info

    will print info about the project in the current working directory.

    Hence, while working on a project, it is convenient to cd into the project directory
    and execute your micc_ commands from there, without the the global ``--project-path=<path>``
    parameter.

    This approach works even with the ``micc create`` command. If you create an empty
    directory and ``cd`` into it, you can just run ``micc create`` and it will create
    the project in the current working directory, taking the project name from the name
    of the current working directory.

.. _virtual-environments:

1.2.2 Virtual environments
^^^^^^^^^^^^^^^^^^^^^^^^^^
Virtual environments enable you to set up a Python environment that isolated
from the installed Python on your system. In this way you can easily cope with varying
dependencies between your Python projects.

For a detailed introduction to virtual environments see
`Python Virtual Environments: A Primer <https://realpython.com/python-virtual-environments-a-primer/>`_.

When you are developing or using several Python projects it can indeed become difficult
for a single Python environment to satisfy all the dependency requirements of these
projects simultaneously. Dependency conflicts can easily arise.
Python promotes and facilitates code reuse and as a consequence Python tools typically
depend on tens to hundreds of other modules. If toolA and toolB both need moduleC, but
each requires a different version of it, there is a conflict because it is impossible
to install two versions of the same module in a Python environment. The solution that
the Python community has come up with for this problem is the construction of *virtual
environments*, which isolates the dependencies of a single project in a single
environment.

.. _venv:

1.2.2.1 Creating virtual environments
"""""""""""""""""""""""""""""""""""""
Since Python 3.3 Python comes with a :py:mod:`venv` module for the creation of
virtual environments. To set up a virtual environment, you first select the Python
version you want to use, e.g. using pyenv_::

    > pyenv local 3.7.5
    > python --version
    Python 3.7.5
    > which python
    /Users/etijskens/.pyenv/shims/python

Next, create the virtual environment ``my_virtual_environment``::

   > python -m venv my_virtual_environment

This creates a directory :file:`my_virtual_environment` in the current working directory
which contains a complete isolated Python environment. To use the virtual environment, you
must *activate* it::

    > source my_virtual_environment/bin/activate
    (my_virtual_environment) >

Activating a virtual environment modifies the command prompt to remind you constantly
that you are now working in virtual environment ``my_virtual_environment``. You can
verify the Python version and its location:

    (my_virtual_environment) > python --version
    Python 3.7.5
    (my_virtual_environment) > which python
    path/to/my_virtual_environment/bin/python

If you now install new packages, they will be installed in the virtual environment **only**.
The virtual environment can be *deactivated* by running ::

    (my_virtual_environment) > deactivate
    >

after which the ``(my_virtual_environment)`` in the prompt disappears, and you are
back to where you created the virtual environment::

    > python --version
    Python 3.7.5
    > which python
    /Users/etijskens/.pyenv/shims/python
    >

.. _venv-poetry:

1.2.2.2 Creating virtual environments with Poetry
"""""""""""""""""""""""""""""""""""""""""""""""""
Poetry_ uses the above mechanism to manage virtual environment on a per project
basis, and can install all the dependencies of that project, as specified in the
:file:`pyproject.toml` file, using the ``install`` command. Since our project does
not have a virtual environment yet, Poetry_ creates one, named :file:`.venv`, and
installs all dependencies in it. Again, we first choose the Python version to use
for the project::

   > pyenv local 3.7.5
   > python --version
   Python 3.7.5
   > which python
   /Users/etijskens/.pyenv/shims/python

Next, we ``cd`` into the project directory and use poetry_ to create the virtual environment
and at the same install all the project's dependencies aa specified in ``pyproject.toml``::

   > cd path/to/my_first_project
   > poetry install
   Creating virtualenv et-dot in /Users/etijskens/software/dev/my_first_project/.venv
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
     - Installing my_first_project (0.0.0)

The installed packages are all dependencies of pytest which we require for testing
our code. The last package is my_first_project itself, which is installed in so-called
*development mode*. This means that any changes in the source code are immediately
visible in the virtual environment. Adding/removing dependencies is easily achieved
by running ``poetry add some_module`` and ``poetry remove some_other_module``.
Consult the poetry_documentation_ for details.

To use the just created virtual environment of our project, we must activate it,
as before::

   > source .venv/bin/activate
   (.venv) >

Poetry_ always names the virtual environment of a project :file:`.venv`. So, when
working on several projects at the same time, you can sometimes get confused which
project's virtual environment is actually activated. Just run::

    (.venv) > which python
    path/to/my_first_project/.venv/bin/python
    (.venv) >

If you no longer need the virtual environment, deactivate it::

   (.venv) > deactivate
   >

If something is wrong with a virtual environment, you can simply delete it::

   > rm -rf .venv

and create it again. Sometimes it is necessary to delete the :file:`poetry.lock` as well::

   > rm poetry.lock

.. _modules-and-scripts:

1.2.3 Modules and scripts
^^^^^^^^^^^^^^^^^^^^^^^^^
Micc_ always creates fully functional examples, complete with test code and documentation,
so that you can inspect the files and learn how things are working. The :file:`my_first_project.py`
module contains a simple *hello world* method, called ``hello``:

.. code-block:: python

   # -*- coding: utf-8 -*-
   """
   Package my_first_project
   ========================

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

   > cd path/to/my_first_project
   > source .venv/bin/activate
   (.venv) > python
   Python 3.8.0 (default, Nov 25 2019, 20:09:24)
   [Clang 11.0.0 (clang-1100.0.33.12)] on darwin
   Type "help", "copyright", "credits" or "license" for more information.
   >>> import my_first_project
   >>> my_first_project.hello()
   'Hello world'
   >>> my_first_project.hello("student")
   'Hello student'
   >>>

**Productivity tip**

Using an interactive python session to verify that a module does indeed what
you expect is a bit cumbersome. A quicker way is to modify the module so that it
can also behave as a script. Add the following lines to :file:`my_first_project.py`
at the end of the file:

.. code-block:: python

   if __name__=="__main__":
      print(hello())
      print(hello("student"))

and execute it on the command line:

.. code-block:: bash

   (.venv) > python my_first_project.py
   Hello world
   Hello student

The body of the ``if __name__=="__main__":`` statement is only executed if the file
is executed as a script. When the file is imported, the condition is ``False``, and
the body (the script part) is ignored.

While working on a single-file project it is sometimes handy to put your tests
the body of ``if __name__=="__main__":``, as below:

.. code-block:: python

   if __name__=="__main__":
      assert hello() == "Hello world"
      assert hello("student") == "Hello student"
      print("-*# success #*-")

The last line makes sure that you get a message that all tests went well if they
did, otherwise an :py:exc:`AssertionError` will be raised.
When you now execute the script, you should see::

   (.venv) > python my_first_project.py
   -*# success #*-

When you develop your code in an IDE like `eclipse+pydev <https://www.pydev.org>`_ or
`PyCharm <https://www.jetbrains.com/pycharm/>`_, you can even execute the file without
having to leave your editor and switch to a terminal. You can quickly code, test and
debug in a single window.

While this is a very productive way of developing, it is a bit on the *quick and dirty*
side. If the module code and the tests become more involved, however,the file will soon
become cluttered with test code and a more scalable way to organise your tests is needed.
Micc_ has already taken care of this.

.. _testing:

1.2.4 Testing your code
^^^^^^^^^^^^^^^^^^^^^^^
`Test driven development <https://en.wikipedia.org/wiki/Test-driven_development>`_ is a
software development process that relies on the repetition of a very short development cycle:
requirements are turned into very specific test cases, then the code is improved so that the
tests pass. This is opposed to software development that allows code to be added that is not
proven to meet requirements. The advantage of this is clear: the shorter the cycle, the
smaller the code that is to be searched for bugs. This allows you to produce correct code
faster, and in case you are a beginner, also speeds your learning of Python. Please check
Ned Batchelder's very good introduction to `testing with pytest <https://nedbatchelder.com/text/test3.html>`_.

When micc_ creates a new project, or when you add components to an existing project,
it immediately adds a test script for each component in the :file:`tests` directory.
The test script for the :py:mod:`my_first_project` module is in file :file:`ET-dot/tests/test_my_first_project.py`.
Let's take a look at the relevant section:

.. code-block:: python

   # -*- coding: utf-8 -*-
   """Tests for my_first_project package."""

   import my_first_project

   def test_hello_noargs():
       """Test for my_first_project.hello()."""
       s = my_first_project.hello()
       assert s=="Hello world"

   def test_hello_me():
       """Test for my_first_project.hello('me')."""
       s = my_first_project.hello('me')
       assert s=="Hello me"

Tests like this are very useful to ensure that during development the changes to
your code do not break things. There are many Python tools for unit testing and test
driven development. Here, we use `Pytest <https://pytest.org/en/latest/>`_:

.. code-block:: bash

   > pytest
   =============================== test session starts ===============================
   platform darwin -- Python 3.7.4, pytest-4.6.5, py-1.8.0, pluggy-0.13.0
   rootdir: /Users/etijskens/software/dev/workspace/my_first_project
   collected 2 items

   tests/test_my_first_project.py ..                                                        [100%]

   ============================ 2 passed in 0.05 seconds =============================


The output shows some info about the environment in which we are running the tests,
the current working directory (c.q. the project directory, and the number of tests
it collected (2). Pytest_ looks for test methods in all :file:`test_*.py` or
:file:`*_test.py` files in the current directory and accepts ``test`` prefixed methods
outside classes and ``test`` prefixed methods inside ``Test`` prefixed classes as test
methods to be executed.

.. note::
   Sometimes pytest_ discovers unintended test files or functions in other directories
   than the :file:`tests` directory, leading to puzzling errors. It is therefore safe
   to instruct pytest_ to look only in the :file:`tests` directory::

        > pytest tests
        ...

If a test would fail you get a detailed report to help you find the cause of the
error and fix it.

.. _debug-test-code:

1.2.4.1 Debugging test code
"""""""""""""""""""""""""""
When the report provided by pytest_ does not yield a clue on the
cause of the failing test, you must use debugging and execute the failing test step
by step to find out what is going wrong where. From the viewpoint of pytest_, the
files in the :file:`tests` directory are modules. Pytest_ imports them and collects
the test methods, and executes them. Micc_ also makes every test module executable using
the technique described in :ref:`modules-and-scripts`. At the end of every test file you
will find some extra code:

.. code-block:: python

   if __name__ == "__main__":
       the_test_you_want_to_debug = test_hello_noargs
       print("__main__ running", the_test_you_want_to_debug)
       the_test_you_want_to_debug()
       print('-*# finished #*-')

On the first line of the ``if __name__ == "__main__":`` body, the name of the test method
we want to debug is set to variable ``the_test_you_want_to_debug``, here ``test_hello_noargs``.
The variable thus becomes an alias for the test method. Line 2 prints a message with the name
of the test method being debugged::

   (.venv) > python tests/test_et_dot.py
   __main__ running <function test_hello_noargs at 0x1037337a0>     # output of line 2
   -*# finished #*-                                                 # output of line 4

Line 3 actually calls the test method. Finally, line 4  prints a message to let the user know
that the script is finished.

You can use your favourite Python debugger to execute this script and step into the
``test_hello_noargs`` test method and from there into ``my_first_project.hello`` to
examine if everything goes as expected.

.. _generate-doc:

1.2.5 Generating documentation [intermediate]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Documentation is extracted from the source code using `Sphinx <http://www.sphinx-doc.org/en/master/>`_.
It is almost completely generated automatically from the doc-strings in your code. Doc-strings are the
text between triple double quote pairs in the examples above, e.g. ``"""This is a doc-string."""``.
Important doc-strings are:

* *module* doc-strings: at the beginning of the module. Provides an overview of what the
  module is for.
* *class* doc-strings: right after the ``class`` statement: explains what the class is for.
  (Usually, the doc-string of the __init__ method is put here as well, as *dunder* methods
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
             mention e.g. its default value.
         :returns: a description of what hello_world returns (if relevant).
         :raises: which exceptions are raised under what conditions.
         """

Here, you can find some more `examples <http://queirozf.com/entries/python-docstrings-reference-examples>`_.

Thus, if you take good care writing doc-strings, helpful documentation follows automatically.

Micc sets up al the necessary components for documentation generation in sub-directory
:file:`et-dot/docs/`. There, you find a :file:`Makefile` that provides a simple interface
to Sphinx_. Here is the workflow that is necessary to build the documentation:

.. code-block:: bash

      > cd path/to/et-dot
      > source .venv/bin/activate
      (.venv) > cd docs
      (.venv) > make html

The last line produces documentation in html format.

Let's explain the steps

#. ``cd`` into the project directory::

      > cd path/to/et-dot
      >

#. Activate the project's virtual environment::

      > source .venv/bin/activate
      (.venv) >

   This is necessary because the tools for documentation generation are installed there.

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
   You can view the documentation in your favorite browser::

        (.venv) > open _build/html/index.html       # on macosx

   or::

        (.venv) > xdg-open _build/html/index.html   # on ubuntu

   (On the cluster the command will fail because it does not have a graphical environment
   and it cannot run a html-browser.)

   Here is a screenshot:

   .. image:: ../tutorials/im1-1.png

   If your expand the **API** tab on the left, you get to see the :py:mod:`my_first_project`
   module documentation, as it generated from the doc-strings:

   .. image:: ../tutorials/im1-2.png

#. To build documentation in .pdf format, enter::

      (.venv) > make latexpdf

   This will generation documentation in :file:et-dot/docs/_build/latex/et-dot.pdf`.
   You can view it in your favorite pdf viewer::

        (.venv) > open _build/latex/et-dot.pdf      # on macosx

   or::

        (.venv) > xdg-open _build/latex/et-dot.pdf      # on ubuntu

.. note:: When building documentation by running the :file:`docs/Makefile`, it is
   verified that the correct virtual environment is activated, and that the needed
   Python modules are installed in that environment. If not, they are first installed
   using `pip install`. These components are not becoming dependencies of the project.
   If needed you can add dependencies using the ``poetry add`` command.

The boilerplate code for documentation generation is in the ``docs`` directory, just as
if it were generated by hand using the ``sphinx-quickstart`` command. (In fact, it was
generated using ``sphinx-quickstart``, but then turned into a
`Cookiecutter <https://github.com/audreyr/cookiecutter-pypackage>`_ template.)
those files is not recommended, and only rarely needed. Then there are a number
of :file:`.rst` files with **capitalized** names in the **project directory**:

* :file:`README.rst` is assumed to contain an overview of the project,
* :file:`API.rst` describes the classes and methods of the project in detail,
* :file:`APPS.rst` describes command line interfaces or apps added to your project.
* :file:`AUTHORS.rst` list the contributors to the project
* :file:`HISTORY.rst` which should describe the changes that were made to the code.

The :file:`.rst` extenstion stands for reStructuredText_. It is a simple and concise
approach to text formatting.

If you add components to your project through micc_, care is taken that the
:file:`.rst` files in the project directory and the :file:`docs` directory are
modified as necessary, so that sphinx_ is able find the doc-strings. Even for
command line interfaces (CLI, or console scripts) based on
`click <https://click.palletsprojects.com/en/7.x/>`_ the documentation is generated
neatly from the :py:obj:`help` strings of options and the doc-strings of the commands.

.. _version-control:

1.2.6 Version control [advanced]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    Although version control is extremely important for any software project
    with a lifetime of more a day, we mark it as an advanced topic as it does
    not affect the development itself. Micc_ facilitates version control by
    automatically creating a local git_ repository in your project directory.
    If you do not want to use it, you may ignore it or even delete it.

    Git_ is a version control system that solves many practical problems related
    to the process software development, independent of whether your are the only
    developer, or there is an entire team working on it from different places in
    the world. You find more information about how micc_ uses git_ in :ref:`tutorial-4`.

.. _miscellaneous:

1.3 Miscellaneous
-----------------

.. _license:

1.3.1 The license file [intermediate]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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

.. _pyproject-toml:

1.3.2 The pyproject.toml file [intermediate]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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

.. _log-file:

1.3.3 The log file Micc.log [intermediate]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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

.. _adjusting-micc:

1.3.4 Adjusting micc to your needs [advanced]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    Micc_ is based on a series of additive Cookiecutter_ templates which generate the
    boilerplate code. If you like, you can tweak these templates in the
    :file:`site-packages/et_micc/templates` directory of your micc_ installation. When you
    ``pipx`` installed micc_, that is typically something like:

       :file:`~/.local/pipx/venvs/et-micc/lib/pythonX.Y/site-packages/et_micc`,

    where :file`pythonX.Y` is the python version you installed micc_ with.

.. _first-project:

1.4 A first real project
------------------------
Let's start with a simple problem: a Python module that computes the
`scalar product of two arrays <https://en.wikipedia.org/wiki/Dot_product>`_,
generally referred to as the *dot product*.
Admittedly, this not a very rewarding goal, as there are already many Python
packages, e.g. Numpy_, that solve this problem in an elegant and efficient way.
However, because the dot product is such a simple concept in linear algebra,
it allows us to illustrate the usefulness of Python as a language for High
Performance Computing, as well as the capabilities of Micc_.

First, set up a new project for this *dot* project, which i named *ET-dot*, *ET*
being my initials. Not knowing beforehand how involved this project will become,
we create a simple *module* project:

.. code-block:: bash

    > micc -p ET-dot create
    [INFO]           [ Creating project (ET-dot):
    [INFO]               Python module (my_first_project): structure = (ET-dot/et_dot.py
    [INFO]               [ Creating git repository
    [WARNING]                    > git push -u origin master
    [WARNING]                    (stderr)
                                 remote: Repository not found.
                                 fatal: repository 'https://github.com/etijskens/ET-dot/' not found
    [INFO]               ] done.
    [WARNING]            Run 'poetry install' in the project directory to create a virtual environment and install its dependencies.
    [INFO]           ] done.
    > cd ET-dot

As the output shows the module name is converted from the project name and made compliant with the
`PEP8 module naming rules <https://www.python.org/dev/peps/pep-0008/#package-and-module-names>`_:
*et_dot*. Next, we create a virtual environment for the project with all the standard micc_
dependencies:

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
    >

Next, activate the virtual environment:

    > source .venv/bin/activate
    (.venv) >

Open module file :file:`et_dot.py` in your favourite editor and code a dot product
method (naievely) as follows:

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

   However, starting out with a simple and naive implementation is not a bad idea at all.
   Once it is correct, it can serve as reference implementation to test any improvements
   against it.

In order to proof that our implementation of the dot product is correct, we write some
tests. For this we open the file ``tests/test_et_dot.py``. Remove the original tests put in
by micc_, and add a new one:

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

You can read more about the ``micc version`` command in section :ref:`version-management`.

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
pytest_ we will get other random numbers, and maybe the test will fail. That would
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

This is a reasonable solution if we accept that when dealing with numbers as big as ``1e16``,
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

The tag is a label for the current code base of our project. It marks a specific
point in the development of a code, in this case the point where our (first)
implementation is considered correct. That is, however, not to say that the tests
are now useless and can be thrown away. Every time we need to change the implemention,
to improve the user interface or the efficiency, or add a feature, we should run the
tests again to make sure that the changes did not break the code. of course, we should
also extend the test suite to cover the new properties of the code.

.. _efficiency:

1.5 Improving efficiency
------------------------
There are times when a just a correct solution to the problem at hand
is sufficient. If ``ET-dot`` is meant to compute a few dot products of small
arrays, the naive implementation above will probably be sufficient.
However, if it is to be used many times and for large arrays and the uses
is impatiently waiting for the answer, or if your computing resources are
scarse, a more efficient implementation is needed. Especially in scientific
computing and high performance computing, where compute tasks may run for days
using hundreds or even thousands of of compute nodes and resources are
to be shared with many researchers, using the resources efficiently is
of utmost importance and efficient implementations are therefore indispensable.

However important efficiency may be, it is nevertheless a good strategy for developing a
new piece of code, to start out with a simple, even naive implementation, neglecting
efficiency considerations totally, instead focussing on correctness. Python has a
reputation of being an extremely productive programming language. Once you have
proven the correctness of this first version it can serve as a reference solution
to verify the correctness of later more efficient implementations. In addition,
the analysis of this version can highlight the sources of inefficiency and help
you focus your attention to the parts that really need it.

.. _timing-code:

1.5.1 Timing your code
^^^^^^^^^^^^^^^^^^^^^^
The simplest way to probe the efficiency of your code is to time it: write a simple script
and record how long it takes to execute. Let us first look at the structure of a Python script.

Here's a script (using the above structure) that computes the dot product of two long arrays
of random numbers.

.. code-block:: python

   """file et_dot/prof/run1.py"""
   import random
   from et_dot import dot

   def random_array(n=1000):
       """Create an array with n random numbers in [0,1[."""
       # Below we use a list comprehension (a Python idiom for creating a list from an iterable object).
       a = [random.random() for i in range(n)]
       return a

   if __name__=='__main__':
       a = random_array()
       b = random_array()
       print(dot(a,b))
       print('-*# done #*-')

We store this file, which we rather simply called :file:`run1.py`, e.g. in a directory
:file:`prof` where we intend to keep all our profiling work. You can execute the script
from the command line (with the project directory as the current working directory:

.. code-block:: bash

   (.venv) > python ./prof/run1.py
   251.08238559724717
   -*# done #*-

.. note:: As our script does not fix the random number seed, every run has a different outcome.

We are now ready to time our script. There are many ways to achieve this. Here is a
`particularly good introduction <https://realpython.com/python-timer/>`_. The
`et-stopwatch project <https://pypi.org/project/et-stopwatch/>`_ takes this a little
further. We add it as a development dependency (``-D``) of our project::

    (.venv) > poetry add et_stopwatch -D
    Using version ^0.3.0 for et_stopwatch
    Updating dependencies
    Resolving dependencies... (0.2s)
    Writing lock file
    Package operations: 1 install, 0 updates, 0 removals
      - Installing et-stopwatch (0.3.0)
    (.venv) >

A development dependency is a package that is not needed for using the package
at hand, bit only needed during development.

Using the :py:class:`Stopwatch` class to time pieces of code is simple:

.. code-block:: python

   """file et_dot/prof/run1.py"""
   from et_stopwatch import Stopwatch

   ...

   if __name__=='__main__':
       with Stopwatch(message="init"):
           a = random_array()
           b = random_array()
       with Stopwatch(message="dot "):
           dot(a,b)
       print('-*# done #*-')

When the script is exectuted the two ``with`` blocks will print the time it takes
to execytre their body. The first ``with`` block times the initialisation if the arrays,
and the second dot product computation.

.. code-block:: bash

   (.venv) > python ./prof/run1.py
   init: 0.000281 s
   dot : 0.000174 s
   -*# done #*-
   >

Note that the initialization phase took longer than the computation. Random number
generation is rather expensive.

.. _comparison-numpy:

1.5.2 Comparing to Numpy
^^^^^^^^^^^^^^^^^^^^^^^^
As said earlier, our implementation of the dot product is rather naive. If you want
to become a good programmer, you should understand that you are probably not the
first researcher in need of a dot product implementation. For most linear algebra
problems, `Numpy <https://numpy.org>`_ provides very efficient implementations.
Below the :file:`run1.py` script adds timing results for the Numpy_ equivalent of
our code.

.. code-block:: python

   """file et_dot/prof/run1.py"""
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
    :py:class:`list`, where every item can in fact point to an arbitrary Python object.
    Contiguous memory access is far more efficient. In addition, the memory footprint of
    a numpy array is significantly lower that that of a plain Python list.
*   The loop over Numpy_ arrays is implemented in a low-level programming languange.
    This allows to make full use of the processors hardware features, such as *vectorization*
    and *fused multiply-add* (FMA).

.. _conclusion:

1.6 Conclusion
--------------
There are three important generic lessons to be learned from this tutorial:

#.  Always start your projects with a simple and straightforward implementation which
    can be easily be proven to be correct, even if you know that it will not satisfy
    your efficiency constraints. You should use it as a reference to prove the correctness
    of future more efficient implementations.

#.  Write test code for proving correctness.

#.  Time your code to understand which parts are time consuming and which not. Optimize
    bottlenecks first and do not waste time optimizing code that does not contribute
    significantly to the total runtime. Optimized code is typically harder to read and
    may become a maintenance issue.

#.  Before you write code, in this case our dot product implementation, spent some time
    searching the internet to see what is already available. Especially in the field of
    scientific and high performance computing there are many excellent libraries available
    which are hard to beat. Use your precious time for new stuff. Consider adding new features
    to an existing codebase, rather than starting from scratch. It will gain you time,
    improve your programming skills. It might also give your code more visibility, and more
    users, because you provide them with and extra feature on top of something they are
    already used to.

