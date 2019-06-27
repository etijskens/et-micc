# -*- coding: utf-8 -*-

"""
{{cookiecutter.app_name}} app
=================================

A console script

"""
#===============================================================================
import sys
import click
#===============================================================================
@click.command()
def main(args=None):
    """
    Console script {{cookiecutter.app_name}}.
    """
    click.echo("running {{cookiecutter.app_name}} ...")
    return 0
#===============================================================================
if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
#===============================================================================
