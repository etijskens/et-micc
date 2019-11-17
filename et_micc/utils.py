# -*- coding: utf-8 -*-
"""
Module et_micc.utils
=================

Utility functions for et_micc.py.
"""
import os, sys, subprocess, logging, sysconfig, copy
from contextlib import contextmanager
# import toml
from et_micc.tomlfile import TomlFile

from pathlib import Path
from datetime import datetime
import et_micc.logging_tools


def get_extension_suffix():
    return sysconfig.get_config_var('EXT_SUFFIX')


def path_to_cmake_tools():
    """Return the path to the folder with the CMake tools."""
    
    p = (Path(__file__) / '..' / 'cmake_tools').resolve()
    return str(p)


@contextmanager
def in_directory(path):
    """Context manager for changing the current working directory while the body of the
    context manager executes.
    """
    previous_dir = os.getcwd()
    os.chdir(str(path)) # the str method takes care of when path is a Path object
    yield os.getcwd()
    os.chdir(previous_dir)


def replace_version_in_file(filepath,current_version,new_version):
    """Replace the version string in a file.
    
    :param Path filepath: Path to the file.
    """
    if filepath.exists():
        if filepath.name == "pyproject.toml":
            fmt = 'version = "{}"'
        else:
            fmt = '__version__ = "{}"'
        old = fmt.format(current_version)
        new = fmt.format(new_version)
        replace_in_file(filepath,old,new)
        return True
    else:
        return False


def replace_in_file(filepath,old,new):
    """Replace :py:obj:`old` string with :py:obj:`new` in a file.
    
    :param Path filepath: 
    """
    with filepath.open() as f:
        content_as_string = f.read()
    content_as_string = content_as_string.replace(old,new)
    with filepath.open(mode="w") as f:
        f.write(content_as_string)


def is_project_directory(path,raise_if=None):
    """Verify that the directory :file:`path` is a project directory. 
    
    As a sufficident condition, we request that 
    
    * there is a pyproject.toml file, exposing ``['tool']['poetry']['name']``
    * that there is a python package or module with that name.
    
    :param Path path:
    :param bool raise_if: If True, raise ``RuntimeError`` if the test succeeds.
        If False, raise ``RuntimeError`` if the test fails.
        If None, do not raise.
    :returns: bool.
    :raises: RuntimeError.
    """
    if not isinstance(path, Path):
        path = Path(path)
    path_to_pyproject_toml = str(path /'pyproject.toml')
    
    try:
        toml = TomlFile(path_to_pyproject_toml)
        project_name = toml['tool']['poetry']['name']
        rv = True
    except Exception as e:
        rv = False

    if rv:
        package_name = convert_to_valid_module_name(project_name)
        if (path / package_name / '__init__.py').exists():
            # python package found
            rv = True
        elif (path / (package_name + '.py')).exists():
            rv = True
        else:
            rv = False
    
    # the stuff below could be achieve through a decorator, but it is a bit
    # complex, and we need it only three times
    if raise_if is None or raise_if!=rv:
        # must not raise
        return rv
    # must raise in all other cases
    elif raise_if==True:
        x = RuntimeError(f"Project path '{path}' is a project directory.")
        x.path = path
    elif raise_if==False:
        x = RuntimeError(f"Project path '{path}' is NOT an project directory.")
        x.path = path
    raise x


def convert_to_valid_module_name(name):
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


def py_module_exists(project_path, module_name):
    """Test if there is already a python module with name :py:obj:`module_name` 
    in the project at :file:`project_path`.
        
    :param Path project_path: project path
    :param str module_name: module name
    :returns: bool
    """
    file = project_path / convert_to_valid_module_name(project_path.name) / f'{module_name}.py'
    return file.is_file()


def py_package_exists(project_path, module_name):
    """Test if there is already a python package with name :py:obj:`module_name` 
    in the project at :file:`project_path`.
        
    :param Path project_path: project path
    :param str module_name: module name
    :returns: bool
    """
    return (project_path / convert_to_valid_module_name(project_path.name) / module_name / '__init__.py').is_file()


