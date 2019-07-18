# -*- coding: utf-8 -*-
"""
Utility functions for micc.py
"""
#===============================================================================
import os
import json
import shutil, platform
from contextlib import contextmanager
#===============================================================================
import click
from cookiecutter.main import cookiecutter
import toml
#===============================================================================
from micc import __version__
#===============================================================================
DEBUG = False
#===============================================================================
def path_to_cmake_tools():
    """
    return the path to the folder with the CMake tools.
    """
    return os.path.join(os.path.dirname(__file__),'cmake_tools')
#===============================================================================
# print('path_to_cmake_tools', path_to_cmake_tools())
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
def get_template_parameters(path_to_template, micc_file, **kwargs):
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

    if DEBUG:
        info(f'Micc v{__version__}')
        info( '  Cookiecutter: ' + path_to_template)
        info( '  Micc file   : ' + micc_file)
        info('Template parameters:')
        info( json.dumps(template_parameters, indent=2) )
        
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
def generate( project_path
            , template
            , template_parameters
            , overwrite=False
            ):
    """
    Generate directory tree according to Cookiecutter template.
    """
    with in_directory(project_path):        
        # write a cookiecutter.json file in the cookiecutter template directory
        cookiecutter_json = os.path.join(template, 'cookiecutter.json')
        with open(cookiecutter_json,'w') as f:
            json.dump(template_parameters, f, indent=2)
        
        # run cookiecutter 
        with in_directory(os.path.join(project_path,'..')):
            # expand the Cookiecutte4r template in a temporary directory,
            tmp = '_cookiecutter_tmp_'
            if os.path.exists(tmp):
                shutil.rmtree(tmp)
            os.makedirs(tmp, exist_ok=True)
            cookiecutter( template
                        , no_input=True
                        , overwrite_if_exists=True
                        , output_dir=tmp
                        )
            # find out if there are any files that would be overwritten.
            os_name = platform.system()
            existing_files = []
            new_files = []
            all_dirs = [] 
            for root, dirs, files in os.walk(tmp):
                if root==tmp:
                    continue
                else:
                    root2 = os.path.join(*root.split(os.sep)[1:])
                for d in dirs:
                    all_dirs.append(os.path.join(root2,d))
                for f in files:
                    if os_name=="Darwin" and f==".DS_Store":
                        continue
                    file = os.path.join(root2,f)
#                     print('FILE',file, 'exists =', os.path.exists(file))
                    if os.path.exists(file):                            
                        existing_files.append(file)
                    else:
                        new_files.append(file)
            # Move the generated files from the tmp directory to their
            # destination if and only if
            #   - there are no files to be overwritten, or
            #   - there are files to be overwritten and overwrite is True.
            # Tell the user what is going on.
            print( all_dirs )
            if existing_files:
                if overwrite:
                    for d in all_dirs:
                        os.makedirs(d,exist_ok=True)
                    info("INFO   : The following files are created:")
                    for f in new_files:
                        info(f"       - {f}")
                        shutil.move(os.path.join(tmp,f),f)
                    warning("WARNING: The following files exist already and are overwritten:")
                    for f in existing_files:
                        warning(f"         - {f}")
                        os.remove(f)
                        os.makedirs(os.path.dirname(f), exist_ok=True)
                        shutil.move(os.path.join(tmp,f),f)                    
                else:
                    error("ERROR  : The following files exist already and would be overwritten:")
                    for f in existing_files:
                        error(f"         - {f}")
                    warning("WARNING: No files were added!\n"
                            "         Add '--overwrite' on the command line to overwrite existing files.\n")
                    return 1
            else:
                for d in all_dirs:
                    os.makedirs(d,exist_ok=False)
                info("INFO : The following files are created:")
                for f in new_files:
                    info(f"     - {f}")
                    shutil.move(os.path.join(tmp,f),f)
            # clean up tmp dir
            shutil.rmtree(tmp)
    return 0
#===============================================================================
INFO    = { 'fg'  :'black'}
WARNING = { 'fg'  :'blue' }
ERROR   = { 'fg'  :'red'
          , 'bold':True   }
#===============================================================================
def info(text):
    click.echo(click.style(text,**INFO))
#===============================================================================
def warning(text):
    click.echo(click.style(text,**WARNING))
#===============================================================================
def error(text):
    click.echo(click.style(text,**ERROR))
#===============================================================================
