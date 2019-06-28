# -*- coding: utf-8 -*-

"""
Console script for micc
=======================

Create a project from a micc file. Micc files are .json files
representing a dict. Keys are *str* objects representing cookiecutter template
arguments. The values are dicts of ``mainck.prompt()`` keyword arguments.
"""
#===============================================================================
import sys
import click
from micc.commands import micc_create, micc_version, micc_tag, micc_app, micc_module
from types import SimpleNamespace
#===============================================================================
@click.group()
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.pass_context
def main(ctx,verbose):
    """
    Micc command line interface. Type ``micc --help`` on the command line for details.
    """
    sns = SimpleNamespace(verbose=verbose)
    ctx.obj = sns
#===============================================================================
@main.command()
@click.argument('project_name',     default='')
@click.option('-o', '--output-dir', default='.', help="location of the new project")
@click.option('-T', '--template',   default='micc-package'
              , help="a Python package cookiecutter template")
@click.option('-m', '--micc-file',  default='micc.json'
              , help="the micc-file for the cookiecutter template")
@click.pass_context
def create( ctx
          , output_dir
          , project_name
          , template, micc_file
          ):
    """
    Create a project skeleton. Prompts the user for all entries in the micc.json file
    that do not have a default.
    
    :param str project_name: name of the project to be created.  
    """
    return micc_create( project_name
                      , template=template
                      , micc_file=micc_file
                      , output_dir=output_dir
                      , verbose=ctx.obj.verbose
                      )
#===============================================================================
@main.command()
@click.argument('app_name', default='')
@click.option('-P', '--project_path', default='')
@click.pass_context
def app(ctx, app_name, project_path):
    """
    ``micc app`` subcommand, add an app (console script) to the package. 
    
    :param str app_name: name of the cli application to be added to the package.
    """
    return micc_app(app_name, project_path, ctx.obj.verbose)
#===============================================================================
@main.command()
@click.argument('module_name', default='')
@click.option('-P', '--project_path', default='')
@click.pass_context
def module(ctx, module_name, project_path):
    """
    ``micc module`` subcommand, add a module to the package. 
    
    :param str module_name: name of the module to be added to the package.
    """
    return micc_module(module_name, project_path, ctx.obj.verbose)
#===============================================================================
@main.command()
@click.argument('project_path', default='')
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
def version(ctx, project_path, major, minor, patch, poetry_version_rule, tag):
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
    return_code = micc_version(project_path, rule, ctx.obj.verbose)
    if return_code==0 and tag:
        return micc_tag(project_path, ctx.obj.verbose)
#===============================================================================
@main.command()
@click.argument('project_path', default='')
@click.pass_context
def tag(ctx, project_path):
    """
    ``micc tag`` subcommand, create a git tag for the current version. 
    """
    return micc_tag(project_path, ctx.obj.verbose)
#===============================================================================
if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
#===============================================================================
