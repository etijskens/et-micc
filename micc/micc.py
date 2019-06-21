# -*- coding: utf-8 -*-
"""
Main module.
"""
#===============================================================================
import os
import json
from shutil import move
from pathlib import Path
from contextlib import contextmanager
#===============================================================================
import click
from cookiecutter.main import cookiecutter
from poetry.console.commands import VersionCommand 
from poetry.utils.toml_file import TomlFile
from poetry.console.application import Application
from cleo.inputs.argv_input import ArgvInput
#===============================================================================
from micc.__version__ import __version__
from distutils.sysconfig import get_python_inc
#===============================================================================
def file_not_found_msg(path, looking_for='File'):
    """
    This function constructs an error message for when a file is not found. 
    If the file is referred to with a relative path, the current working 
    directory is reported to be more informative.
    
    :param str path: path to file or directory.
    :param str looking_for: description of what *path* was supposed to refer
        to: 'file', 'directory', ...
    """
    if path.startswith('~') or path.startswith(os.sep):
        msg = f"{looking_for} {path} not found."
    else:
        msg = f"{looking_for} {path} not found in {os.getcwd()}."
    return msg

#===============================================================================
def get_template_parameters(micc_file, project_name='', verbose=False):
    """
    Read the template parameter descriptions from the micc file, and
    prompt the user for supplying the values for the parameters with an
    empty string as default.     
    
    :returns: a dict of (parameter,value) pairs.
    """
    with open(micc_file,'r') as f:
        template_parameters = json.load(f)
        
    if project_name:
        template_parameters['project_name']['default'] = project_name 

    if verbose:
        click.echo("  template parameters:")
        click.echo( json.dumps(template_parameters, indent=2) )
    
    for k,v in template_parameters.items():
        default = v['default']
        if bool(default):
            value = default
        else:
            kwargs = v
#             text = kwargs['text']
#             del kwargs['msg']
            if 'type' in kwargs:
                kwargs['type'] = eval(kwargs['type'])
            click.echo('')
            value = False
            while not value:
                value = click.prompt(**kwargs,show_default=False)
        template_parameters[k] = value
        
    if verbose:
        click.echo('\ntemplate parameters:')
        click.echo( json.dumps(template_parameters, indent=2) )

    return template_parameters
#===============================================================================
def get_pyproject_toml_path(source_file):
    """
    Try to locate a pyproject.toml file in one of the parent directories.
    """
    d = Path(source_file)
    result = None
    while d.parent != d and result is None:
        d = d.parent
        pyproject_toml_path = d / 'pyproject.toml'
        if pyproject_toml_path.exists():
            result = pyproject_toml_path
#             with open(file=str(pyproject_toml_path)) as f:
#                 pyproject_toml = tomlkit.parse(string=f.read())
#                 if 'tool' in pyproject_toml and 'poetry' in pyproject_toml['tool']:
#                     # noinspection PyUnresolvedReferences
#                     result = pyproject_toml['tool']['poetry']['version']
    return result
#===============================================================================
def micc_create( project_name
               , template='micc-module', micc_file='micc.json'
               , output_dir='.'
               , verbose=False
               ):
    """
    Create a project skeleton. 
        
    :param str template: path to the Cookiecutter_ template.
        (``micc-module`` by default). 
    :param str micc_file: the json file containing the template parameters
        descrioptions. Default is ``micc.json`` in ``template``.
    :param str output_dir: path where the project will be created. By default
        the current directory.
    :param bool verbose: verbose output, False by default. 
    """
    click.echo('Micc v'+__version__)
    template = os.path.expanduser(template)
    if template in ['micc-module']:        
        template =  os.path.join(os.path.dirname(__file__),template)
    if not os.path.exists(template):
        raise FileNotFoundError('ERROR: Missing cookiecutter template: ' +
                                file_not_found_msg(template, looking_for='folder')
                                )
    else:
        if verbose: click.echo('  Cookiecutter: ' + template)
        
    path_to_micc_json = os.path.join(template,micc_file)
    if not os.path.exists(path_to_micc_json):        
        raise FileNotFoundError('ERROR: Missing micc file: '+file_not_found_msg(micc_file))
    else:
        if verbose: click.echo('  Micc file   : ' + micc_file)
    template_parameters = get_template_parameters(path_to_micc_json,project_name=project_name,verbose=verbose)
        

    cookiecutter_json = os.path.join(template, 'cookiecutter.json')
    if os.path.exists(cookiecutter_json):
        cookiecutter_orig_json = os.path.join(template, 'cookiecutter.orig.json')
        # make way for a new cookiecutter.json file
        if not os.path.exists(cookiecutter_orig_json):
            # make a copy of the original cookiecutter.json file if there isn't one already.
            move(cookiecutter_json, cookiecutter_orig_json)
