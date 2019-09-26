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


@click.group()
@click.option('-v', '--verbosity', count=True
             , help="verbosity of program output.")
@click.option('-p', '--project-path', default='.', type=Path
             , help="Path to project directory")
@click.option('--clear-log', is_flag=True, default=False
             , help="Clear the project's micc.log file.")
@click.pass_context
def main(ctx, verbosity, project_path, clear_log):
    """
    Micc command line interface.
    """
    ctx.obj = SimpleNamespace( verbosity=verbosity
                             , project_path=project_path.resolve()
                             , clear_log=clear_log
                             )


@main.command()
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
          , template
          , micc_file
          , structure
          , allow_nesting
          ):
    """
    Create a project skeleton. 
    
    Prompts the user for all entries in the micc.json file
    that do not have a default.
    """
    if ctx.obj.project_path==Path.cwd():
        answer = click.prompt("Enter [path/to/] project_name",default='',show_default=False)
        if not answer:
            click.echo("Command cancelled")
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
       , template
       , micc_file
       , overwrite
       ):
    """
    Add an app (console script) to the package. 
    
    :param str app_name: name of the cli application to be added to the package.
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
             , help='create a f2py module.')
@click.option( '--cpp', is_flag=True, default=False
             , help='create a C++ module.')
@click.option('-s', '--structure', type=click.Choice(['module','package']), default='module'
              , help="create a python project structure ``<module_name>.py`` (module),"
                     " or ``<module_name>/__init__.py`` (package).")
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
          , f2py, cpp, structure
          , template
          , micc_file
          , overwrite
          ):
    """
    Add a module to the package (Python, Fortran, C++). 
    
    :param str module_name: name of the module to be added to the package.
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
def version( ctx
           , major
           , minor
           , patch
           , poetry_version_rule
           , tag
           ):
    """
    Increment the project's version number. 
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
    ``micc tag`` subcommand, create a git tag for the current version. 
    """
    return cmds.micc_tag(global_options=ctx.obj)


@main.command()
@click.option('-m','--module', default=''
             , help="Build only this module. The prefix ['cpp_','f2py'] may be omitted.")
@click.option('-s', '--soft-link', is_flag=True, default=False
             , help="Create a soft link rather than a copy of the extension library.")
@click.pass_context
def build(ctx, module, soft_link):
    """
    Build binary extension libraries (f2py and C++ modules). 
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
    Convert a python module project to a package.

    A Python module project has only a ``package_name.py`` file, whereas
    a Python package project is structured  as ``package_name/__init__.py``.
    Only the latter can contain submodules (python and binary) and applications.

    This also expands the micc-template-general-docs in this project which adds
    a AUTHORS.rst, HISTORY.rst and installation.rst to the documentation structure.
    """
    ctx.obj.overwrite = overwrite
    return cmds.micc_convert_simple(global_options=ctx.obj)


@main.command()
@click.option('-h', '--html', is_flag=True, default=False
             , help="request for html documentation.")
@click.option('-l', '--latexpdf', is_flag=True, default=False
             , help="request for pdf documentation.")
@click.pass_context
def docs(ctx, html, latexpdf):
    """
    Generate documentation.
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
    Show info on a project. Use verbosity to produce more detailed info.
    """    
    return cmds.micc_info(global_options=ctx.obj)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover