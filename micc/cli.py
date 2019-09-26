# -*- coding: utf-8 -*-

"""
Application micc
"""

import sys
from types import SimpleNamespace
from pathlib import Path

import click

import micc.commands as cmds
from micc.utils import module_exists
from micc import utils

__template_help =  "Ordered list of Cookiecutter templates, or a single Cookiecutter template."
__micc_file_help = ("Name of the micc-file in the cookiecutter templates (typically, ``micc.json``). "
                    "Micc does not use the standard ``cookiecutter.json`` file to provide the "
                    "template parameters, but uses a micc-file, usually named ``micc.json`` to "
                    "generate a ``cookiecutter.json`` file. Unlike the ``cookiecutter.json`` file, "
                    "the ``micc.json`` file can contain default values for the template parameters. "
                    "You will be prompted to provide a value for all parameters without default value. "
                    "The micc-file must be found in the template directory."
                   )
__overwrite_help = ("If specified, any existing files are overwritten without backup."
                    "Otherwise, micc will verify if there are existing files that"
                    "would be overwritten and gives you three options: \n\n"
                    "* abort,\n"
                    "* make backup files and continue, and \n"
                    "* continue without backup files. This is equivalent to specifying ``--overwrite``."
                   )
__structure_help = ("Create a python project structure ``<module_name>.py`` (``-s`` ``module``),"
                    " or ``<module_name>/__init__.py`` (``-s`` ``package``)."
                   )

@click.group()
@click.option('-v', '--verbosity', count=True
             , help="Verbosity of program output.")
@click.option('-p', '--project-path', default='.', type=Path
             , help="Path to the project directory.")
@click.option('--clear-log', is_flag=True, default=False
             , help="Clear the project's ``micc.log`` file.")
@click.pass_context
def main(ctx, verbosity, project_path, clear_log):
    """
    Micc command line interface. 
    
    See below for (sub)commands.
    """
    ctx.obj = SimpleNamespace( verbosity=verbosity
                             , project_path=project_path.resolve()
                             , clear_log=clear_log
                             )


@main.command()
@click.option('-T', '--template',   default=[], help=__template_help)
@click.option('-m', '--micc-file',  default='micc.json', help=__micc_file_help)
@click.option('-s', '--structure', type=click.Choice(['module','package']), default='package'
              , help=__structure_help)
@click.option('-n', '--allow-nesting',  is_flag=True, default=False
              , help="Allow to nest a project inside another project.")
@click.pass_context
def create( ctx
          , template
          , micc_file
          , structure
          , allow_nesting
          ):
    """
    Create a project skeleton. 
    
    The project name is taken to be the last directory of the *<project_path>*.
    The package name is the derived from the project name, taking the 
    `PEP8 module naming rules <https://www.python.org/dev/peps/pep-0008/#package-and-module-names>`_
    into account:
    
    * all lowercase.
    * dashes ``'-'`` and spaces ``' '`` replaced with underscores ``'_'``.
    * in case the project name has a leading number, an underscore is prepended ``' '``.
    
    If no *<project_path>* is provided, or if it is the same as the current working
    directory, the user is prompted to enter one. 
    
    Prompts the user for all entries in the micc-file file
    that do not have a default value.
    """
    if ctx.obj.project_path==Path.cwd():
        answer = click.prompt(f"Enter {click.style('[path/to/]',fg='yellow')} project_name\n"
                              f"(relative to CWD (={Path.cwd()}) or absolute)\n"
                              f"or just press Enter to cancel the command"
                             , default=''
                             , show_default=False
                             )
        if not answer:
            click.secho("Command cancelled",fg='red')
            return cmds.EXIT_CANCEL
        else:
            ctx.obj.project_path = ctx.obj.project_path / answer
    
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
        
    return cmds.micc_create( templates=template
                           , micc_file=micc_file
                           , global_options=ctx.obj
                           )


@main.command()
@click.argument('app_name',type=str)
@click.option('-T', '--template',   default='template-app'
             , help=__template_help)
@click.option('-m', '--micc-file',  default='micc.json', help=__micc_file_help)
@click.option('--overwrite', is_flag=True, default=False
             , help=__overwrite_help
             )
@click.pass_context
def app( ctx
       , app_name
       , template
       , micc_file
       , overwrite
       ):
    """
    Add an app (console script) with name *<app_name>* to the package. 
    
    *<app_name>* is also the name of the executable when the package is installed.
    The source code is in ``<project_name>/<package_name>/cli_<app_name>.py``. 
    """
    assert not utils.app_exists(ctx.obj.project_path, app_name), f"Project {ctx.obj.project_path.name} has already an app named {app_name}."
    ctx.obj.overwrite = overwrite
    return cmds.micc_app( app_name
                        , templates=template
                        , micc_file=micc_file
                        , global_options=ctx.obj
                        )


@main.command()
@click.argument('module_name', default='')
@click.option( '--f2py', is_flag=True, default=False
             , help='Create a f2py module.')
@click.option( '--cpp', is_flag=True, default=False
             , help='Create a C++ module.')
@click.option('-s', '--structure', type=click.Choice(['module','package']), default='module'
              , help=__structure_help)
@click.option( '--overwrite', is_flag=True, default=False
             , help=__overwrite_help
             )
