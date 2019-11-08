Starting a new project
----------------------
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

So, let us call the project *ET-dot*. *ET* stands for my initials, which helps 
to be unique, remains descriptive, and is certainly short. First, ``cd`` into a 
directory that you want to use as a workspace for storing your Python projects 
(I am using ``~/software/dev/workspace``). Then ask micc_ to create a project, 
like this:

.. code-block:: bash

   > cd ~/software/dev/workspace
   > micc -p ET-dot create

The ``-p`` option (which is short for ``--project-path``) tells micc_ where we 
want the project to be created. Here, we request a project directory :file:`ET-dot` in 
the current working directory, i.e. :file:`~/software/dev/workspace`. The ``--module``
requests the creation of a simple Python module, rather than a Python package (a
directory with an :file:`__init__.py` file. A module structure is basically a single 
file project, whereas a package structure allows for many different source files,
including applications (console scripts), python submodules and binary extension 
modules written in Fortran or C++. As micc can easily convert a module structure to
a package structure, It is easier to start out with a 

Let' take a look at the output of the *micc create* command: 
 
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
To make it compliant, it replaced all capitals with lowercase, and all spaces ``' '``
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
information about how micc_ plays with git_ in *Tutorial 4*.

Modules and packages
^^^^^^^^^^^^^^^^^^^^

   A *Python module* is the simplest Python project we can create. It is meant for rather
   small projects that fit in a single file. More complex projects have a *package*
   structure, that is, a directory with the same name as the module, i.e. :file:`et_dot`,
   containing a :file:`__init__.py` file. The :file:`__init__.py` file marks the 
   directory as a Python *package* and contains the statements that are executed when
   the module is imported. The *module* structure is the default structure. When creating
   a project you can opt for a *package* structure by appending the flag ``-p`` or 
   ``--package`` to the ``micc creatte`` command: 

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

The project path
^^^^^^^^^^^^^^^^

   The project path (``-p path``) is a variable that is accepted by all micc_ commands.
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
   
Note that micc_ creates fully functional examples, complete with test code and 
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

Generate documentation
^^^^^^^^^^^^^^^^^^^^^^
   You can generate (using `sphinx <http://www.sphinx-doc.org/en/master/>`_)
   the documentation for the project like this:
   
   .. code-block:: bash
   
      > cd docs
      > make html
      
   Next, open the file :file:`ET-dot/docs/_build/html/index.html` in your browser to 
   see a page like below:
   
   .. image:: ../tutorials/tutorial-1/im1.png
   
   If your expand the **API** tab on the left, you get to see the :py:mod:`et_dot`
   module documentation, as it generated from the doc-strings:
   
   .. image:: ../tutorials/tutorial-1/im2.png
   
   A pdf can be generated as:
   
   .. code-block:: bash
   
      > make latexpdf
   
   You will find the result in :file:`docs/_build/ET-dot.pdf`. 
  
   Documentation is almost completely generated automatically from  using *sphinx* 
   and `autodoc <???>`_ extension. Thus, if you take good care writing doc-strings,
   the documentation follows. 
   
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
   modified as necessary, so that *sphinx* is able find the doc-strings. Even for 
   command line interfaces (CLI, or console scripts) based on `click <???>`_ the
   documentation is generated neatly from the :py:obj:`help` strings of options and 
   the doc-strings of the commands.

Running tests
^^^^^^^^^^^^^

   The tests for this module are in file :file:`ET-dot/tests/test_et_dot.py`. Let's
   take a look at the relevant section:

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
                
      # ... some omissions irrelevant for the tutorial ...  
   
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
   it collected (1). *Pytest* looks for test methods in all :file:`test_*.py` or 
   :file:`*_test.py` files in the current directory and accepts ``test`` prefixed methods 
   outside classes and ``test`` prefixed methods inside ``Test`` prefixed classes as test 
   methods to be executed.
   
   Other testing frameworks are 
   
   * `unittest <https://docs.python.org/3/library/unittest.html>`_,
   * `nose <https://nose.readthedocs.io/en/latest/>`_, 
   * `hypothesis <https://hypothesis.readthedocs.io/en/latest/>`_,
   * ...
   
License file
^^^^^^^^^^^^
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
    
Pyproject.toml
^^^^^^^^^^^^^^
   The file :file:`pyproject.toml` (located in the project directory) is the 
   modern way to describe the build system requirements of the project: 
   `PEP 518 <https://www.python.org/dev/peps/pep-0518/>`_. This is a rather new 
   but *imho* promising concept. Not many tools are available that make use of it. 
   Currently, `poetry <https://poetry.eustace.io>`_ seems to be the most actively 
   developed, and micc_ has some support for it. There is also 
   `flit <https://github.com/takluyver/flit>`_.
  
Makefile
^^^^^^^^
   The :file:`makefile` contains a number of recipes for actions for which other 
   tools than micc_ are useful. We'll come to those later.

Micc.log
^^^^^^^^
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

