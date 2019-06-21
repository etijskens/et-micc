# -*- coding: utf-8 -*-

"""
Console script for micc
=======================

Create a cookiecutter project from a micc file. Micc files are .json files
representing a dict. Keys are *str* objects representing cookiecutter template
arguments. The values are dicts of ``click.prompt()`` keyword arguments.
"""
#===============================================================================
import sys
import click
from micc.micc import micc_create, micc_version
#===============================================================================
@click.group()
def cli():
    """
    Micc command line interface. Type ``micc --help`` on the command line for details.
    """
#===============================================================================
@cli.command()
@click.argument('project_name', default='')
@click.option('-t','--template'
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
@cli.command()
@click.argument('project_path',default='')
@click.option('-M','--major', is_flag=True, default=False, help='increment major version number component')
@click.option('-m','--minor', is_flag=True, default=False, help='increment minor version number component')
@click.option('-p','--patch', is_flag=True, default=False, help='increment patch version number component')
@click.option('-r','--poetry-version-rule', help='a "poetry version <rule>"'
             , type=click.Choice(['','patch', 'minor', 'major', 'prepatch', 'preminor', 'premajor', 'prerelease'])
             )
def version(project_path,major,minor,patch,poetry_version_rule):
    """
    Micc version subcommand, similar to ``poetry version``. Increments the
    project's version number. 
    """
    rule = None
    if poetry_version_rule: rule = poetry_version_rule
    if patch: rule = 'patch'
    if minor: rule = 'minor'
    if major: rule = 'major'
    return micc_version(project_path,rule)
#===============================================================================
if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
#===============================================================================
