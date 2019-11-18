# -*- coding: utf-8 -*-

"""
Application micc
"""

import os,sys
from types import SimpleNamespace
from pathlib import Path
# from operator import xor

import click

from et_micc.project import Project
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
    
    if project.rc:
        ctx.exit(project.rc)
    
   
if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover