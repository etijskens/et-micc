#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for et_micc package.
"""
#===============================================================================

import os,re
import shutil
import contextlib
import uuid
import traceback
from pathlib import Path

from et_micc.tomlfile import TomlFile

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
        if result.exit_code:
            raise AssertionError(f"result.exit_code = {result.exit_code}")
        
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
        

def get_version(path_to_file,verbose=False):
    version = '?'
    p = str(path_to_file)
    if p.endswith('.toml'):
        tomlfile = TomlFile(path_to_file)
        content = tomlfile.read()
        version = content['tool']['poetry']['version']
    else:
        if p.endswith('.py'):
            with open(str(p)) as f:
                lines = f.readlines() 
                ptrn = re.compile(r"__version__\s*=\s*['\"](.*)['\"]\s*")
                for line in lines:
                    mtch = ptrn.match(line)
                    if mtch:
                        version = mtch[1]
    if verbose:
        print(f"%% {path_to_file} : version : ({version})")
    return version

    
# ==============================================================================
# ==============================================================================
if __name__ == "__main__":
    pass

# eof #
