# -*- coding: utf-8 -*-

"""
Module et_micc.project 
======================

An OO interface to et-micc_ projects

"""
import os
import json 
from pathlib import Path
from click import secho 

from et_micc.tomlfile import TomlFile
from et_micc.utils import is_project_directory, pep8_module_name
import et_micc.expand
import et_micc.logging


class Project:
    """
    An OO interface to et-micc_ projects.
    """
    def __init__(self,options):
        self.rc = 0
        self.options = options
        project_path = options.project_path
        
        template_parameters_json = project_path / 'micc.json'
        if template_parameters_json.exists():
            options.template_parameters.update(
                et_micc.expand.get_template_parameters(template_parameters_json)
            )
        else:
            options.template_parameters.update(
                et_micc.expand.get_template_parameters(
                    et_micc.expand.get_preferences(Path('.'))
                )
            )
        
        try:
            self.pyproject_toml = TomlFile(project_path / 'pyproject.toml')
        except FileNotFoundError:
            # either the project_directory or the pyproject.toms file does not exist
            if options.create:
                if project_path.exists() and os.listdir(str(project_path)):
                    # do not log here, because project is not created yet.
                    self.error(f"Cannot create project in ({project_path}):\n"
                               f"  Directory must be empty."
                              )
                else:
                    self._create()
            else:
                self.error(f"Not a project directory:\n  {project_path}")
                
            
    def error(self, msg):
        secho("[ERROR]\n" + msg, fg='bright_red')
        self.rc = 1

    
    
    def _create(self):
        """
        """
        project_path = self.options.project_path
        project_path.mkdir(parents=True,exist_ok=True)

        et_micc.logging.get_micc_logger(self.options)
        
        if not self.options.allow_nesting:
            # Prevent the creation of a project inside another project    
            p = project_path.parent.resolve()
            while not p.samefile('/'):
                if is_project_directory(p):
                    self.error(f"Cannot create project in ({project_path}):\n"
                               f"  Specify '--allow-nesting' to create a et_micc project inside another et_micc project ({p})."
                              )
                    return 1
                p = p.parent
        
        project_name  = project_path.name
        package_name = pep8_module_name(project_name)
        try:
            relative_project_path = project_path.relative_to(Path.cwd())
        except ValueError:
            # project_path was specified relative to cwd using ../
            # use full path instead.
            relative_project_path = project_path
            
        if self.options.structure=='module':
            structure = f"({relative_project_path}{os.sep}{package_name}.py)"
        elif self.options.structure=='package':
            structure = f"({relative_project_path}{os.sep}{package_name}{os.sep}__init__.py)"
        else:
            structure = ''
        
        self.options.verbosity = max(1,self.options.verbosity)
        micc_logger = et_micc.logging.get_micc_logger(self.options)
        with et_micc.logging.logtime():
            with et_micc.logging.log( micc_logger.info
                          , f"Creating project ({project_name}):"
                          ):
                micc_logger.info(f"Python {self.options.structure} ({package_name}): structure = {structure}")
                template_parameters = { 'project_name' : project_name
                                      , 'package_name' : package_name
                                      }
                template_parameters.update(self.options.template_parameters)
                self.options.template_parameters = template_parameters
                self.options.overwrite = False
             
                exit_code = et_micc.expand.expand_templates(self.options)                
                if exit_code:
                    micc_logger.critical(f"Exiting ({exit_code}) ...")
                    return exit_code
                
                my_micc_file = project_path / 'micc.json'
                with my_micc_file.open('w') as f:
                    json.dump(template_parameters,f)
                    micc_logger.debug(f" . Wrote project template parameters to {my_micc_file}.")
            
                with et_micc.logging.log(micc_logger.info,"Creating git repository"):
                    with et_micc.utils.in_directory(project_path):
                        cmds = [ ['git', 'init']
                               , ['git', 'add', '*']
                               , ['git', 'add', '.gitignore']
                               , ['git', 'commit', '-m', '"first commit"']
                               ]
                        if template_parameters['github_username']:
                            cmds.extend(
                               [ ['git', 'remote', 'add', 'origin', f"https://github.com/{template_parameters['github_username']}/{project_name}"]
                               , ['git', 'push', '-u', 'origin', 'master']
                               ]
                            )
                        et_micc.utils.execute(cmds, micc_logger.debug, stop_on_error=False)
        
        return 0
        
