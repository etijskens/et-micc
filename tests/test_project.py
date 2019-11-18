#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `micc` package."""
from types import SimpleNamespace
from pathlib import Path

from et_micc.project import Project

def test_ctor():
    global_options = SimpleNamespace(project_path=Path.cwd())
    proj = Project(global_options)
    print(proj.pyproject_toml['tool']['poetry']['dependencies'])
    

# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (normally all tests are run with pytest)
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_ctor

    the_test_you_want_to_debug()
    print('-*# finished #*-')
# ==============================================================================
