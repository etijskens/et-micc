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

Adds a module to the package, as well as a test script for it.

.. code-block:: bash
   
   > micc module [OPTIONS] [MODULE_NAME]

The name of the module ``MODULE_NAME`` is prompted for if omitted.

Options:
  -P, --project_path location of the project to add an app to (current directory by default).
  -f, --f2py         add an f2py module, rather than a python module to the package.
  -T, --template     specify a non-default Python package cookiecutter template.
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
    │   └── my_module_f2py.f90
    └── tests
        └── test_my_module_f2py.py

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
"""
#===============================================================================
import sys
import click
from micc.commands import micc_create, micc_version, micc_tag, micc_app, micc_module, micc_module_f2py
from types import SimpleNamespace
#===============================================================================
@click.group()
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.option('-q', '--quiet'  , is_flag=True, default=False
             , help="Prompts the use for confirmation on most actions.")
@click.pass_context
def main(ctx, verbose, quiet):
    """
    Micc command line interface. Type ``micc --help`` on the command line for details.
    """
    ctx.obj = SimpleNamespace(verbose=verbose, quiet=quiet)
#===============================================================================
@main.command()
@click.argument('project_name',     default='')
@click.option('-o', '--output-dir', default='.', help="location of the new project")
@click.option('-T', '--template',   default='micc-package'
              , help="a Python package cookiecutter template")
@click.option('-m', '--micc-file',  default='micc.json'
              , help="the micc-file for the cookiecutter template")
@click.pass_context
def create( ctx
          , output_dir
          , project_name
          , template, micc_file
          ):
    """
    Create a project skeleton. Prompts the user for all entries in the micc.json file
    that do not have a default.
    
    :param str project_name: name of the project to be created. Current directory if 
        omitted.
    """
    return micc_create( project_name
                      , output_dir=output_dir
                      , template=template
                      , micc_file=micc_file
                      , global_options=ctx.obj
                      )
#===============================================================================
@main.command()
@click.argument('app_name', default='')
@click.option('-P', '--project_path', default='')
@click.option('-T', '--template',   default='micc-app'
              , help="a Python package cookiecutter template")
@click.option('-m', '--micc-file',  default='micc.json'
              , help="the micc-file for the cookiecutter template")
@click.pass_context
def app( ctx
       , app_name
       , project_path
       , template, micc_file
       ):
    """
    ``micc app`` subcommand, add an app (console script) to the package. 
    
    :param str app_name: name of the cli application to be added to the package.
    """
    return micc_app( app_name
                   , project_path
                   , template=template
                   , micc_file=micc_file
                   , global_options=ctx.obj
                   )
#===============================================================================
@main.command()
@click.argument('module_name', default='')
@click.option( '-P', '--project_path', default='')
@click.option( '--f2py', is_flag=True, default=False
             , help='create an f2py module.')
@click.option( '-T', '--template',   default='micc-module'
            , help="a Python package cookiecutter template")
@click.option( '-m', '--micc-file',  default='micc.json'
             , help="the micc-file for the cookiecutter template")
@click.pass_context
def module( ctx
          , module_name
          , project_path
          , f2py
          , template, micc_file
          ):
    """
    ``micc module`` subcommand, add a module to the package. 
    
    :param str module_name: name of the module to be added to the package.
    """
    if f2py:
        return micc_module_f2py( module_name
                               , project_path
                               , template=template + '-f2py'
                               , micc_file=micc_file
                               , global_options=ctx.obj
                               )
    else:
        return micc_module( module_name
                          , project_path
                          , template=template
                          , micc_file=micc_file
                          , global_options=ctx.obj
                          )
#===============================================================================
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
#===============================================================================
@main.command()
@click.argument('project_path', default='.')
@click.pass_context
def tag(ctx, project_path):
    """
    ``micc tag`` subcommand, create a git tag for the current version. 
    """
    return micc_tag(project_path, global_options=ctx.obj)
#===============================================================================
if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
#===============================================================================
