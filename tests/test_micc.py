#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for micc package.
"""
#===============================================================================

import os
import sys
from shutil import rmtree
import uuid
#===============================================================================
# import pytest
from click import echo
from click.testing import CliRunner
import toml
from importlib import import_module
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
    echo(f"Adding '.' to sys.path.\n")
    sys.path.insert(0, '.')
#===============================================================================
clean_up = False
"""remove projects created during testing"""
#===============================================================================    
# from micc import micc
from micc import cli
#===============================================================================
def get_project_name():
    """
    create a unique name for a test project.
    """
    project_name = 'micc-test-project-' + str(uuid.uuid1())
    return project_name


# @pytest.fixture
# def response():
#     """
#     Sample pytest fixture.
# 
#     See more at: http://doc.pytest.org/en/latest/fixture.html
#     """
#     # import requests
#     # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')
# 
# 
# def test_content(response):
#     """Sample pytest test function with the pytest fixture as an argument."""
#     # from bs4 import BeautifulSoup
#     # assert 'GitHub' in BeautifulSoup(response.content).title.string


# def test_cli_no_micc_file():
#     """Test the CLI."""
#     runner = CliRunner()
#     with pytest.raises(FileNotFoundError):
#         try:
#             runner.invoke(cli.main, [''], catch_exceptions=False)
#         except FileNotFoundError as x:
#             echo(x, err=True)
#             raise


# def test_cli_no_cookiecutter_template():
#     """Test the CLI."""
#     runner = CliRunner()
#     with pytest.raises(FileNotFoundError):
#         try:
#             runner.invoke(cli.main, ['-c', './cookiecutter-oops'], catch_exceptions=False)
#         except FileNotFoundError as x:
#             echo(x, err=True)
#             raise

#===============================================================================
def test_cli():
    """Test the CLI."""
    runner = CliRunner()
    project_name = get_project_name()
    output_dir = os.path.join(os.getcwd(),'tests','output')
    input_ = f'{project_name}\ntest_cli()'
    result = runner.invoke(cli.cli, ['create','-v','-o',output_dir], input=input_)
    assert result.exit_code == 0
    print(result.output)
    project_dir = os.path.join(output_dir, project_name)
    assert os.path.exists(project_dir.replace('-','_')) or os.path.exists(project_dir) 
    pyproject_toml = toml.load(os.path.join(project_dir,'pyproject.toml'))
    current_version = pyproject_toml['tool']['poetry']['version']
    assert current_version == "0.0.0"
    print('current_version',current_version)

    result = runner.invoke(cli.cli, ['version', project_dir, '--patch'])
    print(result.output)
    assert result.exit_code == 0
    pyproject_toml = toml.load(os.path.join(project_dir,'pyproject.toml'))
    current_version = pyproject_toml['tool']['poetry']['version']
    print('current_version',current_version)
    assert current_version == "0.0.1"    
    
    # clean up the project if required
    if clean_up:
        echo(f"cleaning up {project_dir}")
        rmtree(project_dir)
    else:
        echo(f"Project directory left: {project_dir}")
    
#===============================================================================
def test_cli_with_project_name():
    """Test the CLI."""
    runner = CliRunner()
    project_name = 'a-test-project'
    output_dir = os.path.join(os.getcwd(),'tests','output')
    input_ = 'test_cli_with_project_name()'
    result = runner.invoke(cli.cli, ['create',project_name,'-v','-o',output_dir], input=input_)
    print(result.output)
    assert result.exit_code == 0
    project_dir = os.path.join(output_dir, project_name)
    assert os.path.exists(project_dir.replace('-','_')) or os.path.exists(project_dir) 
    pyproject_toml = toml.load(os.path.join(project_dir,'pyproject.toml'))
    current_version = pyproject_toml['tool']['poetry']['version']
    print('current_version',current_version)
    assert current_version == "0.0.0"

    result = runner.invoke(cli.cli, ['version', project_dir, '--minor'])
    print(result.output)
    assert result.exit_code == 0
    pyproject_toml = toml.load(os.path.join(project_dir,'pyproject.toml'))
    current_version = pyproject_toml['tool']['poetry']['version']
    print('current_version',current_version)
    assert current_version == "0.1.0"

    # verify that the project exports the new version    
    sys.path.insert(0, project_dir)
    package = import_module(project_name.replace(' ','_').replace('-','_'))
    assert package.__version__=="0.1.0"
    
    # clean up the project if required
    if clean_up:
        echo(f"cleaning up {project_dir}")
        rmtree(project_dir)
    else:
        echo(f"Project directory left: {project_dir}")
    
#===============================================================================
def test_cli_help():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['--help'])
    assert result.exit_code == 0
    assert '--help' in result.output
    assert 'Show this message and exit.' in result.output
    print(result.output)

# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (normally all tests are run with pytest)
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_cli_with_project_name

    from execution_trace import trace
    with trace(f"__main__ running {the_test_you_want_to_debug}",
               '-*# finished #*-', singleline=False, combine=False):
        the_test_you_want_to_debug()
# ==============================================================================
