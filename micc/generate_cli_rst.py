# -*- coding: utf-8 -*-
"""
this is a python script that generates ``cli.rst``
"""

from click.testing import CliRunner

from micc import cli

if __name__=="__main__":
    runner = CliRunner()
    with open('cli.rst','w') as f:
        
        result = runner.invoke( cli.main, ['--help'] )
        f.write('\n')
        f.write(result.stdout.replace('main','micc'))
        
        micc_commands = ['create']
        for command in micc_commands:
            result = runner.invoke( cli.main, [command,'--help'] )
            f.write('\n')
            f.write(result.stdout.replace('main','micc'))
        
    print("done")