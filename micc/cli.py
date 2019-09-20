# -*- coding: utf-8 -*-

"""
Application micc
================

``micc`` is a console application for creating and modifying Python project 
skeletons written around poetry and cookiecutter. 

Usage
*****

.. code-block:: bash

   > micc [global options] command [command options]

Global options
**************

* ``-v``, ``--verbose``: produce somewhat more output.

Commands
********

create
++++++

Create a skeleton for a new Python project, with useful contents. The user
is prompted for parameter with an empty default in the micc-file::
    
   > micc create [OPTIONS] [PROJECT_NAME]

``PROJECT_NAME`` is optional

Options:
  -o, --output-dir   location of the new project, defaults to current directory
  -T, --template     specify a non-default Python package cookiecutter template 
  -m, --micc-file    specify a non-default micc-file for the cookiecutter template
  --help             Show help
  
This is what the project skeleton looks like:

.. code-block:: bash
    
   > micc create my-package
   > tree
   my-package
   ├── API.rst
   ├── AUTHORS.rst
   ├── HISTORY.rst
   ├── LICENSE
   ├── Makefile
   ├── README.rst
   ├── docs
   │   ├── Makefile
   │   ├── api.rst
   │   ├── apps.rst
   ├── authors.rst
   │   ├── conf.py
   │   ├── history.rst
   │   ├── index.rst
   │   ├── installation.rst
   │   └── readme.rst
   ├── my_package
   │   └── __init__.py
   ├── pyproject.toml
   ├── requirements.txt
   └── tests
       ├── __init__.py
       └── test_my_package.py
       
app
+++

Adds an app (console script) to the package, as well as a test script for it.

.. code-block:: bash
   
   > micc app [OPTIONS] [APP_NAME]

The name of the app ``APP_NAME`` is prompted for if omitted.

Options:
  -P, --project_path location of the project to add an app to (current directory by default).
  -T, --template     specify a non-default Python package cookiecutter template.
  -m, --micc-file    specify a non-default micc-file for the cookiecutter template.
  --help             Show help

This command adds the following files to the project tree::

    ├── APPS.rst
    ├── my_pacakage
    │   └── cli_my_app.py
    └── tests
        └── test_cli_my_app.py

module
++++++

Adds a module to the package, as well as a test script for it. By default a Python
module is created, but a f2py or C++ module can be created by specifying ``--f2py``
or ``--cpp`` as a command line option.

.. code-block:: bash
   
   > micc module [OPTIONS] [MODULE_NAME]

The name of the module ``MODULE_NAME`` is prompted for if omitted.

Options:
  -P, --project_path location of the project to add an app to (current directory by default).
  --f2py             add an f2py module, rather than a Python module to the package.
  --cpp              add a C++ module, rather than a Python module to the package.
  -T, --template     specify a non-default cookiecutter template.
  -m, --micc-file    specify a non-default micc-file for the cookiecutter template.
  --help             Show help

This command adds the following files to the project tree::

    ├── my_pacakage
    │   └── my_module.py
    └── tests
        └── test_my_module.py

If the ``--f2py`` flag is added the added files are:: 

    ├── my_pacakage
    │   ├── build_my_module_f2py.sh
    │   ├── my_module_f2py.f90
    │   └── my_module_f2py.rst
    └── tests
        └── test_my_module_f2py.py

If the ``--cpp`` flag is added the added files are:: 

    todo

version
+++++++

Bump the version of a project::

    > micc version [OPTIONS] [PROJECT_PATH]

``PROJECT_PATH`` refers to the projech in current directory if ommitted.

Options:
  -M, --major                   increment major version number component
  -m, --minor                   increment minor version number component
  -p, --patch                   increment patch version number component
  -r, --poetry-version-rule     a ``poetry version <rule>``: either patch 
                                | minor | major | prepatch | preminor 
                                | premajor| prerelease.
  -t, --tag                     if True, create a git tag for the new
                                version, and push it. See the tag command.
  --help                        Show help message.
  
tag
+++

Create a git tag for the current version in the project at ``PROJECT_PATH`` 
and push it::

    > micc tag [OPTIONS] [PROJECT_PATH]

``PROJECT_PATH`` refers to the projech in current directory if ommitted.

Options:
  --help                        Show help message.

build
+++++

Build all binary extensions::

    > micc build [OPTIONS] [PROJECT_PATH]

Options:
    --soft-link, -s             add a soft link to the extension library, rather than a copy.
"""

