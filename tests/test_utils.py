#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for et_micc.utils module."""

from pathlib import Path 

import semantic_version as sv

import et_micc.utils
from tests.helpers import in_empty_tmp_dir


def test_version_range():
    vs = "1.2.3"
    vv = sv.Version(vs)
    vn = vv.next_patch()
    
    vc = f"=={vs}"
    bounds = et_micc.utils.version_range(vc)
    assert bounds[0] == vv
    assert bounds[1] == sv.Version("1.2.4")

    vc = f">={vs}"
    bounds = et_micc.utils.version_range(vc)
    assert bounds[0] == vv
    assert bounds[1] is None

    vc = f">{vs}"
    bounds = et_micc.utils.version_range(vc)
    assert bounds[0] == vn
    assert bounds[1] is None

    vc = f"<={vs}"
    bounds = et_micc.utils.version_range(vc)
    assert bounds[0] is None
    assert bounds[1] == vn

    vc = f"<{vs}"
    bounds = et_micc.utils.version_range(vc)
    assert bounds[0] is None
    assert bounds[1] == vv
    
    vc = f"^{vs}"
    vu = sv.Version("2.0.0")
    bounds = et_micc.utils.version_range(vc)
    assert bounds[0] == vv
    assert bounds[1] == vu


def test_convert_caret_specification():
    spec = ">=1.1.2"
    assert et_micc.utils.convert_caret_specification(spec) == spec
    spec = "^1.1.2"
    spec_new = et_micc.utils.convert_caret_specification(spec)
    assert spec_new == ">=1.1.2,<2.0.0"
    assert     sv.SimpleSpec("1.1.2").match(sv.Version("1.1.2"))
    assert not sv.Version("1.1.1") in sv.SimpleSpec(spec_new)
    assert     sv.Version("1.1.2") in sv.SimpleSpec(spec_new)
    assert     sv.Version("1.1.2") in sv.SimpleSpec(spec_new)
    assert     sv.Version("1.2.2") in sv.SimpleSpec(spec_new)
    assert not sv.Version("2.0.0") in sv.SimpleSpec(spec_new)
    assert not sv.Version("2.2.2") in sv.SimpleSpec(spec_new)


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
    the_test_you_want_to_debug = test_version_range

    print(f"__main__ running {the_test_you_want_to_debug}")
    the_test_you_want_to_debug()
    print('-*# finished #*-')
# ==============================================================================