#         else:
#             os.remove(cookiecutter_json)
    
    
    # write a cookiecutter.json file in the cookiecutter template directory
    with open(cookiecutter_json,'w') as f:
        json.dump(template_parameters, f, indent=2)
    
    # run cookiecutter 
    click.echo(f"Creating {template} from {micc_file}")
    click.echo(f"      in {output_dir}")
    cookiecutter( template
                , no_input=True
                , overwrite_if_exists=True
                , output_dir=output_dir
                )
    click.echo( "Done.")
    
    return 0
#===============================================================================
@contextmanager
def in_directory(path):
    previous_dir = os.getcwd()
    os.chdir(path)
    yield os.getcwd()
    os.chdir(previous_dir)
#===============================================================================
def get_pyproject_toml_document(path_to_pyproject_toml):
    """
    Read a pyproject.toml file and provide read-only access.
    """
    if not os.path.exists(path_to_pyproject_toml):
        raise FileNotFoundError(path_to_pyproject_toml)
    pyproject_toml = TomlFile(path_to_pyproject_toml).read()
    return pyproject_toml
#===============================================================================
def micc_version(path='.', rule=None):
    """
    Bump the version according to *rule*, and modify the pyproject.toml in 
    *project_path*.
    
    :param str path: path to a pyproject.toml file or its parent directory. 
    :param str rule: one of the valid arguments for the ``poetry version <rule>``
        command.
    """
    if not path.endswith('pyproject.toml'):
        path = os.path.join(path, 'pyproject.toml')
    pyproject_toml = get_pyproject_toml_document(path)
    project_name    = pyproject_toml['tool']['poetry']['name']
    current_version = pyproject_toml['tool']['poetry']['version']
    if rule is None:
        print(f"Current version: {project_name} v{current_version}")
    else:
        next_version = VersionCommand().increment_version(current_version, rule)
        print(f"{project_name} v{current_version} -> v{next_version}")
        # Hacking around the problem below:        
        with open(path) as f:
            content_as_string = f.read()
        content_as_string = content_as_string.replace(f'version = "{current_version}"'
                                                     ,f'version = "{next_version.text}"'
                                                     )
        with open(path,"w") as f:
            f.write(content_as_string)
        
# none of this seems to work ... i filed an issue https://github.com/sdispater/poetry/issues/1182
#         with in_directory(project_path): 
#             i = ArgvInput(['poetry','version',rule])
#             Application().run(i)
#             pyproject_toml_path = os.path.join(project_path,  'pyproject.toml')
#             pyproject_toml = TomlFile(pyproject_toml_path)
#             content = pyproject_toml.read()
#             current_version = content['tool']['poetry']['version']
#             vc = VersionCommand()
#             version = vc.increment_version(current_version, rule)
#             print(version)
#             content['tool']['poetry'].__setitem__('version', version.text ) 
#             print(content['tool']['poetry']['version']) 
#             pyproject_toml.write(content)
#     pyproject_toml_path = get_pyproject_toml_path(os.path.join(project_path,'pyproject.toml'))
#     
#     if pyproject_toml_path is None:
#         raise FileNotFoundError('pyproject.toml')
#     
#     pyproject_toml = TomlFile(pyproject_toml_path)
#     content = pyproject_toml.read()
#     tool = content['tool']
#     tool_poetry = tool['poetry']
#     current_version = tool_poetry['version']
#     name = tool_poetry['name']
#     if rule is None:
#         print(f"Current version: {name} v{current_version}")
#     else:
#         vc = VersionCommand()
#         version = vc.increment_version(current_version, rule)
#         print(version)
#         tool_poetry['version'] = version.text
#         tool['poetry'] = tool_poetry
#         pyproject_toml.write(tool)
#         print(f"New version: {name} v{version}")

#===============================================================================