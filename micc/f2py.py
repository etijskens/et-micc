"""
Module f2py
===========
Wrapper for Numpy.f2py
"""

from pathlib import Path

import numpy.f2py

def build_f2py(module_name,args=[]):
    """
    :param Path path: to f90 source
    """
    src_file = module_name + '.f90'
    
    path_to_src_file = Path(src_file).resolve()
    if not path_to_src_file.exists():
        raise FileNotFoundError(str(path_to_src_file))
    
    f2py_args = ['--build-dir','_f2py_build']
    f2py_args .extend(args)
    
    with open(str(path_to_src_file.name)) as f:
        fsource = f.read() 
    returncode = numpy.f2py.compile(fsource, extension='.f90', modulename=module_name, extra_args=f2py_args, verbose=True)
    
    return returncode