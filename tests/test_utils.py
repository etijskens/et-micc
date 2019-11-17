#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for et_micc.utils package.
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


from tests.helpers import report, in_empty_tmp_dir 
from et_micc import cli,commands
import et_micc.utils
import et_micc.logging_tools

#===============================================================================
#   Tests
#===============================================================================
def test_module_to_package():
    with in_empty_tmp_dir():
        et_micc.logging_tools.get_micc_logger(types.SimpleNamespace(verbosity=2
                                             ,project_path=Path.cwd()
                                             ,clear_log=False
                                             ))
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
        assert not et_micc.utils.cpp_module_exists(p,'module')
        Path('foo/foo/cpp_module').mkdir(parents=True)
        Path('foo/foo/cpp_module/module.cpp').touch()
        assert et_micc.utils.cpp_module_exists(p,'module')
                

def test_f2py_module_exists():
    with in_empty_tmp_dir():
        p = Path('foo')
        assert not et_micc.utils.f2py_module_exists(p,'module')
        Path('foo/foo/f2py_module').mkdir(parents=True)
        Path('foo/foo/f2py_module/module.f90').touch()
        assert et_micc.utils.f2py_module_exists(p,'module')
                

def test_py_module_exists():
    with in_empty_tmp_dir():
        p = Path('foo')
        assert not et_micc.utils.py_module_exists(p,'module')
        Path('foo/foo/').mkdir(parents=True)
        Path('foo/foo/module.py').touch()
        assert et_micc.utils.py_module_exists(p,'module')
                

def test_py_package_exists():
    with in_empty_tmp_dir():
        p = Path('foo')
        assert not et_micc.utils.py_module_exists(p,'module')
        Path('foo/foo').mkdir(parents=True)
        Path('foo/foo/module.py').touch()
        assert et_micc.utils.py_module_exists(p,'module')
               

def test_get_project_path():
    p = Path.home()
    with pytest.raises(RuntimeError):
        p = et_micc.utils.get_project_path(p)
    p = Path.cwd()
    p = et_micc.utils.get_project_path(p)
    assert p==(Path.home() / 'software/dev/workspace/et-micc')


def test_get_dependencies():
    deps = et_micc.utils.get_dependencies()
    print(deps)
    assert 'numpy' in deps

# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (normally all tests are run with pytest)
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_get_dependencies

    print(f"__main__ running {the_test_you_want_to_debug}")
    the_test_you_want_to_debug()
    print('-*# finished #*-')
# ==============================================================================
