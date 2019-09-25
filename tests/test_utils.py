#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for micc package.
"""
#===============================================================================

import os
import sys
from pathlib import Path

#===============================================================================
# import pytest
from click import echo
import pytest
import types

#===============================================================================
# Make sure that the current directory is the project directory.
# 'make test" and 'pytest' are generally run from the project directory.
# However, if we run/debug this file in eclipse, we end up in test
if os.getcwd().endswith('tests'):
    echo(f"Changing current working directory"
         f"\n  from '{os.getcwd()}'"
         f"\n  to   '{os.path.abspath(os.path.join(os.getcwd(),'..'))}'\n")
    os.chdir('..')
#===============================================================================    
# Make sure that we can import the module being tested. When running 
# 'make test" and 'pytest' in the project directory, the current working
# directory is not automatically added to sys.path.
if not ('.' in sys.path or os.getcwd() in sys.path):
    p = os.path.abspath('.')
    echo(f"Adding '{p}' to sys.path.\n")
    sys.path.insert(0, p)
echo(f"sys.path = \n{sys.path}".replace(',','\n,'))
#===============================================================================

from tests.helpers import report, in_empty_tmp_dir 
from micc import cli, commands
import micc.utils

    
#===============================================================================
# test scenario blocks
#===============================================================================
def run(runner,arguments,input_='short description'):
    """
    create a project 
    """
    result = runner.invoke( cli.main
                          , arguments
                          , input=input_
                          )
    report(result)


#===============================================================================
#   Tests
#===============================================================================


def test_module_to_package():
    with in_empty_tmp_dir():
        m = Path('m.py')
        m.touch()
        assert m.is_file()
        commands.module_to_package(m)
        p = Path('m')
        assert p.is_dir()
        assert (p / '__init__.py').is_file()
        

def test_cpp_module_exists():
    with in_empty_tmp_dir():
        p = Path('foo')
        assert not micc.utils.cpp_module_exists(p,'module')
        Path('foo/foo/cpp_module').mkdir(parents=True)
        Path('foo/foo/cpp_module/module.cpp').touch()
        assert micc.utils.cpp_module_exists(p,'module')
                

def test_f2py_module_exists():
    with in_empty_tmp_dir():
        p = Path('foo')
        assert not micc.utils.f2py_module_exists(p,'module')
        Path('foo/foo/f2py_module').mkdir(parents=True)
        Path('foo/foo/f2py_module/module.f90').touch()
        assert micc.utils.f2py_module_exists(p,'module')
                

def test_py_module_exists():
    with in_empty_tmp_dir():
        p = Path('foo')
        assert not micc.utils.py_module_exists(p,'module')
        Path('foo/foo/').mkdir(parents=True)
        Path('foo/foo/module.py').touch()
        assert micc.utils.py_module_exists(p,'module')
                

def test_py_package_exists():
    with in_empty_tmp_dir():
        p = Path('foo')
        assert not micc.utils.py_module_exists(p,'module')
        Path('foo/foo').mkdir(parents=True)
        Path('foo/foo/module.py').touch()
        assert micc.utils.py_module_exists(p,'module')
               

def test_log():
    
    with micc.utils.log():
        print('test_log without logfun')
        
    logfile = micc.utils.get_project_path('.') / 'micc.log'
    print(logfile.resolve())
    if logfile.exists():
        logfile.unlink()
    assert not logfile.exists()

    global_options = types.SimpleNamespace(verbosity=3,project_path=Path('.').resolve())
    micc_logger = micc.utils.get_micc_logger(global_options)
    with micc.utils.log(micc_logger.info):
        micc_logger.info('test_log with a logfun')
        micc_logger.debug(' . debug message')
    assert logfile.exists()
    logtext = logfile.read_text()
    print(logtext)
    assert "doing ...\n" in logtext
    assert "test_log with a logfun\n" in logtext
    assert "  . debug message\n" in logtext
    assert "doing ... done.\n" in logtext
    
    
def test_get_project_path():
    p = Path.home()
    with pytest.raises(RuntimeError):
        p = micc.utils.get_project_path(p)
    p = Path.cwd()
    p = micc.utils.get_project_path(p)
    assert p==(Path.home() / 'software/dev/workspace/micc')
    
    
# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (normally all tests are run with pytest)
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_log # test_scenario_1

    from utils import taskcm
    with taskcm(f"__main__ running {the_test_you_want_to_debug}",
               '-*# finished #*-', singleline=False, combine=False):
        the_test_you_want_to_debug()
# ==============================================================================
