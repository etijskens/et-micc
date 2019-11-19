#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for et_micc.utils module."""

from pathlib import Path 

import et_micc.utils
from tests.helpers import in_empty_tmp_dir


def test_constraint_to_version():
    constraint = "^1.2.3"
    expected = ['1','2','3']
    version = et_micc.utils.constraint_to_version(constraint)
    assert version == expected
    
def test_compare_constraints():
    c123 = "^1.2.3"
    c023 = "^0.2.3"
    c003 = "^0.0.3"
    result = et_micc.utils.compare_constraints(c003, c003)
    assert result==0
    result = et_micc.utils.compare_constraints(c003, c023)
    assert result==-1
    result = et_micc.utils.compare_constraints(c003, c123)
    assert result==-1

    result = et_micc.utils.compare_constraints(c023, c003)
    assert result==1
    result = et_micc.utils.compare_constraints(c023, c023)
    assert result==0
    result = et_micc.utils.compare_constraints(c023, c123)
    assert result==-1

    result = et_micc.utils.compare_constraints(c123, c003)
    assert result==1
    result = et_micc.utils.compare_constraints(c123, c023)
    assert result==1
    result = et_micc.utils.compare_constraints(c123, c123)
    assert result==0

    c023 = "^0.2"
    result = et_micc.utils.compare_constraints(c023, c003)
    assert result==1
    result = et_micc.utils.compare_constraints(c003, c023)
    assert result==-1
    result = et_micc.utils.compare_constraints(c023, c023)
    assert result==0
    result = et_micc.utils.compare_constraints(c023, c123)
    assert result==-1
    result = et_micc.utils.compare_constraints(c123, c023)
    assert result==1


def test_verify_project_name():
    assert not et_micc.utils.verify_project_name("1")
    assert not et_micc.utils.verify_project_name("1ab")
    assert et_micc.utils.verify_project_name("a")
    assert et_micc.utils.verify_project_name("a1")
    assert et_micc.utils.verify_project_name("a123b")
    assert et_micc.utils.verify_project_name("a_-123b")
    assert et_micc.utils.verify_project_name("A_-123B")
    assert not et_micc.utils.verify_project_name("A_-123.B")
    assert not et_micc.utils.verify_project_name("A._-123.B")
    assert not et_micc.utils.verify_project_name("A_-123 B")
    
def test_insert_in_file():
    with in_empty_tmp_dir():
        file = Path('test.txt')
        with file.open(mode='w') as f:
            for i in range(10):
                f.write(str(i) + '\n')
        ilines = ["insert 1","insert 2"]
        et_micc.utils.insert_in_file(file, ilines, before=True, startswith="5")
        with file.open() as f:
            lines = f.readlines()
            for l,line in enumerate(lines):
                print(line)
                if l==5:
                    assert line.startswith(ilines[0])
                if l==6:
                    assert line.startswith(ilines[1])

        file = Path('test.txt')
        with file.open(mode='w') as f:
            for i in range(10):
                f.write(str(i) + '\n')
        ilines = ["insert 1","insert 2"]
        et_micc.utils.insert_in_file(file, ilines, before=False, startswith=("5"))
        with file.open() as f:
            lines = f.readlines()
            for l,line in enumerate(lines):
                print(line)
                if l==6:
                    assert line.startswith(ilines[0])
                if l==7:
                    assert line.startswith(ilines[1])
# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (normally all tests are run with pytest)
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug =  test_insert_in_file

    print(f"__main__ running {the_test_you_want_to_debug}")
    the_test_you_want_to_debug()
    print('-*# finished #*-')
# ==============================================================================