import sys,os
from types import SimpleNamespace

import click

from micc.commands import micc_create, micc_version, micc_tag, micc_app, \
                          micc_module_py, micc_module_f2py, micc_module_cpp, \
                          micc_build, micc_convert_simple
                          
from micc.utils import module_exists
from micc import utils


@click.group()
@click.option('-v', '--verbose', count=True)
# @click.option('-q', '--quiet'  , is_flag=True, default=False
#              , help="Prompts the use for confirmation on most actions.")
@click.pass_context
def main(ctx, verbose):
    """
    Micc command line interface. Type ``micc --help`` on the command line for details.
    """
    ctx.obj = SimpleNamespace(verbose=verbose)


@main.command()
@click.argument('project_name')
@click.option('-o', '--output-dir', default='.', help="location of the new project")
@click.option('-T', '--template',   default=[]
              , help="ordered list Python package cookiecutter templates, or a single template")
@click.option('-m', '--micc-file',  default='micc.json'
              , help="name of the micc-file in the cookiecutter templates")
@click.option('-s', '--structure', type=click.Choice(['module','package']), default='package'
              , help="create a python project structure ``<module_name>.py`` (module),"
                     " or ``<module_name>/__init__.py`` (package).")
@click.option('-n', '--allow-nesting',  is_flag=True, default=False
              , help="allow to nest a project inside another project.")
@click.pass_context
def create( ctx
          , output_dir
          , project_name
          , template
          , micc_file
          , structure
          , allow_nesting
          ):
    """
    Create a project skeleton. Prompts the user for all entries in the micc.json file
    that do not have a default.
    
    :param str project_name: name of the project to be created. Current directory if 
        omitted.
    """
    if not template: # default, empty list
        if structure=='module':
            template = ['template-package-base'
                       ,'template-package-simple'
                       ,'template-package-simple-docs'
                       ]
        else:
            template = ['template-package-base'
                       ,'template-package-general'
                       ,'template-package-simple-docs'
                       ,'template-package-general-docs'
                       ]
    else:
        # ignore structure
        structure = 'user-defined'
        
    ctx.obj.structure = structure
    ctx.obj.allow_nesting = allow_nesting
        
    return micc_create( project_name
                      , output_dir=output_dir
                      , templates=template
                      , micc_file=micc_file
                      , global_options=ctx.obj
                      )


@main.command()
@click.argument('app_name', default='')
@click.option('-p', '--project_path', default='.'
             ,help="path to project directory")
@click.option('-T', '--template',   default='template-app'
             , help="ordered list Python package cookiecutter templates, or a single template")
@click.option('-m', '--micc-file',  default='micc.json'
              , help="name of the micc-file in the cookiecutter templates")
@click.option('--overwrite', is_flag=True, default=False
             , help="If True, any existing files are overwritten without backup."
                    "If False, micc verifies if there are existing files that"
                    "would be overwritten and gives you three options: abort, "
                    "continue with backup files, and continue without backup "
                    "files. The latter is equivalent to specifying overwrite=True."
             )
@click.pass_context
def app( ctx
       , app_name
       , project_path
       , template
       , micc_file
       , overwrite
       ):
    """
    ``micc app`` subcommand, add an app (console script) to the package. 
    
    :param str app_name: name of the cli application to be added to the package.
    """
    assert not utils.app_exists(project_path, app_name), f"Project {os.path.basename(project_path)} has already an app named {app_name}."
    ctx.obj.overwrite = overwrite
    return micc_app( app_name
                   , project_path=project_path
                   , templates=template
                   , micc_file=micc_file
                   , global_options=ctx.obj
                   )


@main.command()
@click.argument('module_name', default='')
@click.option( '-P', '--project_path', default='.'
             , help="path to project." )
@click.option( '--f2py', is_flag=True, default=False
             , help='create a f2py module.')
@click.option( '--cpp', is_flag=True, default=False
             , help='create a C++ module.')
@click.option('--simple/--no-simple',  default=True
              , help="create a simple or a general python model (ignored if "
                     " --cpp or --f2py are specified)."
              )
@click.option( '--overwrite', is_flag=True, default=False
             , help="If True, any existing files are overwritten without backup."
                    "If False, micc verifies if there are existing files that"
                    "would be overwritten and gives you three options: abort, "
                    "continue with backup files, and continue without backup "
                    "files. The latter is equivalent to specifying overwrite=True."
             )
