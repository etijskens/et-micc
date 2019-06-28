# -*- coding: utf-8 -*-
"""
Main module.
"""
#===============================================================================
import os
import json
import subprocess
#===============================================================================
import click
from cookiecutter.main import cookiecutter
from poetry.console.commands import VersionCommand 
# from poetry.utils.toml_file import TomlFile
# from poetry.console.application import Application
# from cleo.inputs.argv_input import ArgvInput
import toml
#===============================================================================
from micc import utils
from micc.utils import in_directory
from micc import __version__
#===============================================================================
def _resolve_template(template):
    """
    """
    if  template.startswith('~') or template.startswith(os.sep):
        pass # absolute path
    elif os.sep in template:
        # reative path
        template = os.path.join(os.getcwd(), template)
    else:
        # jutst the template name 
        template = os.path.join(os.path.dirname(__file__), template)
    return template
#===============================================================================
def micc_create( project_name=''
               , output_dir='.'
               , verbose=False
               , template='micc-package', micc_file='micc.json'
               ):
    """
    Create a new project skeleton. 
    
    :param str project_name: the name of the project to be created. If empty str,
    :param str output_dir: path where the project will be created. By default
        the current directory.
    :param str template: path to the Cookiecutter_ template.
        (``micc-module`` by default). 
    :param str micc_file: path to the json file containing the template parameters
        descrioptions, relative to ``template``.  Default is ``micc.json``.
    :param bool verbose: verbose output, False by default. 
    """
    template = _resolve_template(template)
    template_parameters = utils.get_template_parameters( template, micc_file
                                                       , verbose=verbose
                                                       , project_name=project_name
                                                       )  
        
    # write a cookiecutter.json file in the cookiecutter template directory
    cookiecutter_json = os.path.join(template, 'cookiecutter.json')
    with open(cookiecutter_json,'w') as f:
        json.dump(template_parameters, f, indent=2)
    
    # run cookiecutter 
    click.echo(f"Creating package {template_parameters['project_name']}")
    cookiecutter( template
                , no_input=True
                , overwrite_if_exists=True
                , output_dir=output_dir
                )
    
    with utils.in_directory(os.path.join(output_dir,template_parameters['project_name'])):
        cmd = ['git','init']
        completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        click.echo(completed_process.stdout)
        if completed_process.stderr:
            click.echo(completed_process.stderr)

    return 0
#===============================================================================
def micc_app( app_name
            , project_path=''
            , verbose=False
            , template='micc-app', micc_file='micc.json'
            ):
    """
    Micc cli subcommand, add a console script (app) to the package. 
    
    :param str app_name: name of the application.
    :param str project_path: if empty, use the current working directory
    :param str template: path to the Cookiecutter_ template.
        (``micc-module`` by default). 
    :param str micc_file: path to the json file containing the template parameters
        descrioptions, relative to ``template``.  Default is ``micc.json``.
    :param bool verbose: verbose output, False by default. 
    """
    template = _resolve_template(template)

    if not project_path:
        project_path = os.getcwd()
    project_name = os.path.basename(project_path)
    template_parameters = utils.get_template_parameters( template, micc_file
                                                       , verbose=verbose
                                                       , app_name=app_name
                                                       , project_name=project_name
                                                       )      
    with in_directory(project_path):
        # write a cookiecutter.json file in the cookiecutter template directory
        cookiecutter_json = os.path.join(template, 'cookiecutter.json')        
        with open(cookiecutter_json,'w') as f:
            json.dump(template_parameters, f, indent=2)
        
        # run cookiecutter 
        click.echo(f"Adding app '{template_parameters['app_name']}' to project '{template_parameters['project_name']}'")
        with in_directory('..'):
            cookiecutter( template
                        , no_input=True
                        , overwrite_if_exists=True
                        )
            
        cli_app_name = 'cli_' + template_parameters['app_name'    ].lower().replace('-', '_')
        package_name =          template_parameters['project_name'].lower().replace('-', '_')
        # docs
        with open('docs/apps.rst',"w") as f:
            f.write(".. include:: ../APPS.rst\n")
        if not os.path.exists("APPS.rst"):
            with open("APPS.rst","w") as f:
                f.write( "Apps\n")
                f.write( "====\n\n")
        with open("APPS.rst","a") as f:
            f.write(f".. automodule:: {package_name}.{cli_app_name}\n")
            f.write( "   :members:\n\n")
        # pyproject.toml
        with open('pyproject.toml','r') as f:
            lines = f.readlines()
        with open('pyproject.toml','w') as f:
            for line in lines:
                f.write(line)
                if line.startswith('[tool.poetry.scripts]'):
                    f.write(f"{template_parameters['app_name']} = {package_name}:{cli_app_name}\n")
                    
