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
from click.testing import CliRunner

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

from tests.helpers import in_empty_tmp_dir,report
from micc import cli
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
