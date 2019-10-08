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
from micc import utils,logging

__template_help  =  "Ordered list of Cookiecutter templates, or a single Cookiecutter template."

__micc_file_help = ("The path to the *micc-file* with the parameter values used in the cookiecutter"
                    "templates. When a new project is created, "
                    "in the cookiecutter templates (default = ``micc.json``). "
                    "*Micc* does not use the standard ``cookiecutter.json`` file to provide the "
                    "template parameters, but uses a *micc-file*, usually named ``micc.json``, to "
                    "generate a ``cookiecutter.json`` file. Unlike the ``cookiecutter.json`` file, "
                    "the ``micc.json`` file can contain default values for the template parameters. "
                    "You will be prompted to provide a value for all parameters without default value. "
                    "*Micc* looks for the *micc-file* in the template directory **only** "
                    "(as specified with the ``--template`` option)."
                   )
__overwrite_help = ("If specified, any existing files are overwritten without backup. "
                    "Otherwise, *micc* will verify if there are existing files that"
                    "would be overwritten and gives you three options: \n\n"
                    "* abort,\n"
                    "* make a backup (``.bak``) before overwriting pre-existing files,\n"
                    "* do **not** make a backup before overwriting pre-existing files. This is equivalent to specifying ``--overwrite``."
                   )

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
             , help="If specified clears the project's ``micc.log`` file."
             , default=False, is_flag=True
             )
@click.pass_context
def main(ctx, verbosity, project_path, clear_log):
    """
    Micc command line interface.
    
    All commands that change the state of the project produce some output that
    is send to the console (taking verbosity into account). It is also sent to
    a logfile ``micc.log`` in the project directory. All output is always appended
    to the logfile. If you think the file has gotten too big, or you are no more
    interested in the history of your project, you can specify the ``--clear-log``
    flag to clear the logfile before any command is executed. In this way the
    command you execute is logged to an empty logfile.
    
    See below for (sub)commands.
    """
    ctx.obj = SimpleNamespace( verbosity=verbosity
                             , project_path=project_path.resolve()
                             , clear_log=clear_log
                             , template_parameters={}
                             )

    if utils.is_conda_python():
        click.echo( click.style("==========================================================\n"
                                "WARNING: You are running in a conda Python environment.\n"
                                "         Note that poetry does not play well with conda.\n",   fg='yellow')
                  + click.style("         Especially, do NOT use:\n"
                                "         >  poetry install\n",                                 fg='bright_red')
                  + click.style("==========================================================\n", fg='yellow')
                  )
    template_parameters_json = project_path / 'micc.json'
    if template_parameters_json.exists():
        ctx.obj.template_parameters.update(cmds.get_template_parameters(template_parameters_json))
    

