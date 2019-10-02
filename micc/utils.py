# -*- coding: utf-8 -*-
"""
Utility functions for micc.py
"""
import os, sys, subprocess, logging, sysconfig, copy
from contextlib import contextmanager
import toml
from pathlib import Path


def get_extension_suffix():
    return sysconfig.get_config_var('EXT_SUFFIX')


def path_to_cmake_tools():
    """
    return the path to the folder with the CMake tools.
    """
    p = (Path(__file__) / '..' / 'cmake_tools').resolve()
    return str(p)


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
    os.chdir(str(path)) # the str method takes care of when path is a Path object
    yield os.getcwd()
    os.chdir(previous_dir)


def replace_version_in_file(filepath,current_version,new_version):
    """
    :param Path filepath: 
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
    """
    :param Path filepath: 
    """
    with filepath.open() as f:
        content_as_string = f.read()
    content_as_string = content_as_string.replace(old,new)
    with filepath.open(mode="w") as f:
        f.write(content_as_string)


def is_project_directory(path,raise_if=None):
    """
    Verify that the directory ``path`` is a project directory. 
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
        project_name = toml.load(path_to_pyproject_toml)['tool']['poetry']['name']
        rv = True
    except:
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


def get_name_version(project_path):
    """
    Read name and version of this project from the pyproject.toml file.
    """
    path_to_pyproject_toml = Path(project_path) / 'pyproject.toml'
    pyproject_toml = toml.load(str(path_to_pyproject_toml))
    return ( pyproject_toml['tool']['poetry']['name']
           , pyproject_toml['tool']['poetry']['version']
           )


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

def py_module_exists(project_path, module_name):
    """
    Test if there is already a python module with name ``module_name`` 
    in the project at ``project_path``.
        
    :param Path project_path: project path
    :param str module_name: module name
    :returns: bool
    """
    file = project_path / convert_to_valid_module_name(project_path.name) / f'{module_name}.py'
    return file.is_file()


def py_package_exists(project_path, module_name):
    """
    Test if there is already a python package with name ``module_name`` 
    in the project at ``project_path``.
        
    :param Path project_path: project path
    :param str module_name: module name
    :returns: bool
    """
    return (project_path / convert_to_valid_module_name(project_path.name) / module_name / '__init__.py').is_file()


def f2py_module_exists(project_path, module_name):
    """
    Test if there is already a f2py module with name ``module_name`` in this project.
        
    :param Path project_path: project path
    :param str module_name: module name
    :returns: bool
    """
    return (project_path / convert_to_valid_module_name(project_path.name) / ('f2py_' + module_name)/ f"{ module_name}.f90").is_file() 


def cpp_module_exists(project_path, module_name):
    """
    Test if there is already a cpp module with name ``module_name`` in this project.
        
    :param Path project_path: project path
    :param str module_name: module name
    :returns: bool
    """
    return (project_path / convert_to_valid_module_name(project_path.name) / ('cpp_' + module_name)/ f"{ module_name}.cpp").is_file() 