@click.option( '-T', '--template',   default='', help=__template_help)
@click.option( '-m', '--micc-file',  default='micc.json', help=__micc_file_help)
@click.pass_context
def module( ctx
          , module_name
          , f2py, cpp, structure
          , template
          , micc_file
          , overwrite
          ):
    """
    Add a module with name *<module_name>* to the package (Python, Fortran, C++). 
    The source code is in 
    
    * *<module_name>.py* or <*module_name>/__init__.py* for python modules (depending on the *<structure>* parameter.
    * directory *f2py_<module_name>.py* for f2py extension modules (Fortran source code).
    * directory *cpp_<module_name>.py* for cpp extension modules (C++ source code).
    """
    assert not (cpp and f2py), "Flags '--f2py' and '--cpp' cannot be specified simultaneously."
    assert not module_exists(ctx.obj.project_path,module_name), f"Project {ctx.obj.project_path.name} has already a module named {module_name}."

    ctx.obj.structure = structure
    ctx.obj.overwrite = overwrite
    
    if f2py:
        if not template:
            template = 'template-module-f2py'
        return cmds.micc_module_f2py( module_name
                                    , templates=template
                                    , micc_file=micc_file
                                    , global_options=ctx.obj
                                    )
    elif cpp:
        if not template:
            template = 'template-module-cpp'
        return cmds.micc_module_cpp( module_name
                                   , templates=template
                                   , micc_file=micc_file
                                   , global_options=ctx.obj
                                   )
    else:
        if not template:
            template = 'template-module-py'
        return cmds.micc_module_py( module_name
                                  , templates=template
                                  , micc_file=micc_file
                                  , global_options=ctx.obj
                                  )


@main.command()
@click.option('-M','--major', is_flag=True, default=False
             , help='Increment the major version number component and set minor and patch components to 0.')
@click.option('-m','--minor', is_flag=True, default=False
             , help='Increment the minor version number component and set minor and patch component to 0.')
@click.option('-p','--patch', is_flag=True, default=False
             , help='Increment the patch version number component.')
@click.option('-r','--poetry-version-rule', help='Increment the version number using the poetry command ``poetry version <rule>``.'
             , type=click.Choice(['','patch', 'minor', 'major'
                                 , 'prepatch', 'preminor'
                                 , 'premajor', 'prerelease'])
             )
@click.option('-t', '--tag',  is_flag=True, default=False
             , help='Create a git tag for the new version, and push it to the remote repo.')
@click.pass_context
def version( ctx
           , major
           , minor
           , patch
           , poetry_version_rule
           , tag
           ):
    """
    Increment the project's version number, or just show the current version number 
    if no arguments were given.
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
    return_code = cmds.micc_version(rule, global_options=ctx.obj)
    if return_code==0 and tag:
        return cmds.micc_tag(global_options=ctx.obj)
    else:
        return return_code


@main.command()
@click.pass_context
def tag(ctx):
    """
    Create a git tag for the current version and push it to the remote repo. 
    """
    return cmds.micc_tag(global_options=ctx.obj)


@main.command()
@click.option('-m','--module', default=''
             , help="Build only this module. The prefix [``cpp_``, ``f2py_``] may be omitted.")
@click.option('-s', '--soft-link', is_flag=True, default=False
             , help="Create a soft link rather than a copy of the extension library.")
@click.pass_context
def build(ctx, module, soft_link):
    """
    Build binary extension libraries (f2py and cpp modules). 
    """
    return cmds.micc_build( module_to_build=module
                          , soft_link=soft_link
                          , global_options=ctx.obj
                          )


@main.command()
@click.option('--overwrite', is_flag=True, default=False
             , help="If True, any existing files are overwritten without backup."
                    "If False, micc verifies if there are existing files that"
                    "would be overwritten and gives you three options: abort, "
                    "continue with backup files, and continue without backup "
                    "files. The latter is equivalent to specifying overwrite=True."
             )
@click.pass_context
def convert_to_package(ctx, overwrite):
    """
    Convert a Python module project to a package.

    A Python *module* project has only a ``<package_name>.py`` file, whereas
    a Python *package* project has ``<package_name>/__init__.py``.
    Only the latter can contain submodules, such as python modules or packages 
    and binary extension modules, and applications.

    This also expands the ``micc-template-general-docs`` template in this project,
    which adds a AUTHORS.rst, HISTORY.rst and installation.rst to the documentation 
    structure.
    """
    ctx.obj.overwrite = overwrite
    return cmds.micc_convert_simple(global_options=ctx.obj)


@main.command()
@click.option('-h', '--html', is_flag=True, default=False
             , help="Request building html documentation.")
@click.option('-l', '--latexpdf', is_flag=True, default=False
             , help="Request building pdf documentation.")
@click.pass_context
def docs(ctx, html, latexpdf):
    """
    Generate documentation for the project using Sphinx.
    """    
    formats = []
    if html:
        formats.append('html')
    if latexpdf:
        formats.append('latexpdf')
    
    return cmds.micc_docs(formats, global_options=ctx.obj)


@main.command()
@click.pass_context
def info(ctx):
    """
    Show info on the project. Use verbosity to produce more detailed info.
    """    
    return cmds.micc_info(global_options=ctx.obj)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover