#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for micc.utils package.
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
    p = os.path.abspath('.')
    echo(f"Adding '{p}' to sys.path.\n")
    sys.path.insert(0, p)
echo(f"sys.path = \n{sys.path}".replace(',','\n,'))
#===============================================================================

from tests.helpers import report, in_empty_tmp_dir 
from micc import cli,commands
import micc.utils
import micc.logging

def test_log():
    with micc.logging.log():
        print('test_log without logfun')
        
    logfile = micc.utils.get_project_path('.') / 'micc.log'
    print(logfile.resolve())
    if logfile.exists():
        logfile.unlink()
    assert not logfile.exists()

    global_options = types.SimpleNamespace(verbosity=3
                                          ,project_path=Path('.').resolve()
                                          ,clear_log=False
                                          )
    micc_logger = micc.logging.get_micc_logger(global_options)

    with micc.logging.logtime():
        with micc.logging.log(micc_logger.info):
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
    the_test_you_want_to_debug = test_log # test_scenario_1

    print(f"__main__ running {the_test_you_want_to_debug}")
    the_test_you_want_to_debug()
    print('-*# finished #*-')
# ==============================================================================
