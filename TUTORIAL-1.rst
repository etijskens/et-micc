Tutorial 1: a simple project
============================

Let's start with a simple problem. Let's try to make a Python module that 
computes the dot product of two arrays. This not a very rewarding goal, as 
there are already Python packages, e.g. Numpy, that solve this problem in
an elegant and efficient way. Yet because the dot product is such a simple
concept in linear algebra, it allows us to illustrate the usefulness of 
Python as a language for High Performance computing, as well as the capabilities
of *micc*.

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
 *Micc* will help you publishing your work at `PyPI <https://pypi.org>`_  with 
 as little effort as possible.



So, let us call the project *ET-dot*. *ET* stands for my initials, which helps 
to be unique, remains descriptive, and is certainly short. First, ``cd`` into a 
directory that you want to use as a workspace for storing your Python projects 
(I am using ``~/software/dev/workspace``). Then ask *micc* to create a project, 
like this:

.. code-block:: bash

   > cd ~/software/dev/workspace

   [INFO]      Creating project (ET-dot):
   INFO             Python module (et_dot): structure = (ET-dot/et_dot.py)
   INFO             Creating git repository
   INFO             done.
   INFO         done.   
   >

From the first output line we can tell that *micc* has created a project ``ET-dot``,
as we requested after the ``-p`` option (which is short for ``--project-path``).

The second output line tells us two things. First, inside the project directory 
``ET-dot`` a Python module ``et_dot.py`` was created, as requested by the 
``--structure module`` option. A module is the simplest 
Python project we can create. It is meant for rather small projects that fit in
a single file. More complex projects have a package structure, that is a directory 
with the same name as the module, i.e. ``et_dot``, containing a ``__init__.py`` file
which marks the directory as a Python Package and contains the statements that are
executed when the module is imported. Fortunately, you don't have to know in advance
whether your project will grow big, as *micc* can convert your module project into 
a package project at any time. On the other hand, *micc* comes in especially handy 
for larger projects and hence the default structure is ``package``. Secondly, you 
should notice that the name of that module is not exactly the name that we choose 
for our project. The reason why *micc* decided to rename the module, is that our 
project name ``ET-dot`` does not comply with the 
`PEP8 module naming rules <https://www.python.org/dev/peps/pep-0008/#package-and-module-names>`_.
To make it compliant, it replaced all capitals with lowercase, and all spaces ``' '``
and dashes ``'-'`` with underscores ``'_'``. If you want to avoid this, you must 
choose a *PEP8* compliant name for your project from the beginning.

Then there is a line that reminds us that your new project is ready for documentation
generation with `Sphinx <sphinx.org>`_. Of course, you'll have to writ the documentation
yourself, but it will be almost effortlessly and beautifully structured by *sphinx*.

The next line reminds us that there is a ``tests`` directory where you can conveniently
place your tests to make sure that during development, your module works as expected.
The recommended tool for this is `pytest <https://docs.pytest.org>`_ .

And, finally, it is mentioned that a `git <https://git-scm.com/>`_ repository is 
created. *Git* is a version control system. Version control solves many practical
problems. E.g. it provides a backup of every version that was committed (by you or
anyone of the development team) over the course of your project. It also lets you
work on different features of your code without letting them interfere with eachother. 

The project path (``-p path``) is a variable that is accepted by all *micc* commands.
Its default value is the current directory. So, once the project is created it is
convenient to ``cd`` into it and you can leave out the ``-p`` option:

.. code-block:: bash

   > cd ET-dot
   > micc info
   Project ET-dot located at /Users/etijskens/software/dev/workspace/ET-dot
     package: et_dot
     version: 0.0.0
     structure: et_dot.py (Python module)

That works even with the ``micc create`` command: We could also have created our 
project like this:

.. code-block:: bash

   > mkdir ET-dot
   > cd ET-dot
   > micc create --structure module
   ...
   
To get a bit of an idea of what *micc* did for us, you can ask a tree listing of
the project directory (the listing below only show the interesting files and 
directories):

.. code-block:: bash
   
   > tree ET-dot/
   ET-dot/
   ├── .git
   │   └── ...
   ├── .gitignore
   ├── API.rst
   ├── LICENSE
   ├── Makefile
   ├── README.rst
   ├── docs
   │   ├── Makefile
   │   ├── api.rst
   │   ├── conf.py
   │   ├── index.rst
   │   └── readme.rst
   ├── et_dot.py
   ├── micc.log
   ├── pyproject.toml
   └── tests
       ├── __init__.py
       └── test_et_dot.py   

* The **module** itself, ``et_dot.py`` - This file will contain the python code that will 
  compute the dot product.
* The **license** file - There is a very liberal ``LICENSE`` file, which is useful when you 
  want to publish your code.
* **Documentation** files - The boilerplate code is in the ``docs`` directory. You will
  only rarely need to touch the files in there. Then there are a number of ``.rst``
  files with capitalized names, like ``README.rst`` and ``API.rst``. These are in 
  `reStructuredText <https://devguide.python.org/documenting/#restructuredtext-primer>`_ 
  format. ``README.rst`` contains an overview of the project, while ``API.rst`` 
  describes the classes and methods of the project in detail. The way this is set up 
  is that *sphinx* retrieves these descriptions automatically from the doc-strings of 
  modules, classes and methods. The documentation is generated as html or a pdf, with 
  the commands:
  
.. code-block:: bash

   > cd docs 
   > make html
   > make latexpdf
   

* **Test code** - in the ``tests`` directory you will find a ``test_<component>.py`` file
  for every component in your project. At this point there is only one component,
  the *et_doc* module, and thus there is a ``test_et_dot.py`` file. The ``__init__.py``
  ensures that the ``tests`` directory itself can be recognized as a module and thus
  can be imported. All tests are conveniently run as:
  
.. code-block:: bash

   > pytest tests   
  
* The **git repository** - the directory ``.git`` contains the entire history of all the 
  versions of your code that you (or your team) committed. The file ``.gitignore`` lists
  the files and directory that should not end up in the repository.
  
* The **Makefile** - this contains a number of actions for which other tools than *micc*
  are useful. We'll come to those later.
  
* The **log file** ``micc.log`` - all *micc* commands leave a trace in this file, So you
  can look up what happened when to your project.
  
* **Pyproject.toml** a description of the build system requirements of the project. See 
  `PEP 518 <https://www.python.org/dev/peps/pep-0518/>`_. This is a rather new but *imho*
  promising concept. Not many tools are available that make use of it. Currently,
  `poetry <https://poetry.eustace.io>`_ seems to be the most actively developed, and *micc*
  has some support for it. There is also `flit <https://github.com/takluyver/flit>`_.
  
Your first code
---------------
Our module file ``et_dot.py`` looks as follows.

.. code-block:: python

   # -*- coding: utf-8 -*-
   """
   Package et_dot
   =======================================
   
   """
   __version__ = "0.0.0"
   
   # Your code here...
   
Open it in your favourite editor and change it as follows:

.. code-block:: python

   # -*- coding: utf-8 -*-
   """
   Package et_dot
   ==============
   Python module for computing the dot product of two arrays.
   """
   __version__ = "0.0.0"
   
   
   def dot(a,b):
       """computes the dot product of *a* and *b*
       
       :param a: a 1D array.
       :param b: a !D array of the same lenght as *a*.
       :returns: the dot product of *a* and *b*.
       """
       n = len(a)
       if len(b)!=n:
           raise ArithmeticError("dot(a,b) requires len(a)==len(b).")
       d = 0 
       for i in range(n):
           d += a[i]*b[i]
       return d

Then open the file ``tests/test_et_dot.py`` and 

