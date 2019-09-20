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

#===============================================================================
# import pytest
from click import echo
from click.testing import CliRunner

from cookiecutter.main import logger
logfile = logging.FileHandler("log.txt")
logfile.setLevel(logging.DEBUG)
logger.addHandler(logfile)

# import toml
# from importlib import import_module
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

from micc import cli
import micc.commands
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
    
    
@contextlib.contextmanager
def in_empty_tmp_dir():
    """A context manager that creates a temporary folder and changes
    the current working directory to it for isolated filesystem tests.
    """
    cwd = os.getcwd()
    uu = uuid.uuid4()
    tmp = os.path.join(cwd,f'__{uu}')
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    os.makedirs(tmp)
    os.chdir(tmp)
    try:
        yield tmp
    finally:
        os.chdir(cwd)
        try:
            shutil.rmtree(tmp)
        except (OSError, IOError):
            pass

    
#===============================================================================
# test scenario blocks
#===============================================================================
def create(runner,arguments,input_='short description'):
    """
    create a project 
    """
    result = runner.invoke( cli.main
                          , arguments
                          , input=input_
                          )
    report(result)

#===============================================================================
# tests
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
        print(os.getcwd())
        create(runner, ['-vv', 'create','foo', '--allow-nesting'])
        assert micc.utils.is_project_directory('foo')
        assert not micc.utils.is_simple_project('foo')

    
# def test_micc_version():
#     """
#     test `` micc version`` 
#     """
#     runner = CliRunner()
#     project_name = 'foo'
#     output_dir = os.path.join(os.getcwd(),'tests','output')
#     input_ = f'{project_name}\ntest_cli()'
#     result = runner.invoke(cli.main, ['-v','-q','create','-o',output_dir], input=input_)
#     report(result)
#     project_dir = os.path.join(output_dir, project_name)
#     assert os.path.exists(project_dir.replace('-','_')) or os.path.exists(project_dir) 
#     pyproject_toml = toml.load(os.path.join(project_dir,'pyproject.toml'))
#     current_version = pyproject_toml['tool']['poetry']['version']
#     assert current_version == "0.0.0"
#     
#     path_to_pyproject_toml = os.path.join(project_dir,'pyproject.toml')
#     pyproject_toml = toml.load(path_to_pyproject_toml)
#     project_name    = pyproject_toml['tool']['poetry']['name']
#     current_version = pyproject_toml['tool']['poetry']['version']
#     print(project_name, current_version)
# 
#     micc.commands.micc_version(project_dir, rule='patch', global_options=SimpleNamespace(verbose=False, quiet=True))
# 
#     pyproject_toml = toml.load(path_to_pyproject_toml)
#     project_name    = pyproject_toml['tool']['poetry']['name']
#     current_version = pyproject_toml['tool']['poetry']['version']
#     print(project_name, current_version)
#     assert current_version=="0.0.1"
#     
#     # clean up the project if required
#     if clean_up:
#         echo(f"cleaning up {project_dir}")
#         rmtree(project_dir)
#     else:
#         echo(f"Project directory left: {project_dir}")
# 
# #===============================================================================
# def test_micc():
#     """
#     Test for creating a project skeleton and bump the version.
#     """
#     runner = CliRunner()
#     project_name = micc_test_project_uuid()
#     output_dir = os.path.join(os.getcwd(),'tests','output')
#     input_ = f'{project_name}\ntest_cli()'
#     result = runner.invoke(cli.main, ['-v','-q','create','-o',output_dir], input=input_)
#     report(result)
#     project_dir = os.path.join(output_dir, project_name)
#     assert os.path.exists(project_dir.replace('-','_')) or os.path.exists(project_dir) 
#     pyproject_toml = toml.load(os.path.join(project_dir,'pyproject.toml'))
#     current_version = pyproject_toml['tool']['poetry']['version']
#     assert current_version == "0.0.0"
#     
#     # clean up the project if required
#     if clean_up:
#         echo(f"cleaning up {project_dir}")
#         rmtree(project_dir)
#     else:
#         echo(f"Project directory left: {project_dir}")
#     
# #===============================================================================
# def test_micc_create_with_project_name():
#     """
#     Test for creating a project skeleton, with a project name provided on the 
#     command line and bump the version.
#     """
#     runner = CliRunner()
#     project_name = 'a-test-project'
#     output_dir = os.path.join(os.getcwd(),'tests','output')
#     input_ = 'test_cli_with_project_name()'
#     result = runner.invoke(cli.main, ['-v','-q','create',project_name,'-o',output_dir], input=input_)
#     report(result)
#     project_dir = os.path.join(output_dir, project_name)
#     assert os.path.exists(project_dir.replace('-','_')) or os.path.exists(project_dir) 
#     pyproject_toml = toml.load(os.path.join(project_dir,'pyproject.toml'))
#     current_version = pyproject_toml['tool']['poetry']['version']
#     print('current_version',current_version)
#     assert current_version == "0.0.0"
#     
#     # clean up the project if required
#     if clean_up:
#         echo(f"cleaning up {project_dir}")
#         rmtree(project_dir)
#     else:
#         echo(f"Project directory left: {project_dir}")
# 
# # ==============================================================================
# def test_micc_app():
#     """
#     Test ``micc app``
#     """
#     # First create a project
#     runner = CliRunner()
#     project_name = micc_test_project_uuid()
#     output_dir = os.path.join(os.getcwd(),'tests','output')
#     
#     input_ = f'{project_name}\ntest_micc_app()'
#     result = runner.invoke(cli.main, ['-v','-q','create','-o',output_dir], input=input_)
#     report(result)
#     
#     # Add an app
#     project_dir = os.path.join(output_dir, project_name)
#     with in_directory(project_dir):
#         input_ = 'my-app'
#         result = runner.invoke(cli.main, ['-q','app'], input=input_)
#         report(result)
#     
#     # clean up the project if required
#     if clean_up:
#         echo(f"cleaning up {project_dir}")
#         rmtree(project_dir)
#     else:
#         echo(f"Project directory left: {project_dir}")
# 
# # ==============================================================================
# def test_micc_module():
#     """
#     Test ``micc module``
#     """
#     # First create a project
#     runner = CliRunner()
#     project_name = micc_test_project_uuid()
#     output_dir = os.path.join(os.getcwd(),'tests','output')
#     input_ = f'{project_name}\ntest_micc_module()'
#     result = runner.invoke(cli.main, ['-v','-q','create','-o',output_dir], input=input_)
#     report(result)
#     
#     # Add an app
#     project_dir = os.path.join(output_dir, project_name)
#     with in_directory(project_dir):
#         input_ = 'my_module'
#         result = runner.invoke(cli.main, ['-q','module'], input=input_)
#         report(result)
#     
#     # clean up the project if required
#     if clean_up:
#         echo(f"cleaning up {project_dir}")
#         rmtree(project_dir)
#     else:
#         echo(f"Project directory left: {project_dir}")

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
