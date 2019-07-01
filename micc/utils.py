# -*- coding: utf-8 -*-
"""
Utility functions for micc.py
"""
#===============================================================================
import os
import json
import click
from contextlib import contextmanager
#===============================================================================
import toml
#===============================================================================
from micc import __version__
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
def get_template_parameters(path_to_template, micc_file, verbose, **kwargs):
    """
    Read the template parameter descriptions from the micc file, and
    prompt the user for supplying the values for the parameters with an
    empty string as default.     
    
    :returns: a dict of (parameter,value) pairs.
    """
    micc_file = os.path.join(path_to_template, micc_file)

    with open(micc_file, 'r') as f:
        template_parameters = json.load(f)
      
    for kw,arg in kwargs.items():  
        template_parameters[kw]['default'] = arg 
    
    for key,value in template_parameters.items():
        default = value['default']
        if bool(default):
            value = default
        else:
            kwargs = value
#             text = kwargs['text']
#             del kwargs['msg']
            if 'type' in kwargs:
                kwargs['type'] = eval(kwargs['type'])
            click.echo('')
            value = False
            while not value:
                value = click.prompt(**kwargs,show_default=False)
        template_parameters[key] = value

    if verbose:
        click.echo(f'Micc v{__version__}')
        click.echo( '  Cookiecutter: ' + path_to_template)
        click.echo( '  Micc file   : ' + micc_file)
        click.echo('Template parameters:')
        click.echo( json.dumps(template_parameters, indent=2) )
        
    return template_parameters
#===============================================================================
@contextmanager
def in_directory(path):
    """
    Run some code in  working directory *path* (and switch back to the current
    working directory when done. 
    """
    previous_dir = os.getcwd()
    os.chdir(path)
    yield os.getcwd()
    os.chdir(previous_dir)
#===============================================================================
def replace_version_in_file(filepath,current_version,new_version):
    if os.path.exists(filepath):
        print('    Updating :',filepath)
        if os.path.basename(filepath) == "pyproject.toml":
            fmt = 'version = "{}"'
        else:
            fmt = '__version__ = "{}"'
        old = fmt.format(current_version)
        new = fmt.format(new_version)
        replace_in_file(filepath,old,new)
        return True
    else:
        return False
#===============================================================================
def replace_in_file(filepath,old,new):
    with open(filepath) as f:
        content_as_string = f.read()
    content_as_string = content_as_string.replace(old,new)
    with open(filepath,"w") as f:
        f.write(content_as_string)
#===============================================================================
def is_project_directory(path):
    """
    Verify that the dir at path is a project directory. As a sufficident 
    condition, we request that there is a pyproject.toml file, exposing 
    ~`['tool']['poetry']['name']``, and that there is a python package or module 
    with that name.
    """
    
    path_to_pyproject_toml = os.path.join(path,'pyproject.toml')
    
    try:
        project_name = toml.load(path_to_pyproject_toml)['tool']['poetry']['name']
        
    except:
        return False
    
    if  os.path.exists(os.path.join(path, python_name(project_name), '__init__.py')):
        # python package found
        return True
    elif os.path.exists(os.path.join(path, project_name + '.py')):
        return True
        # simple python module found
    else:
        return False
#===============================================================================
def get_name_version(project_path):
    """
    Read name and version of this project from the pyproject.toml file.
    """
    path_to_pyproject_toml = os.path.join(project_path,'pyproject.toml')
    pyproject_toml = toml.load(path_to_pyproject_toml)
    return ( pyproject_toml['tool']['poetry']['name']
           , pyproject_toml['tool']['poetry']['version']
           )
#===============================================================================
def python_name(filename):
    """
    Convert a *filename* to a python name:
    
    * lowercase
    * whitespace -> underscore 
    * dash -> underscore 
    """
    python_name = filename.lower().replace('-', '_')
    return python_name
#===============================================================================
