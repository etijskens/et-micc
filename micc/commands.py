# -*- coding: utf-8 -*-
"""
Main module.
"""
#===============================================================================
import os
import json
import subprocess
from shutil import move
#===============================================================================
import click
from cookiecutter.main import cookiecutter
from poetry.console.commands import VersionCommand 
# from poetry.utils.toml_file import TomlFile
# from poetry.console.application import Application
# from cleo.inputs.argv_input import ArgvInput
import toml
#===============================================================================
from micc import __version__
from micc import utils
from micc.utils import in_directory
#===============================================================================
def micc_create( project_name=''
               , template='micc-module', micc_file='micc.json'
               , output_dir='.'
               , verbose=False
               ):
    """
    Create a new project skeleton. 
    
    :param str project_name: the name of the project to be created. If empty str,
    :param str template: path to the Cookiecutter_ template.
        (``micc-module`` by default). 
    :param str micc_file: the json file containing the template parameters
        descrioptions. Default is ``micc.json`` in ``template``.
    :param str output_dir: path where the project will be created. By default
        the current directory.
    :param bool verbose: verbose output, False by default. 
    """
    template = os.path.expanduser(template)
    if template in ['micc-module']:        
        template = os.path.join(os.path.dirname(__file__), template)
    if not os.path.exists(template):
        raise FileNotFoundError('ERROR: Missing cookiecutter template: ' + 
                                utils.file_not_found_msg(template, looking_for='folder')
                                )
    else:
        if verbose:
            click.echo(f'Micc v{__version__}')
            click.echo( '  Cookiecutter: ' + template)
        
    path_to_micc_json = os.path.join(template,micc_file)
    if not os.path.exists(path_to_micc_json):        
        raise FileNotFoundError('ERROR: Missing micc file: ' + utils.file_not_found_msg(micc_file))
    else:
        if verbose:
            click.echo('  Micc file   : ' + micc_file)
            
    template_parameters = utils.get_template_parameters( path_to_micc_json
                                                       , project_name=project_name
                                                       )  
    if verbose:
        click.echo('\ntemplate parameters:')
        click.echo( json.dumps(template_parameters, indent=2) )
    
    cookiecutter_json = os.path.join(template, 'cookiecutter.json')
    if os.path.exists(cookiecutter_json):
        cookiecutter_orig_json = os.path.join(template, 'cookiecutter.orig.json')
        # make way for a new cookiecutter.json file
        if not os.path.exists(cookiecutter_orig_json):
            # make a copy of the original cookiecutter.json file if there isn't one already.
            move(cookiecutter_json, cookiecutter_orig_json)
    
    # write a cookiecutter.json file in the cookiecutter template directory
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
use_poetry = False
def micc_version(path='.', rule=None):
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
def micc_tag(project_path):
    """
    Create and push a version tag ``vM.m.p`` for the current version.
    
    :param str project_path: path to the project that must be tagged. 
    """
    with utils.in_directory(project_path):
        cmd = f'git tag -a v{__version__} -m "tag version {__version__}"'
        click.echo(f"Running '{cmd}'")
        subprocess.run(cmd)

        cmd = f'git push origin v{__version__}'
        click.echo(f"Running '{cmd}'")
        subprocess.run(cmd)
#===============================================================================
def micc_app(app_name,project_path='',verbose=False):
    """
    Micc cli subcommand, add a console script (app) to the package. 
    
    :param str app_name: name of the application.
    :param str project_path: if empty, use the current working directory
    """
    template = os.path.join(os.path.dirname(__file__), 'micc-app')
    path_to_micc_json = os.path.join(template,'micc.json')            
    
    if not project_path:
        project_path = os.getcwd()
        
    with in_directory(project_path):
        project_name = os.path.basename(project_path)
        template_parameters = utils.get_template_parameters( path_to_micc_json
                                                           , app_name=app_name
                                                           , project_name=project_name
                                                           ) 
        if verbose:
            click.echo('\ntemplate parameters:')
            click.echo( json.dumps(template_parameters, indent=2) )
        
        cookiecutter_json = os.path.join(template, 'cookiecutter.json')
#         if os.path.exists(cookiecutter_json):
#             cookiecutter_orig_json = os.path.join(template, 'cookiecutter.orig.json')
#             # make way for a new cookiecutter.json file
#             if not os.path.exists(cookiecutter_orig_json):
#                 # make a copy of the original cookiecutter.json file if there isn't one already.
#                 move(cookiecutter_json, cookiecutter_orig_json)
        
        # write a cookiecutter.json file in the cookiecutter template directory
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
