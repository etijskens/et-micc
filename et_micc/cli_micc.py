# -*- coding: utf-8 -*-

"""
Application micc
"""

import os, sys, shutil
from types import SimpleNamespace
from pathlib import Path

import click

from et_micc.project import Project, micc_version
import et_micc.logger

__template_help = "Ordered list of Cookiecutter templates, or a single Cookiecutter template."


@click.group()
@click.option('-v', '--verbosity', count=True
    , help="The verbosity of the program output."
    , default=1
)
@click.option('-p', '--project-path'
    , help="The path to the project directory. "
           "The default is the current working directory."
    , default='.'
    , type=str
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
    if verbosity > 1:
        print("Current micc command is using Python", sys.version.replace('\n', ' '), end='\n\n')

    if clear_log:
        os.remove(project_path / 'micc.log')

    ctx.obj = SimpleNamespace(
        verbosity=verbosity,
        project_path=Path(project_path).resolve(),
        default_project_path=(project_path=='.'),
        clear_log=clear_log,
        template_parameters={},
    )


@main.command()
@click.option('--publish'
    , help="If specified, verifies that the package name is available on PyPI.\n"
           "If the result is False or inconclusive the project is NOT created."
    , default=False, is_flag=True
)
@click.option('-p', '--package'
    , help="Create a Python project with a package structure rather than a module structure:\n\n"
           "* package structure = ``<module_name>/__init__.py``\n"
           "* module  structure = ``<module_name>.py`` \n"
    , default=False, is_flag=True
)
@click.option('--micc-file'
    , help="The file containing the descriptions of the template parameters used"
           "in the *Cookiecutter* templates. "
    , default='', type=Path
)
@click.option('--python'
    , help="minimal python version for your project."
    , default='3.7'
)
@click.option('-d', '--description'
    , help="Short description of your project."
    , default='<Enter a one-sentence description of this project here.>'
)
@click.option('-l', '--lic'
    , help="License identifier."
    , default='MIT'
)
@click.option('-T', '--template', help=__template_help, default=[])
@click.option('-n', '--allow-nesting'
    , help="If specified allows to nest a project inside another project."
    , default=False, is_flag=True
)
@click.option('--module-name'
    , help="use this name for the module, rather than deriving it from the project name."
    , default=''
)
@click.argument('name', type=str, default='')
@click.pass_context
def create(ctx
           , name
           , package
           , module_name
           , micc_file
           , description
           , python
           , lic
           , template
           , allow_nesting
           , publish
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

    if name:
        if not options.default_project_path:
            # global option -p and argument name were both specified.
            print( "ERROR: you specified both global option -p and argument 'name':"
                  f"         -p -> {options.project_path}"
                  f"         name -> {name}"
                   "       You must choose one or the other, not both."
                 )
            ctx.exit(-1)
        else:
            # overwrite the -p global option so the project will be created:
            options.project_path = Path(name).resolve()
            options.default_project_path = False

    options.create = True
    options.micc_file = micc_file
    options.package = package
    options.publish = publish
    options.module_name = module_name

    if not template:  # default, empty list
        if options.package:
            template = [ 'package-base'
                       , 'package-general'
                       , 'package-simple-docs'
                       , 'package-general-docs'
                       ]
        else:
            template = [ 'package-base'
                       , 'package-simple'
                       , 'package-simple-docs'
                       ]
        options.templates = template
    # else:
    #     # ignore structure
    #     options.structure = 'user-defined'

    options.allow_nesting = allow_nesting

    licenses = ['MIT license'
        , 'BSD license'
        , 'ISC license'
        , 'Apache Software License 2.0'
        , 'GNU General Public License v3'
        , 'Not open source'
                ]
    for l in licenses:
        if l.startswith(lic):
            license_ = l
            break
    else:
        license_ = licenses[0]

    options.template_parameters.update(
        {'project_short_description': description,
         'open_source_license': license_,
         'python_version': python,
        }
    )
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
    options.backup = backup

    project = Project(options)
    if project.exit_code:
        ctx.exit(project.exit_code)

    with et_micc.logger.logtime(options):
        project.module_to_package_cmd()

        if project.exit_code == et_micc.expand.EXIT_OVERWRITE:
            options.logger.warning(
                f"It is normally ok to overwrite 'index.rst' as you are not supposed\n"
                f"to edit the '.rst' files in '{options.project_path}{os.sep}docs.'\n"
                f"If in doubt: rerun the command with the '--backup' flag,\n"
                f"  otherwise: rerun the command with the '--overwrite' flag,\n"
            )

    if project.exit_code:
        ctx.exit(project.exit_code)


@main.command()
@click.option('--name', is_flag=True
    , help="print the project name."
    , default=False
)
@click.option('--version', is_flag=True
    , help="print the project version."
    , default=False
)
@click.pass_context
def info(ctx,name,version):
    """Show project info.

    * file location
    * name
    * version number
    * structure (with ``-v``)
    * contents (with ``-vv``)

    Use verbosity to produce more detailed info.
    """
    options = ctx.obj

    project = Project(options)
    if project.exit_code:
        ctx.exit(project.exit_code)

    if name:
        print(project.package_name)
        return
    if version:
        print(project.version)
        return
    else:
        with et_micc.logger.logtime(options):
            project.info_cmd()

    if project.exit_code:
        ctx.exit(project.exit_code)


@main.command()
@click.option('-M', '--major'
    , help='Increment the major version number component and set minor and patch components to 0.'
    , default=False, is_flag=True
)
@click.option('-m', '--minor'
    , help='Increment the minor version number component and set minor and patch component to 0.'
    , default=False, is_flag=True
)
@click.option('-p', '--patch'
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
def version(ctx, major, minor, patch, rule, tag, short, dry_run):
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

    project = Project(options)
    if project.exit_code:
        ctx.exit(project.exit_code)

    with et_micc.logger.logtime(project):
        project.version_cmd()
        if project.exit_code == 0 and tag:
            project.tag_cmd()

    if project.exit_code:
        ctx.exit(project.exit_code)


@main.command()
@click.pass_context
def tag(ctx):
    """Create a git tag for the current version and push it to the remote repo."""
    options = ctx.obj

    project = Project(options)
    if project.exit_code:
        ctx.exit(project.exit_code)

    if project.exit_code:
        ctx.exit(project.exit_code)

    project.tag_cmd()

    if project.exit_code:
        ctx.exit(project.exit_code)


@main.command()
@click.option('--app'
    , default=False, is_flag=True
    , help="Add a CLI ."
)
@click.option('--group'
    , default=False, is_flag=True
    , help="Add a CLI with a group of sub-commands rather than a single command CLI."
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
@click.option('--f90'
    , default=False, is_flag=True
    , help="Add a f90 binary extionsion module (Fortran)."
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
@click.argument('name', type=str)
@click.pass_context
def add(ctx
        , name
        , app, group
        , py, package
        , f90
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

    If ``f90==True``: (add f90 module)

    * Fortran source in :file:`f90_<name>/<name>.f90` for f90 binary extension modules.

    If ``cpp==True``: (add cpp module)

    * C++ source     in :file:`cpp_<name>/<name>.cpp` for cpp binary extension modules.
    """
    options = ctx.obj
    options.add_name = name
    options.app = app
    options.group = group
    options.py = py
    options.package = package
    options.f90 = f90
    options.cpp = cpp
    options.templates = templates
    options.overwrite = overwrite
    options.backup = backup

    project = Project(options)
    if project.exit_code:
        ctx.exit(project.exit_code)

    with et_micc.logger.logtime(options):
        project.add_cmd()

    if project.exit_code:
        ctx.exit(project.exit_code)


@main.command()
@click.option('--silent', is_flag=True
    , help="Do not ask for confirmation on deleting a component."
    , default=False
)
@click.option('--entire-package', is_flag=True
    , help="Replace all occurences of <cur_name> in the entire package and in the ``tests`` directory."
    , default=False
)
@click.option('--entire-project', is_flag=True
    , help="Replace all occurences of <cur_name> in the entire project."
    , default=False
)
@click.argument('cur_name', type=str)
@click.argument('new_name', type=str, default='')
@click.pass_context
def mv(ctx, cur_name, new_name, silent, entire_package, entire_project):
    """Rename or remove a component, i.e an app (CLI) or a submodule.

    :param cur_name: name of component to be removed or renamed.
    :param new_name: new name of the component. If empty, the component will be removed.
    """
    options = ctx.obj

    options.cur_name = cur_name
    options.new_name = new_name
    options.silent = silent
    if new_name:
        options.entire_package, options.entire_project =  entire_package, entire_project
    # else these flags are ignored.

    project = Project(options)
    if project.exit_code:
        ctx.exit(project.exit_code)

    with et_micc.logger.logtime(options):
        project.mv_component()


@main.command()
@click.pass_context
def setup(ctx,
        ):
    """Setup your micc preferences.

    This command must be run once before you can use micc to manage your projects.
    """
    options = ctx.obj

    # options.cur_name = cur_name
    micc_file_template = Path(__file__).parent / 'micc.json'
    dotmicc = Path().home() / '.et_micc'
    dotmicc.mkdir(exist_ok=True)
    dotmicc_miccfile = dotmicc / 'micc.json'
    shutil.copyfile(str(micc_file_template),str(dotmicc_miccfile))
    preferences = et_micc.expand.set_preferences(dotmicc_miccfile)
    print("Done\n\n"
          "If you want to change your preferences, edit the default entries in file \n"
         f"    {dotmicc_miccfile}\n"
          "Note that these changes will only affect NEW projects. Existing projects will be unaffected.\n"
          "Micc is now configured and ready to be used.s"
    )

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

# eof