def module_exists(project_path, module_name):
    """
    Test if there is already a module with name ``module_name`` in this project.

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
    """
    Test if there is already an app with name ``app_name`` in this project.
    
        * ``<package_name>/cli_<app_name>.py``
        
    :param Path project_path: project path
    :param str app_name: app name
    :returns: bool
    """
    return (project_path / convert_to_valid_module_name(project_path.name) / f"cli_{app_name}.py").is_file()
    

def is_module_project(project_path, raise_if=None):
    """Find out if this project is a simple or general python project.
    
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
    """Find out if this project is a simple or general python project.
    
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
        x = RuntimeError(f"Directory '{project_path}' is NOT a package     project")
        x.path = project_path
    raise x


def execute(cmds,logfun=None,stop_on_error=True,env=None):
    """
    Executes a list of OS commands, and log with logfun.
    
    :param list cmds: list of OS commands (=list of list of str) or a single command (list of str)
    :parma callable logfun: a function to write output, typically 
        ``logging.getLogger('micc').debug``.
    :returns int: return code of first failing command, or 0 if all
        commanbds succeed.
    """
    if isinstance(cmds[0],str):
        # this is a single command
        cmds = [cmds]
        
    for cmd in cmds:
        with log(logfun, f"> {' '.join(cmd)}", end_msg=None):
            completed_process = subprocess.run(cmd, capture_output=True,env=env)
            if not logfun is None:
                if completed_process.stdout:
                    logfun(' (stdout)\n' + completed_process.stdout.decode('utf-8'))
                if completed_process.stderr:
                    logfun(' (stderr)\n' + completed_process.stderr.decode('utf-8'))
            if stop_on_error:
                if completed_process.returncode:
                    return completed_process.returncode
    return 0


def verbosity_to_loglevel(verbosity):
    """
    :param int verbosity:
    """
    if verbosity==0:
        return logging.CRITICAL
    elif verbosity==1:
        return logging.INFO
    else:
        return logging.DEBUG


def get_project_path(p):
    """
    :param Path p:
    :returns: the nearest directory above ``p`` that is project directory.
    """
    root = Path('/')
    p = Path(p).resolve()
    p0 = copy.copy(p)
    while not is_project_directory(p):
        p = p.parent
        if p==root:
            raise RuntimeError(f"Folder {p0} is not inside a Python project.")
    return p


def static_vars(**kwargs):
    """
    Add static variables to a method.
    """
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


# Use static vare to implement a singleton
@static_vars(the_logger=None)
def get_micc_logger(global_options): 
    """
    Set up and store a micc logger that writes to the console (taking verbosity 
    into account) and to a log file ``micc.log``.
    
    :param types.SimpleNamespace global_options: namespace object with options 
        accepted by (almost) all micc commands.
    :returns: a logging.Logger object.
    """
    
    if not get_micc_logger.the_logger is None:
        # verify that the current logger is for the current project directory
        # (When running pytest, micc commands are run in several different
        # project directories created on the fly. the micc_logger must adjust
        # to this situation and log to a micc.log file in the project directory.
        current_logfile = get_micc_logger.the_logger.logfile
        current_project_path = global_options.project_path
        if not current_logfile.parent == current_project_path:
            get_micc_logger.the_logger = None
            
    if get_micc_logger.the_logger is None:
        
        if global_options.clear_log:
            logfile = global_options.project_path / 'micc.log'
            if logfile.exists():
                logfile.unlink()
            else: 
                global_options.clear_log = False
                
        # create a new logger object that will write to micc.log 
        # in the current project directory
        p = global_options.project_path / 'micc.log'
        get_micc_logger.the_logger = create_logger(p)
        get_micc_logger.the_logger.logfile = p
        if global_options.verbosity>2:
            print(f"micc_logger.logfile = {get_micc_logger.the_logger.logfile}")

            
            
    # set the log level from the verbosity
    get_micc_logger.the_logger.console_handler.setLevel(verbosity_to_loglevel(global_options.verbosity))

    if global_options.clear_log:
        global_options.clear_log = False
        get_micc_logger.the_logger.debug("The log file was cleared.")

    
    return get_micc_logger.the_logger


def create_logger(filepath,filemode='a'):
    """
    create a logging.Logger object with a 
    
    * console handler
    * file handler, writing to file ``filename``
    """
    # create formatters and add it to the handlers
    format_string = '[%(levelname)s] %(message)s'
    console_formatter = logging.Formatter(format_string)
    logfile_formatter = logging.Formatter('\n%(asctime)s\n' + format_string)
    # create and add a console handler 
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(1)
    
    # create and add a logfile handler
    logfile_handler = logging.FileHandler(filepath,mode=filemode)
    logfile_handler.setFormatter(logfile_formatter) 
    logfile_handler.setLevel(logging.DEBUG)
            
    # create logger for micc
    logger = logging.getLogger(filepath.name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logfile_handler)
    logger.addHandler(console_handler)
    
    # add the handlers as a member, so we can still modify them on the fly.
    logger.logfile_handler = logfile_handler
    logger.console_handler = console_handler
    
    return logger


@contextmanager
def log(logfun=None, begin_msg='doing', end_msg='done.'):
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
    else:
        yield
        pass


def is_conda_python():
    """
    :returns: test if user's python environment is anaconda.
    
    see `https://stackoverflow.com/questions/21282363/any-way-to-tell-if-users-python-environment-is-anaconda`_
    """
    is_conda = os.path.exists(os.path.join(sys.prefix, 'conda-meta'))
    return is_conda

# end of file