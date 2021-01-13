#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for et_micc package.
"""
#===============================================================================

import os
import sys
from pathlib import Path
from types import SimpleNamespace

#===============================================================================
from click.testing import CliRunner

import et_micc.logger
from tests.helpers import in_empty_tmp_dir, report, get_version
from et_micc import cli_micc

#===============================================================================
# test scenario blocks
#===============================================================================
def run(runner, arguments, input_=None):
    """
    create a project 
    """
    result = runner.invoke( cli_micc.main
                          , arguments
                          , input=input_
                          )
    return report(result)


#===============================================================================
#   Tests
#===============================================================================
def test_micc_help():
    """
    Test ``et_micc --help``.
    """
    runner = CliRunner()
    result = run(runner,['--help'])
    report(result)
    assert '--help' in result.output
    assert 'Show this message and exit.' in result.output


def test_scenario_1():
    """
    """
    runner = CliRunner()
    with in_empty_tmp_dir():
        run(runner, ['-vv', '-p', 'FOO', 'create', '--allow-nesting'])
        assert Path('FOO/foo.py').exists()
        run(runner, ['-vvv', '-p', 'FOO', 'info'])
 
 
def test_scenario_2():
    """
    """
    runner = CliRunner()
    with in_empty_tmp_dir():
        run(runner, ['-vv', '-p', 'FOO', 'create', '-p', '--allow-nesting'])
        assert Path('FOO/foo/__init__.py').exists()
        run(runner, ['-vvv', '-p', 'FOO', 'info'])
        run(runner, ['-v', '-p', 'FOO', 'version'])
        run(runner, ['-v', '-p', 'FOO', 'version','--short'])
        run(runner, ['-vv', '-p', 'FOO', 'version','-M'])
        run(runner, ['-v', '-p', 'FOO', 'version','--short'])
        run(runner, ['-vv', '-p', 'FOO', 'version','-m'])
        run(runner, ['-v', '-p', 'FOO', 'version','--short'])
        run(runner, ['-vv', '-p', 'FOO', 'version','-p'])
        run(runner, ['-v', '-p', 'FOO', 'version','--short'])
        
 
# def test_scenario_1b():
#     """
#     """
#     runner = CliRunner()
# #     with runner.isolated_filesystem():
#     with in_empty_tmp_dir():
#         oops = Path('oops')
#         oops.touch()
#         with pytest.raises(AssertionError):
#             run(runner, ['-vv', 'create', '--allow-nesting'] )
#         l = os.listdir()
#         assert len(l)==1
#         
#         
# def test_scenario_2():
#     """
#     """
#     runner = CliRunner()
# #     with runner.isolated_filesystem():
#     with in_empty_tmp_dir():
#         run(runner, ['-p','foo','-vv', 'create', '--allow-nesting'])
#         foo = Path('foo')
#         et_micc.utils.is_project_directory(foo,raise_if=False)
#         et_micc.utils.is_module_project   (foo,raise_if=False)
#         et_micc.utils.is_package_project  (foo,raise_if=True)
#         expected = '0.0.0'
#         assert get_version(foo / 'pyproject.toml')==expected
#         assert get_version(foo / 'foo.py')==expected
#         
#         run(runner, ['-p','foo','-vv', 'convert-to-package','--overwrite'])
#         et_micc.utils.is_module_project   (foo,raise_if=True)
#         et_micc.utils.is_package_project  (foo,raise_if=False)
# 
#         run(runner, ['-vv','-p','foo','version'])
#         assert get_version(foo / 'pyproject.toml')==expected
#         assert get_version(foo / 'foo' / '__init__.py')==expected
# 
#         run(runner, ['-p','foo','version', 'patch'])
#         expected = '0.0.1'
#         assert get_version(foo / 'pyproject.toml')==expected
#         assert get_version(foo / 'foo' / '__init__.py')==expected
#         
#         run(runner, ['-p','foo','version', 'minor'])
#         expected = '0.1.0'
#         assert get_version(foo / 'pyproject.toml')==expected
#         assert get_version(foo / 'foo' / '__init__.py')==expected
# 
#         run(runner, ['-p','foo','version', 'major'])
#         expected = '1.0.0'
#         assert get_version(foo / 'pyproject.toml')==expected
#         assert get_version(foo / 'foo' / '__init__.py')==expected
# 
#         run(runner, ['-p','foo','version', 'major'])
#         expected = '2.0.0'
#         assert get_version(foo / 'pyproject.toml')==expected
#         assert get_version(foo / 'foo' / '__init__.py')==expected
#         
#         result = run(runner, ['-p','foo','version', '-s'])
#         assert expected in result.stdout
#         
#         run(runner, ['-p','foo','-vv', 'add', '--app', 'my_app'])
#         assert Path('foo/foo/cli_my_app.py').exists()
#         
#         run(runner, ['-p','foo','-vv', 'add', 'mod1', '--py'])
#         assert Path('foo/foo/mod1.py').exists()
#         
#         run(runner, ['-p','foo','-vv', 'add', 'mod2', '--py', '--package'])
#         assert Path('foo/foo/mod2/__init__.py').exists()
# 
#         run(runner, ['-p','foo','-vv', 'add', 'mod3', '--f2py'])
#         assert Path('foo/foo/f2py_mod3/mod3.f90').exists()
#         print("f2py ok")
# 
#         run(runner, ['-p','foo','-vv', 'add', 'mod4', '--cpp'])
#         assert Path('foo/foo/cpp_mod4/mod4.cpp').exists()
#         print("cpp ok")
#         
#         extension_suffix = et_micc.utils.get_extension_suffix()
#         run(runner, ['-p','foo','build'])
#         assert Path('foo/foo/mod3'+extension_suffix).exists()
#         assert Path('foo/foo/mod4'+extension_suffix).exists()
#         
#         run(runner, ['-p','foo','docs','--html','-l'])
#         assert Path('foo/docs/_build/html/index.html').exists()
#         assert Path('foo/docs/_build/latex/foo.pdf').exists()
#         print('make docs ok')
#         
#         run(runner, ['-p','foo','-vv','info'])
# 
# 
# def _test_add_dependency():
#     """
#     the outcome of this depends on whether we are online or not
#     this is mainly for debugging
#     """
#     runner = CliRunner()
#     with in_empty_tmp_dir():
#         run(runner, ['-vv', '-p', 'FOO', 'create', '--allow-nesting'])
#         assert Path('FOO/foo.py').exists()
#         with et_micc.utils.in_directory('FOO'):
#             et_micc.commands.add_dependencies(['numpy'],SimpleNamespace(verbosity=0))


# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (normally all tests are run with pytest)
# ==============================================================================
if __name__ == "__main__":
    print(sys.version_info)
    the_test_you_want_to_debug = test_scenario_2

    with et_micc.logging_.log(print,f"__main__ running {the_test_you_want_to_debug}",'-*# finished #*-'):
        the_test_you_want_to_debug()
# ==============================================================================
