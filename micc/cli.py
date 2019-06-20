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
def create( template, micc_file
          , output_dir
          , verbose
          ):
    """
    Console script for micc. Prompts the user for all entries in the micc.json file
    that do not have a default.

    :param str template: path to the cookiecutter template.  
    """
    return micc_create( template=template
                      , micc_file=micc_file
                      , output_dir=output_dir
                      , verbose=verbose
                      )
#===============================================================================
@cli.command()
@click.argument('project_path',default='')
@click.option('--major','-M',is_flag=True,default=False,help='increment major version number component')
@click.option('--minor','-m',is_flag=True,default=False,help='increment minor version number component')
@click.option('--patch','-p',is_flag=True,default=False,help='increment patch version number component')
def version(project_path,major,minor,patch):
    level = None
    if patch: level = 'patch'
    if minor: level = 'minor'
    if major: level = 'major'
    return micc_version(project_path,level)
#===============================================================================
if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
#===============================================================================
