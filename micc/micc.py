# -*- coding: utf-8 -*-
"""
Main module.
"""
#===============================================================================
import os
import json
from shutil import move
from pathlib import Path
import tomlkit
#===============================================================================
import click
from cookiecutter.main import cookiecutter
from micc.__version__ import __version__
from poetry.console.commands import VersionCommand 
from poetry.utils.toml_file import TomlFile
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
def get_template_parameters(micc_file,verbose=False):
    """
    Read the template parameter descriptions from the micc file, and
    prompt the user for supplying the values for the parameters with an
    empty string as default.     
    
    :returns: a dict of (parameter,value) pairs.
    """
    with open(micc_file,'r') as f:
        template_parameters = json.load(f)

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
def micc_create( template='micc-module', micc_file='micc.json'
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
    template_parameters = get_template_parameters(path_to_micc_json,verbose)
        

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
def micc_version(project_path, rule):
    
    pyproject_toml_path = get_pyproject_toml_path(os.path.join(project_path,'pyproject.toml'))
    
    if pyproject_toml_path is None:
        raise FileNotFoundError('pyproject.toml')
    
    pyproject_toml = TomlFile(pyproject_toml_path)
    content = pyproject_toml.read()
    tool = content['tool']
    tool_poetry = tool['poetry']
    current_version = tool_poetry['version']
    name = tool_poetry['name']
    if rule is None:
        print(f"Current version: {name} v{current_version}")
    else:
        vc = VersionCommand()
        version = vc.increment_version(current_version, rule)
        print(version)
        tool_poetry['version'] = version.text
        tool['poetry'] = tool_poetry
        pyproject_toml.write(tool)
        print(f"New version: {name} v{version}")

#===============================================================================