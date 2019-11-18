# -*- coding: utf-8 -*-

"""
Application micc
"""

import os,sys
from types import SimpleNamespace
from pathlib import Path
from operator import xor

import click

import et_micc.commands as cmds
import et_micc.expand

import et_micc_tools.utils
import et_micc_tools.logging_tools

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
                             )

#     if et_micc.utils.is_conda_python():
#         click.echo( click.style("==========================================================\n"
#                                 "WARNING: You are running in a conda Python environment.\n"
#                                 "         Note that poetry does not play well with conda.\n",   fg='yellow')
#                   + click.style("         Especially, do NOT use:\n"
#                                 "         >  poetry install\n",                                 fg='bright_red')
#                   + click.style("==========================================================\n", fg='yellow')
#                   )
    template_parameters_json = project_path / 'micc.json'
    if template_parameters_json.exists():
        ctx.obj.template_parameters.update(
            et_micc.expand.get_template_parameters(template_parameters_json)
        )
    else:
        ctx.obj.template_parameters.update(
            et_micc.expand.get_template_parameters(
                et_micc.expand.get_preferences(Path('.'))
            )
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
    
    If the *<project_path>* refers to an existing project, *micc* refuses to continu,
    unless ``--allow-nesting`` is soecified.
    """
    structure = 'package' if package else 'module'
    
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

    ctx.obj.template_parameters.update({'project_short_description' : description
                                       ,'open_source_license'       : license_
                                       }
                                      ) 
                                        
    rc = cmds.micc_create( templates=template
                         , micc_file=micc_file
                         , global_options=ctx.obj
                         )
    if rc: ctx.exit(rc)

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
@click.option('-T', '--template', default='', help=__template_help)
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
       , template
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
    # set implied flags:
    if group:
        app_implied = f" [implied by --group   ({int(group  )})]"
        app = True
    else:
        app_implied = ""
        
    if package:
        py_implied  = f" [implied by --package ({int(package)})]"
        py = True
    else:
        py_implied = ""
    
    if not (app or py or f2py or cpp) or not xor(xor(app,py),xor(f2py,cpp)):
        # Do not log, as the state of the project is not changed.
        click.secho(f"ERROR: specify one and only one of \n"
                    f"  --app  ({int(app )}){app_implied}\n"
                    f"  --py   ({int(py  )}){py_implied}\n"
                    f"  --f2py ({int(f2py)})\n"
                    f"  --cpp  ({int(cpp )})\n"
                   ,fg='bright_red'
                   )
        ctx.exit(1)
        
    if app:
        if et_micc_tools.utils.app_exists(ctx.obj.project_path, name):
            msg = f"Project {ctx.obj.project_path.name} has already an app named {name}."
            click.secho("ERROR: " + msg,fg='bright_red')
            if ctx.obj.verbosity>1:
                raise AssertionError(msg)
            else:
                ctx.exit(1) 
    
        with et_micc_tools.logging_tools.logtime(ctx.obj):
            if group:
                if not template:
                    template = 'app-sub-commands'
            else:
                if not template:
                    template = 'app-simple'
                    
            ctx.obj.overwrite = overwrite
            ctx.obj.backup    = backup
            ctx.obj.group     = group
            
            rc =  cmds.micc_app( name
                               , templates=template
                               , global_options=ctx.obj
                               )
    else:
        if et_micc_tools.utils.module_exists(ctx.obj.project_path,name):
            msg = f"Project {ctx.obj.project_path.name} has already a module named {name}."
            click.secho("ERROR: " + msg, fg='bright_red')
            if ctx.obj.verbosity>1:
                raise AssertionError(msg)
            else:
                ctx.exit(1) 

        ctx.obj.overwrite = overwrite
        ctx.obj.backup    = backup
        ctx.obj.template_parameters['path_to_cmake_tools'] = et_micc_tools.utils.path_to_cmake_tools()
        
        if py:
            ctx.obj.structure = 'package' if package else 'module'
            if not template:
                template = 'module-py'
            rc = cmds.micc_module_py( name, templates=template, global_options=ctx.obj )
                    
        elif f2py:
            if not template:
                template = 'module-f2py'
            rc = cmds.micc_module_f2py( name, templates=template, global_options=ctx.obj )

        elif cpp:
            if not template:
                template = 'module-cpp'
            rc = cmds.micc_module_cpp( name, templates=template, global_options=ctx.obj )

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
    """Increment or show the project's version number.
    
    By default *micc* uses *bumpversion* for this, but it can also use *poetry*,
    by specifiying the ``--poetry`` flag.
    
    You can also avoide using ``micc version`` and use *bumpversion* directly. Note,
    however, that the version string appears in both ``pyproject.toml`` and in the top-level
    package (``<mopdule_name>.py`` or ``<mopdule_name>/__init__.py``). Since, currently,
    *poetry* is incapable of bumping the version string in any other file than *pyproject.tom.*,
    using ``poetry version ...`` is not recommented.
    
    :param str rule: any string that is also accepted by poetry version. Typically, the empty
        string (show current version), a valid rule: patch, minor, major, prepatch, preminor, 
        premajor, prerelease, or any valid version string.  
    """
    if rule and (major or minor or patch):
        msg = "Ambiguous arguments:\n  specify either 'rule' argments,\n  or one of [--major,--minor--patch], not both."
        click.secho(msg,fg='bright_red')
        if ctx.obj.verbosity>1:
            raise RuntimeError(msg)
        else:
            ctx.exit(1)

    if major:
        rule = 'major'
    if minor:
        rule = 'minor'
    if patch:
        rule = 'patch'
    
    with et_micc_tools.logging_tools.logtime(ctx.obj):
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
    """Create a git tag for the current version and push it to the remote repo."""
    
    with et_micc_tools.logging_tools.logtime(ctx.obj):
        return cmds.micc_tag(global_options=ctx.obj)
      

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

    with et_micc_tools.logging_tools.logtime(ctx.obj):
        ctx.obj.overwrite = overwrite
        ctx.obj.backup    = backup
        rc = cmds.micc_convert_simple(global_options=ctx.obj)
        if rc==et_micc_tools.expand.EXIT_OVERWRITE:
            et_micc_tools.logging_tools.get_micc_logger(ctx.obj).warning(
                f"It is normally ok to overwrite 'index.rst' as you are not supposed\n"
                f"to edit the '.rst' files in '{ctx.obj.project_path}{os.sep}docs.'\n"
                f"If in doubt: rerun the command with the '--backup' flag,\n"
                f"  otherwise: rerun the command with the '--overwrite' flag,\n"
            )
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
    """Build documentation for the project using Sphinx with the specified formats."""
    
    with et_micc_tools.logging_tools.logtime(ctx.obj):
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
    """Show project info.
        
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
    """A wrapper around poetry that warns for dangerous poetry commands in a conda environment."""
    with et_micc_tools.logging_tools.logtime(ctx.obj):
        ctx.obj.system = system
        rc = cmds.micc_poetry( *args, global_options=ctx.obj)
    if rc:
        ctx.exit(rc)


@main.command()
@click.pass_context
def dev_install(ctx):
    """Perform development install of the package. 
    
    (Changes to python source are immediately visible, changes to Fortran
    or C++ source are visible after running ``et_micc build``. :py:mod:import.reload`
    may be necessary.)
    
    Copy the directory structure of the project's package directory
    and create a symlink for every file in there.
    
    This is a temporary workaround for installing packages
    with binary extensions. Some day poetry_ will take over.
    """
    with et_micc_tools.logging_tools.logtime(ctx.obj):
        cmds.micc_dev_install(ctx.obj)

@main.command()
@click.pass_context
def dev_uninstall(ctx):
    """Undo ``et_micc dev-install``.
    
    This is a temporary workaround for uninstalling packages
    with binary extensions. Some day poetry_ will take over.
    """
    with et_micc_tools.logging_tools.logtime(ctx.obj):
        cmds.micc_dev_install(ctx.obj,install=False)
    
   
if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover