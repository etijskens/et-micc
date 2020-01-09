Tutorial 4: Version control and version management
==================================================

4.1 Git support
---------------
When you create a new project, Micc_ immediately provides a local git_ repository for 
you and commits the initial files Micc_ set up for you. If you have a github_ account you
can register it in the preferences file :file:`~/.micc/micc.json`, using the 
``github_username`` entry::

   {
   ...
   , "github_username"  : {"default":"etijskens"
                          ,"text"   :"your github username"
                          }
   ...
   }

Micc_ cannot create a remote `github <https://github.com>`_ repository for you, 
but if you registered your github_ username in the preferences file, it will add 
a remote origin at ``https://github.com/etijskens/<your_project_name>/``, and
try to push the files to the github_ repo. If you have created the remote repository 
before you create the project, the new project will be immediately pushed onto
the remote origin. Otherwise, you get a warning that the remote repository does not
yet exist. You can create the remote repository whenever you like and push your work
onto the remote repository using the git_ CLI. 

4.2 Version management
----------------------
Version numbers are practical, even for a small software project used only by 
yourself. For larger projects, certainly when other users start using them, 
they become indispensable. When giving version numbers to a project, we highly
recommend to follow the guidelines `Semantic Versioning 2.0 <https://semver.org>`_.
Such a version number consists of ``Major.minor.patch``. According to 
semantic versioning you should increment the:

* ``Major`` version when you make incompatible API changes,
* ``minor`` version when you add functionality in a backwards compatible manner, and
* ``patch`` version when you make backwards compatible bug fixes.

Micc_ sets a version number of 0.0.0 when it creates a project, and you can bump the 
version number at any time with the ``micc version`` command.

.. code-block:: bash

   > micc info
   Project ET-dot located at /Users/etijskens/software/dev/workspace/ET-dot
     package: et_dot
     version: 0.0.0
     structure: et_dot/__init__.py (Python package)
     contents:
       application cli_dot_files.py
       C++ module  cpp_dotc/dotc.cpp
       f2py module f2py_dotf/dotf.f90

To bump the patch component:
       
.. code-block:: bash

   > micc version
   Project (ET-dot version (0.0.0)
   > micc version --patch
   [INFO]           bumping version (0.0.0) -> (0.0.1)

Again, with the short version of ``--patch`` and verbose this time, :
   
.. code-block:: bash

   > micc -vv version -p
   [DEBUG] start = 2019-10-16 13:18:16.995416
   [INFO]           bumping version (0.0.1) -> (0.0.2)
   [DEBUG]          . Updated (/Users/etijskens/software/dev/workspace/ET-dot/pyproject.toml)
   [DEBUG]          . Updated (/Users/etijskens/software/dev/workspace/ET-dot/et_dot/__init__.py)
   [DEBUG] stop  = 2019-10-16 13:18:17.261962
   [DEBUG] spent = 0:00:00.266546   
   
Here, you can see that micc_ updated the version number in :file:`ET-dot/pyproject.toml` 
and :file:`ET-dot/et_dot/__init__.py`.

To bump the minor component use the ``--minor`` or ``-m`` flag:

.. code-block:: bash

   > micc version -m
   [INFO]           bumping version (0.0.2) -> (0.1.0)

As you can see the patch component is reset to 0.

To bump the major component use the ``--major`` or ``-M`` flag:

.. code-block:: bash

   > micc version -M
   [INFO]           bumping version (0.1.0) -> (1.0.0)

As you can see the minor component (as well as the patch component) is reset to 0.

The version number has a ``--tag`` flag that creates a git_ tag (see
https://git-scm.com/book/en/v2/Git-Basics-Tagging) and trys

.. code-block:: bash

   > micc -vv version -p --tag
   [DEBUG] start = 2019-10-16 13:37:25.026161
   [INFO]           bumping version (1.0.1) -> (1.0.2)
   [DEBUG]          . Updated (/Users/etijskens/software/dev/workspace/ET-dot/pyproject.toml)
   [DEBUG]          . Updated (/Users/etijskens/software/dev/workspace/ET-dot/et_dot/__init__.py)
   [INFO]           Creating git tag v1.0.2 for project ET-dot
   [DEBUG]          Running 'git tag -a v1.0.2 -m "tag version 1.0.2"'
   [DEBUG]
   [DEBUG]          Pushing tag v1.0.2 for project ET-dot
   [DEBUG]          Running 'git push origin v1.0.2'
   [DEBUG]          remote: Repository not found.
                      fatal: repository 'https://github.com/etijskens/ET-dot/' not found
   [INFO]           Done.
   [DEBUG] stop  = 2019-10-16 13:37:26.101959
   [DEBUG] spent = 0:00:01.075798
   
If you created a remote github_ repository for your project and registered
your github_ username in the preferences file, the tag is pushed to the remote origin.