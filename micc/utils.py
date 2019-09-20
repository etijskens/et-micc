# -*- coding: utf-8 -*-
"""
Utility functions for micc.py
"""
import os
import json
import shutil, platform
from contextlib import contextmanager

import click
from cookiecutter.main import cookiecutter
import toml
from pathlib import Path
from micc import __version__

DEBUG = False
CANCEL = -1


def path_to_cmake_tools():
    """
    return the path to the folder with the CMake tools.
    """
    return os.path.join(os.path.dirname(__file__),'cmake_tools')


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


def replace_version_in_file(filepath,current_version,new_version):
    if os.path.exists(filepath):
        click.echo('    Updating : ' + filepath)
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
    Verify that the directory ``path`` is a project directory. 
    As a sufficident condition, we request that 
    
    * there is a pyproject.toml file, exposing ``['tool']['poetry']['name']``
    * that there is a python package or module with that name.
    
    :param Path path:
    """
    if not isinstance(path, Path):
        path = Path(path)
    path_to_pyproject_toml = str(path /'pyproject.toml')
    
    try:
        project_name = toml.load(path_to_pyproject_toml)['tool']['poetry']['name']
    except:
        return False
    
    package_name = convert_to_valid_module_name(project_name)
    if (path / package_name / '__init__.py').exists():
        # python package found
        return True
    elif (path / (package_name + '.py')).exists():
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
def convert_to_valid_module_name(name):
    """
    Convert a *name* to a python name:
    
    * lowercase
    * whitespace -> underscore 
    * dash -> underscore 
    * if leading numeric character, prepend '_'
      Names like this are discouraged by https://www.python.org/dev/peps/pep-0008/#package-and-module-names,
      but so are, names starting with a numeric character.
    """
    
    if name[0].isnumeric():
        name = '_'+name
    valid_module_name = name.lower().replace('-', '_').replace(' ', '_')
    return valid_module_name


def module_exists(project_path, module_name):
    """
    Test if there is already a module with name ``module_name`` in this project.
    This can be:

        * a simple python module  ``<package_name>/<module_name>.py``
        * a generel python module ``<package_name>/<module_name>/__init__.py``
        * a f2py module           ``<package_name>/f2py_<module_name>``
        * a cpp module            ``<package_name>/cpp_<module_name>``
        
    :param str project_path: project path
    :param str module_name: module name
    :returns: bool
    """
    package_dir = os.path.join( project_path, convert_to_valid_module_name(os.path.basename(project_path)))
    
    exists_py = ( os.path.isdir (os.path.join(package_dir,module_name,'__init__.py'))
               or os.path.isfile(os.path.join(package_dir,module_name + '.py')) 
                )
    exists_cpp  = os.path.isdir (os.path.join(package_dir,'cpp' + module_name))
    exists_f2py = os.path.isdir (os.path.join(package_dir,'cpp' + module_name))

    return exists_cpp or exists_f2py or exists_py


def app_exists(project_path, app_name):
    """
    Test if there is already an app with name ``app_name`` in this project.
    
        * ``<package_name>/cli_<app_name>.py``
        
    :param str project_path: project path
    :param str app_name: app name
    :returns: bool
    """
    package_dir = os.path.join( project_path, convert_to_valid_module_name(os.path.basename(project_path)))
    
    exists_app = os.path.isfile(os.path.join(package_dir,app_name,'__init__.py'))

    return exists_app

### is this still usefull?
INFO    = { 'fg'  :'black'}
WARNING = { 'fg'  :'blue' }
ERROR   = { 'fg'  :'red'
          , 'bold':True   }

def info(text):
    click.echo(click.style(text,**INFO))


def warning(text):
    click.echo(click.style(text,**WARNING))


def error(text):
    click.echo(click.style(text,**ERROR))
###



def is_simple_project(project_path):
    """Find out if this project is a simple or general python project."""
    
    if project_path == '.':
        project_path = os.path.abspath(project_path)
    package_name = convert_to_valid_module_name(os.path.basename(project_path))
    package_dir = os.path.join(project_path, package_name)
    
    has_module  = os.path.isfile( os.path.join(project_path, package_name + ".py") )

    has_package = os.path.isdir(package_dir) 
    if has_package:
        if not os.path.exists(os.path.join(package_dir,"__init__.py")):
            has_package = False
    
    if has_module and has_package:
        raise RuntimeError(f"ERROR: This project has both '{package_dir}.py' and '{package_dir}/__init__.py'.")
 
    if not has_module and not has_package:
        raise RuntimeError(f"ERROR: This directory has neither '{package_dir}.py' nor '{package_dir}/__init__.py'.")
    
    return has_module


def get_parent_dir(p):
    """
    Return the parent directory of ``p``. If ``p`` is ``'/'`` an empty string
    (``' '``) is returned.
    """
    if p[0] != os.sep:
        p = os.path.abspath(p)
    if p[-1] == os.sep:
        p = p[:-1]
    p = os.path.dirname(p)
    return p


def verify_name(name,obj,force_python_name=False):
    """
    Verifies ``name`` for module and app objects. 
    
    :param str name: name of a module or app. If name is empty, the user is
        prompted to provide a name.
    :param str obj: either ``'module'`` or ``'app'``. if ``obj`` is ``'module'``,
        or ``force_python_name`` is ``True``, then it is checked if name is a
        valid name for a python_module. If not, name is converted 
    """
    valid_objects = ('module', 'app')
    assert obj in valid_objects, f"invalid object {obj}, expecting {valid_objects}."
    if not name:
        name = click.prompt(f"Enter {obj} name (leave empty to quit)",default='',show_default=False)
        if not name:
            warning(f"No {obj} name provided, exiting.")
            return CANCEL
        
    if obj=='module' or force_python_name:
        while True:
            py_name = convert_to_valid_module_name(name)
            if py_name==name:
                # name is ok 
                return name
            
            msg = (f"Not a valid python name: {name}\n"
                   f"Valid python names\n"
                   f" - must be lower case,\n"
                   f" - must not contain any special characters other than '_',\n"
                   f" - must not start with a number.\n"
                   f"Press Enter to use {py_name} instead.\n"
                   f"Press a+Enter to abort\n"
                   f"Any string + Enter to propose a new name:")
            name = click.prompt(msg,default='',show_default=False)
            if not name:
                # accepting py_name
                return py_name
            elif name=='a':
                warning(f"Exiting.")
                return CANCEL
            # continue with verifying new name provided.
            

#===============================================================================
@contextmanager
def log(logfun, begin_msg='doing', end_msg='done.'):
    """
    Print a start and stop message when executing a task.

    :param logfun: function that writes  e.g. ``logging.info`
    :param str begin_msg: print this before body is executed
    :param str end_msg: print this after body is executed
    :param singleline: generates a single line execution trace as in
        `<begin_msg> ... <end_msg>`. Calling print2stderr may obfuscate this.
    """
    if logfun:
        if end_msg is None:
            logfun(begin_msg)
        else:
            logfun(begin_msg+' ...')
        yield
        if not end_msg is None:
            logfun(f"{begin_msg} ... {end_msg}\n")
#===============================================================================

# end of file