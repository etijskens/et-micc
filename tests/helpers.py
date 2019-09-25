#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for micc package.
"""
#===============================================================================

import os
import shutil
import contextlib
import uuid
import traceback
from pathlib import Path


def report(result,assert_exit_code=True):
    """
    helper to show the ``result`` of CliRunner.invoke
    """
    print(result.output)
    if result.exception:
        if result.stderr_bytes:
            print(result.stderr)
        print('exit_code =',result.exit_code)
        print(result.exception)
        traceback.print_tb(result.exc_info[2])
        print(result.exc_info[2])
        
    if assert_exit_code:
        assert result.exit_code == 0
        
    return result


@contextlib.contextmanager
def in_empty_tmp_dir(cleanup=True):
    """A context manager that creates a temporary folder and changes
    the current working directory to it for isolated filesystem tests.
    
    :param bool cleanup: if True the temporary folder is removed on exit, 
        otherwise a message is printed.
    """
    cwd = Path.cwd()
    uu = uuid.uuid4()
    tmp = cwd / f'__{uu}'
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True, exist_ok=True)
    os.chdir(tmp)
    print("Switching cwd to", tmp)
    try:
        yield tmp
    finally:
        print("Switching cwd back to", cwd)
        os.chdir(cwd)
        if cleanup:
            try:
                shutil.rmtree(tmp)
            except (OSError, IOError):
                pass
        else:
            print(f"Leftover: {tmp}")
        
    
# ==============================================================================
# ==============================================================================
if __name__ == "__main__":
    pass

# eof #