@main.command()
@click.option('-m', '--module'
             , help="Create a Python project with a module structure rather than a package structure:\n\n"
                    "* module  structure = ``<module_name>.py`` \n"
                    "* package structure = ``<module_name>/__init__.py``\n\n"
                    "Default = ``package``."
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
@click.option('-T', '--template' , help=__template_help , default=[])
@click.option('-n', '--allow-nesting'
             , help="If specified allows to nest a project inside another project."
             , default=False, is_flag=True
             )
@click.pass_context
def create( ctx
          , module
          , micc_file
          , description
          , template
          , allow_nesting
          ):
    """
    Create a project skeleton.
    
    The project name is taken to be the last directory of the *<project_path>*.
    If this directory does not yet exist, it is created. If it exists already, it
    must be empty.
    
    The package name is the derived from the project name, taking the
    `PEP8 module naming rules <https://www.python.org/dev/peps/pep-0008/#package-and-module-names>`_
    into account:
    
    * all lowercase.
    * dashes ``'-'`` and spaces ``' '`` replaced with underscores ``'_'``.
    * in case the project name has a leading number, an underscore is prepended ``'_'``.
    
    If no *<project_path>* is provided, or if it is the same as the current working
    directory, the user is prompted to enter one.
    
    If the *<project_path>* refers to an existing project, *micc* refuses to continu.
    
    TODO:
    Prompts the user for all entries in the *micc-file* file
    that do not have a default value.
    """
    structure = 'module' if module else 'package'
    if not template: # default, empty list
        if structure=='module':
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
    else:
        # ignore structure
        structure = 'user-defined'
        
    ctx.obj.structure = structure
    ctx.obj.allow_nesting = allow_nesting
    ctx.obj.template_parameters['project_short_description'] = description
        
    rc = cmds.micc_create( templates=template
                         , micc_file=micc_file
                         , global_options=ctx.obj
                         )
    if rc: ctx.exit(rc)


@main.command()
@click.argument('app_name',type=str)
@click.option('-T', '--template', default='app', help=__template_help)
@click.option('--overwrite', is_flag=True
             , help="Overwrite pre-existing files (without backup)."
             , default=False
             )
@click.option('--backup', is_flag=True
             , help="Make backup files (.bak) before overwriting any pre-existing files."
             , default=False
             )
@click.pass_context
def app( ctx
       , app_name
       , template
       , overwrite
       , backup
       ):
    """
    Add an app (console script) with name *<app_name>* to the package.
    
    *<App_name>* is also the name of the executable when the package is installed.
    The source code of the app resides in ``<project_name>/<package_name>/cli_<app_name>.py``.
    """
    
    if utils.app_exists(ctx.obj.project_path, app_name):
        raise AssertionError(f"Project {ctx.obj.project_path.name} has already an app named {app_name}.")

    with logging.logtime(ctx.obj):
        ctx.obj.overwrite = overwrite
        ctx.obj.backup    = backup
        
        rc =  cmds.micc_app( app_name
                           , templates=template
                           , global_options=ctx.obj
                           )
    if rc:
        ctx.exit(rc)


@main.command()
@click.argument('module_name', default='')
@click.option( '--f2py'
             , help='If specified creates a f2py module.'
             , default=False, is_flag=True
             )
@click.option( '--cpp'
             , help='If specified creates a C++ module.'
             , default=False, is_flag=True
             )
@click.option('-p', '--package'
             , help="Create a Python module with a package structure rather than a module structure:\n\n"
                    "* module  structure = ``<module_name>.py`` \n"
                    "* package structure = ``<module_name>/__init__.py``\n\n"
                    "Default = module structure."
             , default=False, is_flag=True
             )
@click.option( '-T', '--template' , default='', help=__template_help)
@click.option('--overwrite', is_flag=True
             , help="Overwrite pre-existing files (without backup)."
             , default=False
             )
@click.option('--backup', is_flag=True
             , help="Make backup files (.bak) before overwriting any pre-existing files."
             , default=False
             )
@click.pass_context
def module( ctx
          , module_name
          , f2py, cpp, package
          , template
          , overwrite
          , backup
          ):
    """
    Add a sub-module with name *<module_name>* to the package. This can be a Python
    module, or a binary extension module (Fortran or C++).
    The source code is in
    
    * *<module_name>.py* or *<module_name>/__init__.py* for python modules, depending on the *<structure>* parameter.
    * directory *f2py_<module_name>.py* for f2py extension modules (Fortran source code).
    * directory *cpp_<module_name>.py* for cpp extension modules (C++ source code).
    """
    if (cpp and f2py):
        raise AssertionError("Flags '--f2py' and '--cpp' cannot be specified simultaneously.")
    if module_exists(ctx.obj.project_path,module_name):
        raise AssertionError(f"Project {ctx.obj.project_path.name} has already a module named {module_name}.")

    ctx.obj.structure = 'package' if package else 'module'
    ctx.obj.overwrite = overwrite
    ctx.obj.backup    = backup
    ctx.obj.template_parameters['path_to_cmake_tools'] = utils.path_to_cmake_tools()
    
    with logging.logtime(ctx.obj):
        if f2py:
            if not template:
                template = 'module-f2py'
            rc = cmds.micc_module_f2py( module_name
                                      , templates=template
                                      , global_options=ctx.obj
                                      )
        elif cpp:
            if not template:
                template = 'module-cpp'
            rc = cmds.micc_module_cpp( module_name
                                     , templates=template
                                     , global_options=ctx.obj
                                     )
        else:
            if not template:
                template = 'module-py'
            rc = cmds.micc_module_py( module_name
                                    , templates=template
                                    , global_options=ctx.obj
                                    )
    if rc:
        ctx.exit(rc)


@main.command()
@click.argument( 'rule', default='')
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
@click.option('-t', '--tag'
             , help='Create a git tag for the new version, and push it to the remote repo.'
             , default=False, is_flag=True
             )
@click.option('-s', '--short'
             , help='Print the version on stdout.'
             , default=False, is_flag=True
             )
@click.option('--poetry'
             , help='Use poetry instead of bumpversion for bumping the version.'
             , default=False, is_flag=True
             )
@click.pass_context
def version( ctx, rule, major, minor, patch, tag, short, poetry):
    """
    Increment or show the project's version number.  By default micc uses
    *bumpversion* for this, but it can also use *poetry*, by specifiying ``--poetry``.
    
    You can also avoide using ``micc version`` and using *bumpversion* directly. Note,
    however, that the version string appears in both ``pyproject.toml`` and in the top-level
    package (``<mopdule_name>.py`` or ``<mopdule_name>/__init__.py``). Since, currently,
    *poetry* is incapable of bumping the version string in any other file than *pyproject.tom.*,
    using ``poetry version ...`` is not recommented.
    
    :param str rule: any string that is also accepted by poetry version. Typically, the empty
        string (show current version), a valid rule: patch, minor, major, prepatch, preminor, 
        premajor, prerelease, or any valid version string.  
    """
    if rule and (major or minor or patch):
        raise RuntimeError("Ambiguous arguments:\n  specify either 'rule' argments,\n  or one of [--major,--minor--patch], not both.")
        
    with logging.logtime(ctx.obj):
        return_code = cmds.micc_version(rule, short, poetry, global_options=ctx.obj)
        if return_code==0 and tag:
            rc = cmds.micc_tag(global_options=ctx.obj)
        else:
            rc = return_code
    if rc: 
        ctx.exit(rc)


@main.command()
@click.pass_context
def tag(ctx):
    """
    Create a git tag for the current version and push it to the remote repo.
    """
    with logging.logtime(ctx.obj):
        return cmds.micc_tag(global_options=ctx.obj)


@main.command()
@click.option('-m','--module'
             , help="Build only this module. The module kind prefix (``cpp_`` "
                    "for C++ modules, ``f2py_`` for Fortran modules) may be omitted."
             , default=''
             )
@click.option('-s', '--soft-link'
             , help="Create a soft link rather than a copy of the extension library."
             , default=False, is_flag=True
             )
@click.pass_context
def build(ctx, module, soft_link):
    """
    Build binary extension libraries (f2py and cpp modules). 
    """
    with logging.logtime(ctx.obj):
        rc = cmds.micc_build( module_to_build=module
                            , soft_link=soft_link
                            , global_options=ctx.obj
                            )
    if rc:
        ctx.exit(rc)
      

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
    """
    Convert a Python module project to a package.

    A Python *module* project has only a ``<package_name>.py`` file, whereas
    a Python *package* project has ``<package_name>/__init__.py`` and can contain
    submodules, such as Python modules, packages and applications, as well as
    binary extension modules.

    This command also expands the ``package-general-docs`` template in this
    project, which adds a ``AUTHORS.rst``, ``HISTORY.rst`` and ``installation.rst``
    to the documentation structure.
    """
    with logging.logtime(ctx.obj):
        ctx.obj.overwrite = overwrite
        ctx.obj.backup    = backup
        rc = cmds.micc_convert_simple(global_options=ctx.obj)
    if rc:
        ctx.exit(rc)


@main.command()
@click.option('-h', '--html'
             , help="If specified builds html documentation."
             , default=False, is_flag=True
             )
@click.option('-l', '--latexpdf'
             , help="If specified builds pdf documentation."
             , default=False, is_flag=True
             )
@click.pass_context
def docs(ctx, html, latexpdf):
    """
    Build documentation for the project using Sphinx with the specified formats.
    """
    with logging.logtime(ctx.obj):
        formats = []
        if html:
            formats.append('html')
        if latexpdf:
            formats.append('latexpdf')
        
        rc = cmds.micc_docs(formats, global_options=ctx.obj)
    if rc:
        ctx.exit(rc)


@main.command()
@click.pass_context
def info(ctx):
    """
    Show info on the project.
        
    * file location
    * name
    * version number
    * structure (with ``-v``)
    * contents (with ``-vv``)
    
    Use verbosity to produce more detailed info.
    """    
    rc = cmds.micc_info(global_options=ctx.obj)
    if rc:
        ctx.exit(rc)


@main.command()
@click.argument('args',nargs=-1)
@click.option('--system'
             , help="Use the poetry version installed in the system, instead "
                    "of that in the python environment."
             , default=False, is_flag=True
             )
@click.pass_context
def poetry(ctx,args,system):
    """
    A wrapper around poetry that warns for dangerous poetry commands in a conda environment.
    """
    with logging.logtime(ctx.obj):
        ctx.obj.system = system
        rc = cmds.micc_poetry( *args, global_options=ctx.obj)
    if rc:
        ctx.exit(rc)

    
if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover