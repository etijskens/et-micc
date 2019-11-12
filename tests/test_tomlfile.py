#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for et_micc.tomlfile module."""

import shutil
from pathlib import Path

from et_micc.tomlfile import TomlFile


def test_exists():
    toml = TomlFile('pyproject.toml')
    assert toml.exists()
    

def test_read():
    toml = TomlFile('pyproject.toml')
    project_name = toml['tool']['poetry']['name']
    assert project_name=='et-micc'


def test_write():
    c = Path('copy.toml')
    if c.exists():
        c.unlink()
    shutil.copy('pyproject.toml', str(c))
    toml = TomlFile(c)
    toml['tool']['poetry']['name'] = 'copy'
    project_name = toml['tool']['poetry']['name']
    assert project_name=='copy'
    toml.save()

    toml = TomlFile(c)
    project_name = toml['tool']['poetry']['name']
    assert project_name=='copy'
    
    c.unlink()
    assert not c.exists()


# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (normally all tests are run with pytest)
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_write

    print(f"__main__ running {the_test_you_want_to_debug}")
    the_test_you_want_to_debug()
    print('-*# finished #*-')
# ==============================================================================
