#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for micc package.
"""
#===============================================================================

import os
import sys
import shutil
import logging
import contextlib
import uuid
import traceback
from pathlib import Path

#===============================================================================
# import pytest
from click import echo
from click.testing import CliRunner
import pytest

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

from micc import cli, commands
import micc.utils
#===============================================================================
def report(result,assert_exit_code=True):
    """
    helper to show the result of CliRunner.invoke
    """
    print(result.output)
    if result.exception:
        if result.stderr_bytes:
            print(result.stderr)
        print('exit_code =',result.exit_code)
        print(result.exception)
        traceback.print_tb(result.exc_info[2])
        print(result.exc_info[2])
        
    if assert_exit_code:
        assert result.exit_code == 0


cleanup_empty_dir = False # use this if you want to check the contents of the directory after the run
cleanup_empty_dir = True
    
@contextlib.contextmanager
def in_empty_tmp_dir():
    """A context manager that creates a temporary folder and changes
    the current working directory to it for isolated filesystem tests.
    """
    cwd = Path.cwd()
    uu = uuid.uuid4()
    tmp = cwd / f'__{uu}'
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True, exist_ok=True)
    os.chdir(tmp)
    print("Switching cwd to", tmp)
    try:
        yield tmp
    finally:
        print("Switching cwd back to", cwd)
        os.chdir(cwd)
        if cleanup_empty_dir:
            try:
                shutil.rmtree(tmp)
            except (OSError, IOError):
                pass
        else:
            print(f"Leftover: {tmp}")
    
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
def test_micc_help():
    """
    Test ``micc --help``.
    """
    runner = CliRunner()
    result = runner.invoke(cli.main, ['--help'])
    report(result)
    assert '--help' in result.output
    assert 'Show this message and exit.' in result.output


def test_scenario_1():
    """
    """
    runner = CliRunner()
#     with runner.isolated_filesystem():
    with in_empty_tmp_dir():
        run(runner, ['-p','foo','-vv', 'create', '--allow-nesting'])
        foo = Path('foo')
        assert micc.utils.is_project_directory(foo)
        assert not micc.utils.is_module_project(foo)
        assert     micc.utils.is_package_project(foo)
        
        run(runner, ['-p','foo','-vv', 'app','my_app'])
        assert Path('foo/foo/cli_my_app.py').exists()
        
        run(runner, ['-p','foo','-vv', 'module','mod1','--structure','module'])
        assert Path('foo/foo/mod1.py').exists()
        
        run(runner, ['-p','foo','-vv', 'module','mod2','--structure','package'])
        assert Path('foo/foo/mod2/__init__.py').exists()

        run(runner, ['-p','foo','-vv', 'module','mod3','--f2py'])
        assert Path('foo/foo/f2py_mod3/mod3.f90').exists()
        print("f2py ok")

        run(runner, ['-p','foo','-vv', 'module','mod4','--cpp'])
        assert Path('foo/foo/cpp_mod4/mod4.cpp').exists()
        print("cpp ok")
        
        extension_suffix = micc.utils.get_extension_suffix()
        run(runner, ['-p','foo','build'])
        assert Path('foo/foo/mod3'+extension_suffix).exists()
        assert Path('foo/foo/mod4'+extension_suffix).exists()
        
        run(runner, ['-p','foo','docs','--html','-l'])
        assert Path('foo/docs/_build/html/index.html').exists()
        assert Path('foo/docs/_build/latex/foo.pdf').exists()
        print('make docs ok')
        
        micc.utils.delete_micc_logger()

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
    
#     with micc.utils.log():
#         print('test_log without logfun')
    logfile = micc.utils.get_project_path() / 'micc.log'
    print(logfile.resolve())
    if logfile.exists():
        logfile.unlink()
    assert not logfile.exists()
    micc_logger = micc.utils.get_micc_logger(3)
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
    the_test_you_want_to_debug = test_scenario_1

    from utils import taskcm
    with taskcm(f"__main__ running {the_test_you_want_to_debug}",
               '-*# finished #*-', singleline=False, combine=False):
        the_test_you_want_to_debug()
# ==============================================================================
