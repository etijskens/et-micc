# -*- coding: utf-8 -*-

"""
Console script for micc
=======================

Create a cookiecutter project from a micc file. Micc files are .json files
representing a dict. Keys are *str* objects representing cookiecutter template
arguments. The values are dicts of ``mainck.prompt()`` keyword arguments.
"""
#===============================================================================
import sys
import click
from .commands import micc_create, micc_version, micc_tag, micc_app
#===============================================================================
@click.group()
def main():
    """
    Micc command line interface. Type ``micc --help`` on the command line for details.
    """
#===============================================================================
@main.command()
@click.argument('project_name', default='')
@click.option('-T','--template'
             , default='micc-module'
             )
@click.option('-m', '--micc-file'
             , default='micc.json'
             )
@click.option('-o', '--output-dir'
             , default='.'
             )
@click.option('-v', '--verbose'
             , is_flag=True
             , default=False
             )
def create( project_name
          , template, micc_file
          , output_dir
          , verbose
          ):
    """
    Create a project skeleton. Prompts the user for all entries in the micc.json file
    that do not have a default.

    :param str template: path to the cookiecutter template.  
    """
    return micc_create( project_name
                      , template=template
                      , micc_file=micc_file
                      , output_dir=output_dir
                      , verbose=verbose
                      )
#===============================================================================
@main.command()
@click.argument('project_path', default='')
@click.option('-M','--major', is_flag=True, default=False
             , help='increment major version number component'
             )
@click.option('-m','--minor', is_flag=True, default=False
             , help='increment minor version number component'
             )
@click.option('-p','--patch', is_flag=True, default=False
             , help='increment patch version number component'
             )
@click.option('-r','--poetry-version-rule', help='a "poetry version <rule>"'
             , type=click.Choice(['','patch', 'minor', 'major'
                                 , 'prepatch', 'preminor'
                                 , 'premajor', 'prerelease'
                                 ]
                                )
             )
@click.option('-t', '--tag'
             , is_flag=True
             , default=False
             )
def version(project_path, major, minor, patch, poetry_version_rule, tag):
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
    return_code = micc_version(project_path,rule)
    if return_code==0 and tag:
        return micc_tag(project_path)
#===============================================================================
@main.command()
@click.argument('project_path', default='')
def tag(project_path):
    """
    ``micc tag`` subcommand, create a git tag for the current version. 
    """
    return micc_tag(project_path)
#===============================================================================
@main.command()
@click.argument('app_name', default='')
@click.option('-P', '--project_path', default='')
def app(app_name,project_path):
    """
    ``micc app`` subcommand, add an app (console script) to the package. 
    
    :param str app_name: name of the cli application.
    """
    return micc_app(app_name, project_path)
#===============================================================================
if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
#===============================================================================
