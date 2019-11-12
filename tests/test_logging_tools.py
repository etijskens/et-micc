#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for et_micc package."""

from pathlib import Path
import types

import et_micc.utils
import et_micc.logging_tools

def test_log():
    with et_micc.logging_tools.log():
        print('test_log without logfun')
        
    logfile = et_micc.utils.get_project_path('.') / 'et_micc.log'
    print(logfile.resolve())
    if logfile.exists():
        logfile.unlink()
    assert not logfile.exists()

    global_options = types.SimpleNamespace(verbosity=3
                                          ,project_path=Path('.').resolve()
                                          ,clear_log=False
                                          )
    micc_logger = et_micc.logging_tools.get_micc_logger(global_options)

    with et_micc.logging_tools.logtime():
        with et_micc.logging_tools.log(micc_logger.info):
            micc_logger.info('test_log with a logfun')
            micc_logger.debug('debug message\nwith 2 lines')

    assert logfile.exists()
    logtext = logfile.read_text()
    print(logtext)
    assert "doing" in logtext
    assert "test_log with a logfun\n" in logtext
    assert "debug message" in logtext
    assert "done." in logtext
    

# ==============================================================================
# The code below is for debugging a particular test in eclipse/pydev.
# (normally all tests are run with pytest)
# ==============================================================================
if __name__ == "__main__":
    the_test_you_want_to_debug = test_log

    print(f"__main__ running {the_test_you_want_to_debug}")
    the_test_you_want_to_debug()
    print('-*# finished #*-')
# ==============================================================================
