# -*- coding: utf-8 -*-
"""
Created on 18 Nov 2019

@author: etijskens

Module et_micc.utils
====================

Utility functions for et_micc.
"""
import os
import subprocess
import copy
from pathlib import Path
from contextlib import contextmanager

from et_micc.tomlfile import TomlFile
import et_micc.logging

def pep8_module_name(name):
    """Convert a module name to a PEP8 compliant module name.
    
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


def is_project_directory(path):
    """Verify that the directory :file:`path` is a project directory. 
    
    :param Path path: path to a directory.
    :returns: bool.
    
    As a sufficident condition, we request that 
    
    * there is a pyproject.toml file, exposing ``['tool']['poetry']['name']``
    * that there is a python package or module with that name.
    """
    if not isinstance(path, Path):
        path = Path(path)
        
    path_to_pyproject_toml = str(path /'pyproject.toml')
    
    try:
        toml = TomlFile(path_to_pyproject_toml)
        _ = toml['tool']['poetry']['name']
    except Exception:
        return False

    return bool(package_or_module(path))
    

def package_or_module(path):
    """Test if *path* contains a python module or package.
    :param Path path: path to a directory.
    :returns: 'package' or 'module' if *path* contains a python package or
      module, resp., or None if it contains neither.
    """
    project_name = path.name
    package_name = pep8_module_name(project_name)
    if (path / package_name / '__init__.py').exists():
        # python package found
        return 'package'
    elif (path / (package_name + '.py')).exists():
        # python module found
        return 'module'
    else:
        return None
    

@contextmanager
def in_directory(path):
    """Context manager for changing the current working directory while the body of the
    context manager executes.
    """
    previous_dir = os.getcwd()
    os.chdir(str(path)) # the str method takes care of when path is a Path object
    yield os.getcwd()
    os.chdir(previous_dir)


def execute(cmds,logfun=None,stop_on_error=True,env=None):
    """Executes a list of OS commands, and log with logfun.
    
    :param list cmds: list of OS commands (=list of list of str) or a single command (list of str)
    :parma callable logfun: a function to write output, typically 
        ``logging.getLogger('et_micc').debug``.
    :returns int: return code of first failing command, or 0 if all
        commanbds succeed.
    """
    if isinstance(cmds[0],str):
        # this is a single command
        cmds = [cmds]
        
    for cmd in cmds:
        with et_micc.logging.log(logfun, f"> {' '.join(cmd)}"):
            completed_process = subprocess.run(cmd, capture_output=True,env=env)
            if not logfun is None:
                if completed_process.returncode:
                    logfun0 = logfun
                    logfun = logfun.__self__.warning
                    logfun(f"> {' '.join(cmd)}")
                if completed_process.stdout:
                    logfun(' (stdout)\n' + completed_process.stdout.decode('utf-8'))
                if completed_process.stderr:
                    logfun(' (stderr)\n' + completed_process.stderr.decode('utf-8'))
                if completed_process.returncode:
                    logfun = logfun0
            if completed_process.returncode:
                if stop_on_error:
                    return completed_process.returncode
    return 0


def get_project_path(p):
    """Look for a project directory in the parents of path :py:obj:`p`.
    
    :param Path p:
    :returns: the nearest directory above :py:obj:`p` that is project directory.
    :raise: RuntimeError if :py:obj:`p` is noe inside a project directory.
    """
    root = Path('/')
    p = Path(p).resolve()
    p0 = copy.copy(p)
    while not is_project_directory(p):
        p = p.parent
        if p==root:
            raise RuntimeError(f"Folder {p0} is not inside a Python project.")
    return p


#eof