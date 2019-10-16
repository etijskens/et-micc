# -*- coding: utf-8 -*-
"""
Command line interface {{ cookiecutter.app_name }}.
"""

import sys
from types import SimpleNamespace

import click


@click.group()
@click.option('-v', '--verbosity', count=True
             , help="The verbosity of the program output."
             , default=1
             )
@click.pass_context
def main(ctx, verbosity):
    """Command line interface {{ cookiecutter.app_name }}.
    
    A 'hello' world CLI example.
    """
    # store global options in ctx.obj
    ctx.obj = SimpleNamespace(verbosity=verbosity)

    click.echo(f"running {{ cookiecutter.app_name }}")


@main.command()
@click.argument('who', default='world')
@click.option('-u', '--uppercase'
             , help="Print 'Hello world' in uppercase."
             , default=False, is_flag=True
             )
@click.pass_context
def hello(ctx, who, uppercase):
    """Subcommand hello.
    
    :param str who: whom to say hello to.
    """
    msg = "Hello " + who
    if uppercase:
        msg = msg.upper()
    for i in range(ctx.obj.verbosity):
        print(i,msg)

    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
#eodf
