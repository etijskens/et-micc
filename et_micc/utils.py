# -*- coding: utf-8 -*-
"""
Created on 18 Nov 2019

@author: etijskens

Module et_micc.utils
====================

Utility functions for et_micc.
"""
import os
import re
import subprocess
import copy
from pathlib import Path
from contextlib import contextmanager

import semantic_version as sv

from et_micc.tomlfile import TomlFile
import et_micc.logger

from pypi_simple import PyPISimple


def operator_version(version_constraint_string):
    """Split version_constraint_string in operator and version.

    :returns: (str,semantic_version.Version)
    """
    for i in range(2):
        if version_constraint_string[i].isdigit():
            operator = version_constraint_string[:i]
            if not operator:
                operator = '=='
            version = sv.Version(version_constraint_string[i:])
            break
    else:
        operator = version_constraint_string[:2]
        version  = sv.Version(version_constraint_string[2:])
    return (operator,version)


def version_range(version_constraint_string):
    """Return interval [lower_bound,upper_bound[ as a tuple for a given version constraint.
    
    Note that the lower bound is inclusive, but the upper bound is exclusive.
    If one of the bounds is None, then it is unbound in that direction.
    """
    if version_constraint_string.startswith('^'):
        vc = version_constraint_string[1:]
        vn = sv.Version(vc).next_major()
        version_constraint_string = f">={vc},<{vn}"

    if ',' in version_constraint_string:
        constraints = version_constraint_string.split(',')
        bnds = (None, None)
        for constraint in constraints:
            b = version_range(constraint)
            bnds = intersect(bnds,b)
        return bnds
        
    operator,version = operator_version(version_constraint_string)
    if operator == '==':
        return (version, version.next_patch())
    elif operator == '>=':
        return (version, None)
    elif operator == '<=':
        return (None, version.next_patch())
    elif operator == '>':
        return (version.next_patch(),None)
    elif operator == '<':
        return (None,version)
    

def largest_lower_bound(l,r):
    # None is always smaller
    if l is None:
        return r
    if r is None:
        return l
    else:
        return r if l.__cmp__(r)==-1 else l

        
def smallest_upper_bound(l,r):
    # None is always larger
    if l is None:
        return r
    if r is None:
        return l
    else:
        return l if l.__cmp__(r)==-1 else r

        
def intersect(version_range_1, version_range_2):
    """Compute the intersection of two version ranges"""
    llb = largest_lower_bound (version_range_1[0],version_range_2[0])
    sub = smallest_upper_bound(version_range_1[1],version_range_2[1])
    return (llb,sub)


def validate_intersection(intersection):
    """Test if the intersection is not empty.
    :returns: bool
    """
    if None in intersection[0]:
        return True
    else:
        return intersection[0].__cmp__(intersection[1]) != 1


def most_recent(version_constraint_string1, version_constraint_string2):
    range1 = version_range(version_constraint_string1)
    range2 = version_range(version_constraint_string2)
    if (not range1[1] is None) and (not range2[0] is None) and sv.compare(range1[1],range2[0])==-1:
        return version_constraint(range2)
    elif (not range2[1] is None) and (not range1[0] is None) and sv.compare(range2[1],range1[0])==-1:
        return version_constraint(range1)
    raise ValueError(f"ERROR: {range1} and {range2} intersect.")


def version_constraint(version_range):
    """Convert a version_range to a version constraing string"""
    return f">={version_range[0]},<{version_range[1]}"


def convert_caret_specification(spec):
    """"""
    if spec.startswith('^'):
        v = spec[1:]
        vlower = sv.Version(v)
        vupper = vlower.next_major()
        new_spec = f">={vlower},<{vupper}"
        return new_spec 
    else:
        return spec

def replace_in_file(file_to_search, look_for, replace_with):
    """Replace the text :py:obj:`look_for` with :py:obj:`replace_with` in file :file:`file_to_search`"""
    path = Path(file_to_search)
    text = path.read_text()
    text = text.replace(look_for, replace_with)
    path.write_text(text)


def verify_project_name(project_name):
    """Project names must start with a char, and contain only chars, digits, underscores and dashes.
    
    :returns: bool
    """
    p = re.compile("\A[a-zA-Z][a-zA-Z0-9_-]*\Z")
    return bool( p.match(project_name) )
    
    
def pep8_module_name(name):
    """Convert a module name to a PEP8 compliant module name.
    
    * lowercase
    * whitespace -> underscore 
    * dash -> underscore 
    """
    if name[0].isnumeric():
        name = '_'+name
    
    valid_module_name = name.lower().replace('-', '_').replace(' ', '_')            
    
    return valid_module_name


def existsOnPyPI(package):
    """Does package exist already on PyPI?

    :return: True|False|Exception`

    In case of an exception, the result is inconclusive.
    """
    try:
        with PyPISimple() as client:
            requests_page = client.get_project_page(package)

    except Exception as e:
        return e

    return not requests_page is None