def f2py_module_exists(project_path, module_name):
    """Test if there is already a f2py module with name py:obj:`module_name` in this project.
        
    :param Path project_path: project path
    :param str module_name: module name
    :returns: bool
    """
    return (project_path / convert_to_valid_module_name(project_path.name) / ('f2py_' + module_name)/ f"{ module_name}.f90").is_file() 


def cpp_module_exists(project_path, module_name):
    """Test if there is already a cpp module with name py:obj:`module_name` in this project.
        
    :param Path project_path: project path
    :param str module_name: module name
    :returns: bool
    """
    return (project_path / convert_to_valid_module_name(project_path.name) / ('cpp_' + module_name)/ f"{ module_name}.cpp").is_file() 


def module_exists(project_path, module_name):
    """Test if there is already a module with name py:obj:`module_name` in this project.

    :param Path project_path: project path
    :param str module_name: module name
    :returns: bool
    """
    return (  py_module_exists(project_path, module_name)
         or  py_package_exists(project_path, module_name)
         or  cpp_module_exists(project_path, module_name)
         or f2py_module_exists(project_path, module_name)
           )

def app_exists(project_path, app_name):
    """Test if there is already an app with name ``app_name`` in this project.
    
    * :file:`<package_name>/cli_<app_name>.py`
        
    :param Path project_path: project path
    :param str app_name: app name
    :returns: bool
    """
    return (project_path / convert_to_valid_module_name(project_path.name) / f"cli_{app_name}.py").is_file()
    

def is_module_project(project_path, raise_if=None):
    """Find out if this project is a module python project.
    
    :param Path project_path: project path
    :param bool raise_if: If True, raise ``RuntimeError`` if the test succeeds.
        If False, raise ``RuntimeError`` if the test fails.
        If None, do not raise.
    :returns: bool.
    :raises: RuntimeError.
    """
    package_name = convert_to_valid_module_name(project_path.name)
    rv = (project_path / f'{package_name}.py').is_file()
    if raise_if is None or raise_if!=rv:
        return rv
    elif raise_if==True:
        x = RuntimeError(f"Directory '{project_path}' is a module project")
        x.path = project_path
    elif raise_if==False:
        x = RuntimeError(f"Directory '{project_path}' is NOT a module project")
        x.path = project_path
    raise x
    

def is_package_project(project_path, raise_if=None):
    """Find out if this project is a package python project.
    
    :param Path project_path: project path
    """    
    package_name = convert_to_valid_module_name(project_path.name)
    rv = (project_path / package_name / '__init__.py').is_file()

    if raise_if is None or raise_if!=rv:
        return rv
    elif raise_if==True:
        x = RuntimeError(f"Directory '{project_path}' is a package project")
        x.path = project_path
    elif raise_if==False:
        x = RuntimeError(f"Directory '{project_path}' is NOT a package project")
        x.path = project_path
    raise x


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
        with et_micc.logging_tools.log(logfun, f"> {' '.join(cmd)}"):
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


def is_conda_python():
    """Test if the user's environment is a conda Python environment.
    
    see https://stackoverflow.com/questions/21282363/any-way-to-tell-if-users-python-environment-is-anaconda
    """
    is_conda = os.path.exists(os.path.join(sys.prefix, 'conda-meta'))
    return is_conda


def is_poetry_available(system):
    """Test if *poetry* is available in the environment."""    
    myenv=os.environ.copy()
    if system:
        cmd=['which','poetry_']
    else:
        cmd=['which','poetry']
    result = subprocess.run(cmd,capture_output=True,env=myenv)
    return result.returncode==0


def is_bumpversion_available():
    """Test if *bumpversion* is available in the environment."""
    myenv=os.environ.copy()
    cmd=['which','bumpversion']
    result = subprocess.run(cmd,capture_output=True,env=myenv)
    return result.returncode==0


def get_dependencies():
    """
    """
    pyproject_toml = TomlFile('pyproject.toml')
    current_deps = pyproject_toml['tool']['poetry']['dependencies']
    return current_deps

# end of file