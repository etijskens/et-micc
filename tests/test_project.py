#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `micc` package."""
from types import SimpleNamespace
from pathlib import Path

from et_micc.project import Project

def test_ctor():
    options = SimpleNamespace(
        project_path=Path.cwd(),
        template_parameters={},
        verbosity=3,
        clear_log=False,
    )
    proj = Project(options)
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
