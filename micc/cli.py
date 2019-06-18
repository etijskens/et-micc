# -*- coding: utf-8 -*-

"""
Console script for micc
=======================

Create a cookiecutter project from a micc file. Micc files are .json files
representing a dict. Keys are *str* objects representing cookiecutter template
arguments. The values are dicts of ``click.prompt()`` keyword arguments.
"""
import sys
import click

from .micc import micc

@click.command()
@click.argument('cookiecutter'
               , default='micc-module'
               )
@click.option('-m', '--micc-file'
             , default='micc.json'
             )
@click.option('-v', '--verbose'
             , is_flag=True
             , default=False
             )
def main(cookiecutter, micc_file, verbose):
    """
    Console script for micc. Prompts the user for all entries in the micc.json file
    that do not have a default.

    :param str cookiecutter: path to the cookiecutter template.  
    """
    return micc(cookiecutter, micc_file, verbose)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
