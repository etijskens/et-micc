# -*- coding: utf-8 -*-

"""
Application micc
"""

import os,sys
from types import SimpleNamespace
from pathlib import Path

import click

from et_micc.project import Project, micc_version
import et_micc.logging

__template_help  =  "Ordered list of Cookiecutter templates, or a single Cookiecutter template."


@click.group()
@click.option('-v', '--verbosity', count=True
             , help="The verbosity of the program output."
             , default=1
             )
@click.option('-p', '--project-path'
             , help="The path to the project directory. "
                    "The default is the current working directory."
             , default='.'
             , type=Path
             )
@click.option('--clear-log'
             , help="If specified clears the project's ``et_micc.log`` file."
             , default=False, is_flag=True
             )
@click.version_option(version=micc_version())
@click.pass_context
def main(ctx, verbosity, project_path, clear_log):
    """Micc command line interface.
    
    All commands that change the state of the project produce some output that
    is send to the console (taking verbosity into account). It is also sent to
    a logfile ``et_micc.log`` in the project directory. All output is always appended
    to the logfile. If you think the file has gotten too big, or you are no more
    interested in the history of your project, you can specify the ``--clear-log``
    flag to clear the logfile before any command is executed. In this way the
    command you execute is logged to an empty logfile.
    
    See below for (sub)commands.
    """
    if clear_log:
        os.remove(project_path / 'micc.log')
        
    ctx.obj = SimpleNamespace( verbosity=verbosity
                             , project_path=project_path.resolve()
                             , clear_log=clear_log
                             , template_parameters={}
                             , create = False
                             )
    

@main.command()
@click.option('-p', '--package'
             , help="Create a Python project with a package structure rather than a module structure:\n\n"
                    "* package structure = ``<module_name>/__init__.py``\n"
                    "* module  structure = ``<module_name>.py`` \n"
             , default=False, is_flag=True
             )
@click.option('--micc-file'
             , help="The file containing the descriptions of the template parameters used"
                    "in the *Cookiecutter* templates. "
             , default='',type=Path
             )
@click.option('-d', '--description'
             , help="Short description of your project."
             , default='<Enter a one-sentence description of this project here.>'
             )
@click.option('-l', '--lic'
             , help="License identifier."
             , default='MIT'
             )
@click.option('-T', '--template' , help=__template_help , default=[])
@click.option('-n', '--allow-nesting'
             , help="If specified allows to nest a project inside another project."
             , default=False, is_flag=True
             )
@click.pass_context
def create( ctx
          , package
          , micc_file
          , description
          , lic
          , template
          , allow_nesting
          ):
    """Create a new project skeleton.
    
    The project name is taken to be the last directory of the *project_path*.
    If this directory does not yet exist, it is created. If it does exist already, it
    must be empty.
    
    The package name is the derived from the project name, taking the
    `PEP8 module naming rules <https://www.python.org/dev/peps/pep-0008/#package-and-module-names>`_
    into account:
    
    * all lowercase.
    * dashes ``'-'`` and spaces ``' '`` replaced with underscores ``'_'``.
    * in case the project name has a leading number, an underscore is prepended ``'_'``.
        
    If *project_path* is a subdirectory of a micc project, *micc* refuses to continu,
    unless ``--allow-nesting`` is soecified.
    """
    options = ctx.obj
    options.create = True
    options.micc_file = micc_file
    options.structure = 'package' if package else 'module'
    
    if not template: # default, empty list
        if options.structure=='module':
            template = ['package-base'
                       ,'package-simple'
                       ,'package-simple-docs'
                       ]
        else:
            template = ['package-base'
                       ,'package-general'
                       ,'package-simple-docs'
                       ,'package-general-docs'
                       ]
        options.templates = template
    else:
        # ignore structure
        options.structure = 'user-defined'
        
    options.allow_nesting = allow_nesting
    
    licenses = ['MIT license'
               ,'BSD license'
               ,'ISC license'
               ,'Apache Software License 2.0'
               ,'GNU General Public License v3'
               ,'Not open source'
               ]
    for l in licenses:
        if l.startswith(lic):
            license_ = l
            break
    else:
        license_ = licenses[0]
    options.template_parameters.update({'project_short_description' : description
                                       ,'open_source_license'       : license_
                                       }
                                      ) 
#     with et_micc.logging.logtime(ctx.obj):
    project = Project(options)
    
    if project.exit_code:
        ctx.exit(project.exit_code)
    
   
@main.command()
@click.option('--overwrite', is_flag=True
             , help="Overwrite pre-existing files (without backup)."
             , default=False
             )
@click.option('--backup', is_flag=True
             , help="Make backup files (.bak) before overwriting any pre-existing files."
             , default=False
             )
@click.pass_context
def convert_to_package(ctx, overwrite, backup):
    """Convert a Python module project to a package.

    A Python *module* project has only a ``<package_name>.py`` file, whereas
    a Python *package* project has ``<package_name>/__init__.py`` and can contain
    submodules, such as Python modules, packages and applications, as well as
    binary extension modules.

    This command also expands the ``package-general-docs`` template in this
    project, which adds a ``AUTHORS.rst``, ``HISTORY.rst`` and ``installation.rst``
    to the documentation structure.
    """
    options = ctx.obj
    options.overwrite = overwrite
    options.backup    = backup
    
    with et_micc.logging.logtime(options):
        project = Project(options)
        project.module_to_package_cmd()
        
        if project.exit_code==et_micc.expand.EXIT_OVERWRITE:
            et_micc.logging.get_micc_logger(ctx.obj).warning(
                f"It is normally ok to overwrite 'index.rst' as you are not supposed\n"
                f"to edit the '.rst' files in '{options.project_path}{os.sep}docs.'\n"
                f"If in doubt: rerun the command with the '--backup' flag,\n"
                f"  otherwise: rerun the command with the '--overwrite' flag,\n"
            )

    if project.exit_code:
        ctx.exit(project.exit_code)
            
            
