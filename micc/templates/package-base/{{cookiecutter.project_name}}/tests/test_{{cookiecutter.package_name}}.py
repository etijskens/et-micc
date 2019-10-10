#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for {{ cookiecutter.package_name }} package."""

import os
import sys
import pytest

import {{ cookiecutter.package_name }}

# Make sure that the current directory is the project directory.
# 'make test" and 'pytest' are generally run from the project directory.
# However, if we run/debug this file in eclipse, we end up in test
if os.getcwd().endswith('tests'):
    echo(f"Changing current working directory"
         f"\n  from '{os.getcwd()}'"
         f"\n  to   '{os.path.abspath(os.path.join(os.getcwd(),'..'))}'.\n")
    os.chdir('..')
# Make sure that we can import the module being tested. When running
# 'make test" and 'pytest' in the project directory, the current working
# directory is not automatically added to sys.path.
if not ('.' in sys.path or os.getcwd() in sys.path):
    echo(f"Adding '.' to sys.path.\n")
    sys.path.insert(0, '.')

def test_hello():
    """Test for {{ cookiecutter.package_name }}.hello()."""
    s = {{ cookiecutter.package_name }}.hello()
    assert s=="Hello world"

    s = {{ cookiecutter.package_name }}.hello('me')
    assert s=="Hello me"
    
    
# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (normally all tests are run with pytest)
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_hello

    print("__main__ running", the_test_you_want_to_debug)
    the_test_you_want_to_debug()
    print('-*# finished #*-')
    
# eof