@click.option( '-T', '--template',   default=''
              , help="ordered list Python package cookiecutter templates, or a single template")
@click.option( '-m', '--micc-file',  default='micc.json'
             , help="the micc-file for the cookiecutter template")
@click.pass_context
def module( ctx
          , module_name
          , project_path
          , f2py, cpp, simple
          , template
          , micc_file
          , overwrite
          ):
    """
    ``micc module`` subcommand, add a module to the package. 
    
    :param str module_name: name of the module to be added to the package.
    """
    assert not (cpp and f2py), "Flags '--f2py' and '--cpp' cannot be specified simultaneously."
    assert not module_exists(project_path,module_name), f"Project {os.path.basename(project_path)} has already a module named {module_name}."

    ctx.obj.overwrite = overwrite
    
    if f2py:
        if not template:
            template = 'template-module-f2py'
        return micc_module_f2py( module_name
                               , project_path=project_path
                               , templates=template
                               , micc_file=micc_file
                               , global_options=ctx.obj
                               )
    elif cpp:
        if not template:
            template = 'template-module-cpp'
        return micc_module_cpp( module_name
                              , project_path=project_path
                              , templates=template
                              , micc_file=micc_file
                              , global_options=ctx.obj
                              )
    else:
        if not template:
            template = 'template-module-py'
        return micc_module_py( module_name
                             , project_path=project_path
                             , simple=simple
                             , templates=template
                             , micc_file=micc_file
                             , global_options=ctx.obj
                             )


@main.command()
@click.argument('project_path', default='.')
@click.option('-M','--major', is_flag=True, default=False
             , help='increment major version number component')
@click.option('-m','--minor', is_flag=True, default=False
             , help='increment minor version number component')
@click.option('-p','--patch', is_flag=True, default=False
             , help='increment patch version number component')
@click.option('-r','--poetry-version-rule', help='a "poetry version <rule>"'
             , type=click.Choice(['','patch', 'minor', 'major'
                                 , 'prepatch', 'preminor'
                                 , 'premajor', 'prerelease'])
             )
@click.option('-t', '--tag',  is_flag=True, default=False
             , help='if True, create a git tag for the new version, and push it')
@click.pass_context
def version(ctx, project_path, major, minor, patch, poetry_version_rule, tag):
    """
    ``micc version`` subcommand, similar to ``poetry version``. Increments the
    project's version number. 
    """
    rule = None
    if poetry_version_rule:
        rule = poetry_version_rule
    if patch:
        rule = 'patch'
    if minor:
        rule = 'minor'
    if major:
        rule = 'major'
    return_code = micc_version(project_path, rule, global_options=ctx.obj)
    if return_code==0 and tag:
        return micc_tag(project_path, global_options=ctx.obj)


@main.command()
@click.argument('project_path', default='.')
@click.pass_context
def tag(ctx, project_path):
    """
    ``micc tag`` subcommand, create a git tag for the current version. 
    """
    return micc_tag(project_path, global_options=ctx.obj)


@main.command()
@click.argument('project_path', default='.')
@click.option('-m','--module', default=''
             , help="Build only this module. The prefix ['cpp_','f2py'] may be omitted.")
@click.option('-s', '--soft-link', is_flag=True, default=False
             , help="Create a soft link rather than a copy of the extension library.")
@click.pass_context
def build(ctx, project_path, module, soft_link):
    """
    ``micc build`` subcommand, builds all binary extension libraries (f2py and C++ modules. 
    """
    return micc_build( project_path=project_path
                     , module_to_build=module
                     , soft_link=soft_link
                     , global_options=ctx.obj
                     )


@main.command()
@click.argument('project_path', default='.')
@click.option('--overwrite', is_flag=True, default=False
             , help="If True, any existing files are overwritten without backup."
                    "If False, micc verifies if there are existing files that"
                    "would be overwritten and gives you three options: abort, "
                    "continue with backup files, and continue without backup "
                    "files. The latter is equivalent to specifying overwrite=True."
             )
@click.pass_context
def convert_simple(ctx, project_path, overwrite):
    """
    ``micc convert_simple`` subcommand, convert a simple python package
    (created as ``micc create <module_name> --simple``) to a general python package. 
    """
    ctx.obj.overwrite = overwrite
    return micc_convert_simple(project_path, global_options=ctx.obj)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