@main.command()
@click.pass_context
def info(ctx):
    """Show project info.
        
    * file location
    * name
    * version number
    * structure (with ``-v``)
    * contents (with ``-vv``)
    
    Use verbosity to produce more detailed info.
    """ 
    options = ctx.obj   
    with et_micc.logging.logtime(options):
        project = Project(options)
        project.info_cmd()

    if project.exit_code:
        ctx.exit(project.exit_code)


@main.command()
@click.option('-M','--major'
             , help='Increment the major version number component and set minor and patch components to 0.'
             , default=False, is_flag=True
             )
@click.option('-m','--minor'
             , help='Increment the minor version number component and set minor and patch component to 0.'
             , default=False, is_flag=True
             )
@click.option('-p','--patch'
             , help='Increment the patch version number component.'
             , default=False, is_flag=True
             )
@click.option('-r', '--rule'
             , help='Any semver 2.0 version string.'
             , default=''
             )
@click.option('-t', '--tag'
             , help='Create a git tag for the new version, and push it to the remote repo.'
             , default=False, is_flag=True
             )
@click.option('-s', '--short'
             , help='Print the version on stdout.'
             , default=False, is_flag=True
             )
@click.option('-d', '--dry-run'
             , help='bumpversion --dry-run.'
             , default=False, is_flag=True
             )
@click.pass_context
def version( ctx, major, minor, patch, rule, tag, short, dry_run):
    """Modify or show the project's version number."""
    options = ctx.obj

    if rule and (major or minor or patch):
        msg = ("Both --rule and --major|--minor|--patc specified.")
        click.secho("[ERROR]\n" + msg, fg='bright_red')
        ctx.exit(1)
    elif major:
        rule = 'major'
    elif minor:
        rule = 'minor'
    elif patch:
        rule = 'patch'

    options.rule = rule
    options.short = short
    options.dry_run = dry_run
        
    with et_micc.logging.logtime(ctx.obj):
        project = Project(options)
        project.version_cmd()
        if project.exit_code==0 and tag:
            project.tag_cmd()
            
    if project.exit_code: 
        ctx.exit(project.exit_code)


@main.command()
@click.pass_context
def tag(ctx):
    """Create a git tag for the current version and push it to the remote repo."""


@main.command()
@click.option('--app'
             , default=False, is_flag=True
             , help="Add a CLI."
             )
@click.option('--group'
             , default=False, is_flag=True
             , help="Add a CLI with a group of sub-commands."
             )
@click.option('--py'
             , default=False, is_flag=True
             , help="Add a Python module."
             )
@click.option('--package'
             , help="Add a Python module with a package structure rather than a module structure:\n\n"
                    "* module  structure = ``<module_name>.py`` \n"
                    "* package structure = ``<module_name>/__init__.py``\n\n"
                    "Default = module structure."
             , default=False, is_flag=True
             )
@click.option('--f2py'
             , default=False, is_flag=True
             , help="Add a f2py binary extionsion module (Fortran)."
             )
@click.option('--cpp'
             , default=False, is_flag=True
             , help="Add a cpp binary extionsion module (C++)."
             )
@click.option('-T', '--templates', default='', help=__template_help)
@click.option('--overwrite', is_flag=True
             , help="Overwrite pre-existing files (without backup)."
             , default=False
             )
@click.option('--backup', is_flag=True
             , help="Make backup files (.bak) before overwriting any pre-existing files."
             , default=False
             )
@click.argument('name',type=str)
@click.pass_context
def add( ctx
       , name
       , app, group
       , py, package
       , f2py
       , cpp
       , templates
       , overwrite
       , backup
       ):
    """Add a module or CLI to the projcect.
    
    :param str name: name of the CLI or module added.
    
    If ``app==True``: (add CLI application)
    
    * :py:obj:`app_name` is also the name of the executable when the package is installed.
    * The source code of the app resides in :file:`<project_name>/<package_name>/cli_<name>.py`.


    If ``py==True``: (add Python module)
    
    * Python source  in :file:`<name>.py*`or :file:`<name>/__init__.py`, depending on the :py:obj:`package` flag.

    If ``f2py==True``: (add f2py module)
    
    * Fortran source in :file:`f2py_<name>/<name>.f90` for f2py binary extension modules.

    If ``cpp==True``: (add cpp module)
    
    * C++ source     in :file:`cpp_<name>/<name>.cpp` for cpp binary extension modules.
    """
    options = ctx.obj    
    options.add_name = name
    options.app = app
    options.group = group
    options.py = py
    options.package = package
    options.f2py = f2py
    options.cpp = cpp
    options.templates = templates
    options.overwrite = overwrite
    options.backup = backup
        
    with et_micc.logging.logtime(options):
        project = Project(options)            
        project.add_cmd()
      
    if project.exit_code: 
        ctx.exit(project.exit_code)

        
    

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
    
    
#eof