# 'pip search name' will soon disappear
# seehttps://stackoverflow.com/questions/65307988/error-using-pip-search-pip-search-stopped-working
# def is_publishable(package_name, verbose=True):
#     """Is the name <package_name> available for publishing on PyPI?
#
#     This is achieved by running ``pip search <package_name>`` and examining the output. If
#     <package_name> is in use, it will appear in the output.
#
#     :param str package_name: name of the package for which we want to verify the availability.
#     :param bool verbose: show the output of ``pip search <package_name>`` and the examination
#         process.
#
#     :returns: the answer as a bool, if the command ``pip search <package_name>`` was successful,
#         and None otherwise (e.g. because of no connection).
#     """
#
#     # We are using subprocess to run 'pip search' because if we use pip as a module
#     # the output cannot be suppressed in case of an error
#
#     cmd = ['pip', 'search', package_name]
#     if verbose:
#         print(
#             f"Verifying the availability of name '{package_name}' on PyPI.\n"
#             f"  Running: '{' '.join(cmd)}'"
#         )
#     try:
#         # python >=3.7
#         completed_process = subprocess.run(cmd, capture_output=True)
#     except:
#         # python <3.7, e.g 3.6.9:
#         #   capture_output parameter does not exist.
#         completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#
#     if completed_process.returncode:
#         if verbose:
#             print(completed_process.stderr.decode('utf-8'))
#             print(f"\nRunning: '{' '.join(cmd)}' FAILED!")
#         return None
#
#     if verbose:
#         print(f"  Examining the output of 'pip search {package_name}':")
#     lines = completed_process.stdout.decode('utf-8').split('\n')
#     for line in lines:
#         words = line.split(' ')
#         package = words[0]
#         if verbose:
#             print(f"    found '{package}' : {package_name==package}")
#         if package_name == package:
#             return False
#     return True


def is_project_directory(path,project=None):
    """Verify that the directory :file:`path` is a project directory. 
    
    :param Path path: path to a directory.
    :param Project project: if not None these variables are set:

        * project.project_name
        * project.package_name
        * project.pyproject_toml

    :returns: bool.
    
    As a sufficident condition, we request that 
    
    * there is a pyproject.toml file, exposing the project's name:py:obj:`['tool']['poetry']['name']`
    * that there is a python package or module with that name, converted by :py:meth:`pep8_module_name`.
    """
    if not isinstance(path, Path):
        path = Path(path)
        
    path_to_pyproject_toml = str(path /'pyproject.toml')
    
    try:
        pyproject_toml = TomlFile(path_to_pyproject_toml)
        project_name = pyproject_toml['tool']['poetry']['name']
        if not project is None:
            project.pyproject_toml = pyproject_toml
            project.project_name = project_name
    except Exception:
        return False

    return verify_project_structure(path,project)


def verify_project_structure(path,project=None):
    """Verify that there is either a Python module :file:`<package_name>.py`, or
    a package :file:`<package_name>/__init__.py` (and not both).
    
    :returns: a list with what was found. This list should have length 1. If its 
        length is 0, neither module.py, nor module/__init__.py were found. If its 
        length is 2, both were found.
    """
    package_name = pep8_module_name(path.name)
    
    module = path / (package_name + ".py")
    module = str(module.relative_to(path)) if module.exists() else ""

    package = path / package_name / "__init__.py"
    package = str(package.relative_to(path)) if package.exists() else ""
    
    if package and module:
        if project:
            project.error(f"Package ({package_name}/__init__.py) and module ({package_name}.py) found.")
        return False
    elif (not module and not package):
        if project:
            project.error(f"Neither package ({package_name}/__init__.py) nor module ({package_name}.py) found.")
        return False
    else:
        if project:
            project.structure = 'module' if module else 'package'
            project.src_file = module if module else package
            project.package_name = package_name
        return True

@contextmanager
def in_directory(path):
    """Context manager for changing the current working directory while the body of the
    context manager executes.
    """
    previous_dir = os.getcwd()
    os.chdir(str(path)) # the str method takes care of when path is a Path object
    yield os.getcwd()
    os.chdir(previous_dir)


def execute(cmds,logfun=None,stop_on_error=True,env=None,cwd=None):
    """Executes a list of OS commands, and logs with logfun.
    
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
        with et_micc.logger.log(logfun, f"> {' '.join(cmd)}"):
            try:
                # python >=3.7
                completed_process = subprocess.run(cmd, capture_output=True,env=env,cwd=cwd)
            except:
                # python <3.7, e.g 3.6.9:
                #   capture_output parameter does not exist.
                completed_process = subprocess.run(cmd, env=env, cwd=cwd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            if not logfun is None:
                if completed_process.returncode:
                    logfun0 = logfun
                    try:
                        logfun = logfun.__self__.warning
                    except:
                        pass
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


def insert_in_file(file, lines=[], before=False, startswith=None):
    """Insert *lines* at a specific position in a <file>.
    
    :param Path file: path to file in which to insert
    :param list lines: list of lines to insert. If a line does not end with 
        a newline, it is added.
    :param bool before: insert before or after a reference line.
    :param str startswith: find the reference line as the first line that
        starts with <startswith>. If no such line is found the text is inserted
        at the end.
    """
    if lines:
        with file.open() as f:
            content = f.readlines()
        for l,line in enumerate(content):
            if startswith and line.startswith(startswith):
                if not before:
                    l += 1
                break
        for i,line in enumerate(lines):
            if not line.endswith('\n'):
                line += '\n'
            content.insert(l+i,line)
        with file.open(mode='w') as f:
            for line in content:
                f.write(line)
        
    
#eof