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
from micc.exceptions import NotAProjectDirectory

use_poetry = True
if use_poetry:
    from poetry.console.application import Application
    from cleo.inputs.argv_input import ArgvInput
    # from poetry.utils.toml_file import TomlFile
else:
    from poetry.console.commands import VersionCommand 
import toml
#===============================================================================
from micc import utils
from micc.utils import in_directory
from micc import __version__
from types import SimpleNamespace
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
_global_options = SimpleNamespace(verbose=False, quiet=False)
CANCEL = -1
#===============================================================================
def micc_create( project_name=''
               , output_dir='.'
               , global_options=_global_options
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
    if not global_options.quiet:
        if utils.is_project_directory(output_dir):
            if click.confirm(f"Directory '{output_dir}' is a project_directory.\n"
                              "Are you sure you want to create a project inside a project?"):
                click.echo("Proceeding...")
            else:
                click.echo(f"Canceled 'micc create ...'")
                return CANCEL            
                
    template = _resolve_template(template)
    template_parameters = utils.get_template_parameters( template, micc_file
                                                       , verbose=global_options.verbose
                                                       , project_name=project_name
                                                       )  
        
    # write a cookiecutter.json file in the cookiecutter template directory
    cookiecutter_json = os.path.join(template, 'cookiecutter.json')
    with open(cookiecutter_json,'w') as f:
        json.dump(template_parameters, f, indent=2)
    
    project_name = template_parameters['project_name']
    overwrite_if_exists = global_options.quiet
    # run cookiecutter 
    click.echo(f"Creating package {project_name}")
    if os.path.exists(os.path.join(output_dir,project_name)):
        if not global_options.quiet:
            msg = f"Project already exists:\n    {os.path.abspath(os.path.join(output_dir,project_name))}\nOverwrite?"
            if not click.confirm(msg):
                click.echo(f"Canceled: 'micc create {project_name}'")
                return CANCEL
            else:
                click.echo("Overwriting ...")
                overwrite_if_exists = True
        
    cookiecutter( template
                , no_input=True
                , overwrite_if_exists=overwrite_if_exists
                , output_dir=output_dir
                )
    
    with utils.in_directory(os.path.join(output_dir,project_name)):
        cmd = ['git','init']
        completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        click.echo(completed_process.stdout)
        if completed_process.stderr:
            click.echo(completed_process.stderr)
    return 0
#===============================================================================
def micc_app( app_name
            , project_path=''
            , global_options=_global_options
            , template='micc-app', micc_file='micc.json'
            ):
    """
    Micc app subcommand, add a console script (app) to the package. 
    
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
        
    if not utils.is_project_directory(project_path):
        raise NotAProjectDirectory(project_path)
    
    project_name = os.path.basename(project_path)
    template_parameters = utils.get_template_parameters( template, micc_file
                                                       , verbose=global_options.verbose
                                                       , app_name=app_name
                                                       , project_name=project_name
                                                       )
    app_name = template_parameters['app_name']
    if not global_options.quiet:
        msg = f"Are you sure to add application '{app_name}' to project '{project_name}'?"
        if not click.confirm(msg,default=False):
            click.echo(f"Canceled: 'micc app {app_name}'")
            return CANCEL
        else:
            click.echo("Proceeding...")
    
    with in_directory(project_path):
        # write a cookiecutter.json file in the cookiecutter template directory
        cookiecutter_json = os.path.join(template, 'cookiecutter.json')        
        with open(cookiecutter_json,'w') as f:
            json.dump(template_parameters, f, indent=2)
        
        # run cookiecutter 
        click.echo(f"Adding app '{app_name}' to project '{project_name}'")
        with in_directory('..'):
            cookiecutter( template
                        , no_input=True
                        , overwrite_if_exists=True
                        )
        cli_app_name = 'cli_' + utils.python_name(app_name)
        package_name =          utils.python_name(project_name)
        
        # docs
        with open('docs/api.rst',"r") as f:
            lines = f.readlines()
        has_already_apps = False
        for line in lines:
            has_already_apps = has_already_apps or line.startswith(".. include:: ../APPS.rst")
        if not has_already_apps:        
            with open('docs/api.rst',"w") as f:
                f.write(".. include:: ../APPS.rst\n\n")
                f.write(".. include:: ../API.rst\n\n")
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
                    f.write(f'{app_name} = "{package_name}:{cli_app_name}"\n')
    return 0
#===============================================================================
def micc_module( module_name
               , project_path=''
               , global_options=_global_options
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
    if not utils.is_project_directory(project_path):
        raise NotAProjectDirectory(project_path)

    project_name = os.path.basename(project_path)        
    template_parameters = utils.get_template_parameters( template, micc_file
                                                       , verbose=global_options.verbose
                                                       , module_name=module_name
                                                       , project_name=project_name
                                                       )   
    module_name = template_parameters['module_name']
    if not global_options.quiet:
        msg = f"Are you sure to add module '{module_name}' to project '{project_name}'?"
        if not click.confirm(msg,default=False):
            click.echo(f"Canceled: 'micc module {module_name}'")
            return CANCEL
        else:
            click.echo("Proceeding...")
            
    py_name = utils.python_name(module_name)
    if not py_name==module_name:
        msg  = f"Not a valid module name: {module_name}\n"
        msg += f"Use {py_name} instead?"
        if not click.confirm(msg):
            click.echo(f"Canceled: 'micc module {module_name}'")
            return CANCEL
        else:
            module_name = py_name
            template_parameters['module_name'] = py_name

           
    with in_directory(project_path):        
        # write a cookiecutter.json file in the cookiecutter template directory
        cookiecutter_json = os.path.join(template, 'cookiecutter.json')        
        with open(cookiecutter_json,'w') as f:
            json.dump(template_parameters, f, indent=2)
        
        # run cookiecutter 
        click.echo(f"Adding module '{module_name}' to project '{project_name}'")
        with in_directory('..'):
            cookiecutter( template
                        , no_input=True
                        , overwrite_if_exists=True
                        )
            # it is a pity that we have to specify overwrite=True, because 
            # cookiecutter chokeson this if the directories exist, even if 
            # all files are different. So, cookiecutter does not allow 
            # additions.
            
            
        package_name = template_parameters['project_name'].lower().replace('-', '_')
        # docs
        with open("API.rst","a") as f:
            f.write(f"\n.. automodule:: {package_name}.{module_name}")
            f.write( "\n   :members:\n\n")
    return 0
#===============================================================================
def micc_version(project_path='.', rule=None, global_options=_global_options):
    """
    Bump the version according to *rule*, and modify the pyproject.toml in 
    *project_path*.
    
    :param str project+path: path to a pyproject.toml file or its parent directory. 
    :param str rule: one of the valid arguments for the ``poetry version <rule>``
        command.
    """
    if not utils.is_project_directory(project_path):
        raise NotAProjectDirectory(project_path)

    if use_poetry:
        # what a shame - cannot get this to work`; 
        # I filed an issue https://github.com/sdispater/poetry/issues/1182
        with utils.in_directory(project_path): 
            print(1,os.getcwd())
            i = ArgvInput(['poetry','version',rule])
            Application().run(i)
            print(2,os.getcwd())
             
    else:
        # We are hacking around the problem https://github.com/sdispater/poetry/issues/1182:        
        path_to_pyproject_toml = os.path.join(project_path,'pyproject.toml')
        pyproject_toml = toml.load(path_to_pyproject_toml)
        project_name    = pyproject_toml['tool']['poetry']['name']
        current_version = pyproject_toml['tool']['poetry']['version']
        package_name    = project_name.replace('-','_').replace(' ','_')
        
        if rule is None:
            click.echo(f"Current version: {package_name} v{current_version}")
        else:
            new_version = VersionCommand().increment_version(current_version, rule)
            if not global_options.quiet:
                msg = f"Package {package_name} v{current_version}\n"\
                      f"Are you sure to move to v{new_version}'?"
                if not click.confirm(msg,default=False):
                    click.echo(f"Canceled: 'micc version {rule}'")
                    return CANCEL
                else:
                    click.echo("Proceeding...")
                    
            else:
                click.echo(f"{package_name} v{current_version} -> v{new_version}")
            
            # update version in pyproject.toml
            utils.replace_version_in_file( path_to_pyproject_toml
                                         , current_version, new_version)
            # update version in package
            if not utils.replace_version_in_file( os.path.join(project_path, package_name, '__init__.py')
                                                , current_version, new_version):
                if not utils.replace_version_in_file( os.path.join(project_path, package_name + '.py')
                                                    , current_version, new_version):
                    click.echo(f"Warning: No package {package_name}/__init__.py and no modute {package_name}.py found.")
        return 0
#===============================================================================
def micc_tag(project_path, global_options=_global_options):
    """
    Create and push a version tag ``vM.m.p`` for the current version.
    
    :param str project_path: path to the project that must be tagged. 
    """
    if not project_path:
        project_path = os.getcwd()
        
    if not utils.is_project_directory(project_path):
        raise NotAProjectDirectory(project_path)
    # There is not really a reason to be careful when creating a tag
    # if not global_options.quiet:
    #     project_name, version = utils.get_name_version(project_path)
    #     msg = f"Are you sure to create tag 'v{version}' for project '{project_name}'?"
    #     if not click.confirm(msg,default=False):
    #         click.echo("Canceled: 'micc tag'")
    #         return -1
    #     else:
    #         click.echo("Proceeding...")
        
    with utils.in_directory(project_path):
        cmd = ['git', 'tag', '-a', f'v{__version__}', '-m', f'"tag version {__version__}"']
        if global_options.verbose:
            click.echo(f"Running '{' '.join(cmd)}'")
        completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        click.echo(completed_process.stdout)
        if completed_process.stderr:
            click.echo(completed_process.stderr)

        cmd = ['git', 'push', 'origin', f'v{__version__}']
        if global_options.verbose:
            click.echo(f"Running '{' '.join(cmd)}'")
        completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        click.echo(completed_process.stdout)
        if completed_process.stderr:
            click.echo(completed_process.stderr)
    return 0
#===============================================================================