#===============================================================================
def micc_module( module_name
               , project_path=''
               , verbose=False
               , template='micc-module', micc_file='micc.json'
               ):
    """
    Micc module subcommand, add a module to the package. 
    
    :param str module_name: name of the module.
    :param str project_path: if empty, use the current working directory
    """
    template = _resolve_template(template)

    if not project_path:
        project_path = os.getcwd()
    project_name = os.path.basename(project_path)
    template_parameters = utils.get_template_parameters( template, micc_file
                                                       , verbose=verbose
                                                       , module_name=module_name
                                                       , project_name=project_name
                                                       )              
    with in_directory(project_path):        
        # write a cookiecutter.json file in the cookiecutter template directory
        cookiecutter_json = os.path.join(template, 'cookiecutter.json')        
        with open(cookiecutter_json,'w') as f:
            json.dump(template_parameters, f, indent=2)
        
        # run cookiecutter 
        click.echo(f"Adding app '{template_parameters['module_name']}' to project '{template_parameters['project_name']}'")
        with in_directory('..'):
            cookiecutter( template
                        , no_input=True
                        , overwrite_if_exists=True
                        )
            
        package_name = template_parameters['project_name'].lower().replace('-', '_')
        # docs
        with open("API.rst","a") as f:
            f.write(f"\n.. automodule:: {package_name}.{template_parameters['module_name']}")
            f.write( "\n   :members:\n\n")
        
#===============================================================================
use_poetry = False
def micc_version(path='.', rule=None, verbose=False):
    """
    Bump the version according to *rule*, and modify the pyproject.toml in 
    *project_path*.
    
    :param str path: path to a pyproject.toml file or its parent directory. 
    :param str rule: one of the valid arguments for the ``poetry version <rule>``
        command.
    """
#     if use_poetry: # what a shame - cannot get this to work`; 
#                    # I filed an issue https://github.com/sdispater/poetry/issues/1182
#         with in_directory(???): 
#             print(1,os.getcwd())
#             i = ArgvInput(['poetry','version',rule])
#             Application().run(i)
#             print(2,os.getcwd())
#             
#     else:
    # We ara hacking around the problem https://github.com/sdispater/poetry/issues/1182:        
    
    # pyproject.toml
    path_to_pyproject_toml = os.path.join(path,'pyproject.toml')
    pyproject_toml = toml.load(path_to_pyproject_toml)
    project_name    = pyproject_toml['tool']['poetry']['name']
    current_version = pyproject_toml['tool']['poetry']['version']
    package_name    = project_name.replace('-','_').replace(' ','_')
    
    if rule is None:
        print(f"Current version: {package_name} v{current_version}")
    else:
        new_version = VersionCommand().increment_version(current_version, rule)
        print(f"{package_name} v{current_version} -> v{new_version}")
        
        utils.replace_version_in_file( path_to_pyproject_toml
                                     , current_version, new_version)
        
        utils.replace_version_in_file( os.path.join(path, package_name, '__init__.py')
                                     , current_version, new_version)

        utils.replace_version_in_file( os.path.join(path, package_name + '.py')
                                     , current_version, new_version)
#===============================================================================
def micc_tag(project_path, verbose=False):
    """
    Create and push a version tag ``vM.m.p`` for the current version.
    
    :param str project_path: path to the project that must be tagged. 
    """
    if not project_path:
        project_path = os.getcwd()
    with utils.in_directory(project_path):
        cmd = f'git tag -a v{__version__} -m "tag version {__version__}"'
        cmd = ['git', 'tag', '-a', f'v{__version__}', '-m', '"tag version {__version__}"']
#         click.echo(f"Running '{cmd}'")
        completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        click.echo(completed_process.stdout)
        if completed_process.stderr:
            click.echo(completed_process.stderr)

        cmd = f'git push origin v{__version__}'
        cmd = ['git', 'push', 'origin', f'v{__version__}']
#         click.echo(f"Running '{cmd}'")
        completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        click.echo(completed_process.stdout)
        if completed_process.stderr:
            click.echo(completed_process.stderr)
#===============================================================================
