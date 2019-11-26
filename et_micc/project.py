 # -*- coding: utf-8 -*-

"""
Module et_micc.project 
======================

An OO interface to et-micc_ projects

"""
import os
import shutil
import json 
from pathlib import Path
import subprocess
from operator import xor

import click 
import semantic_version

from et_micc.tomlfile import TomlFile
import et_micc.utils
import et_micc.expand
import et_micc.logging
from et_micc import __version__

CURRENT_ET_MICC_BUILD_VERSION = __version__


def micc_version():
    return __version__
    
    
class Project:
    """
    An OO interface to et-micc_ projects.
    """
    def __init__(self,options):
        self.exit_code = 0
        self.options = options
        project_path = options.project_path
        
        if hasattr(options, 'template_parameters'):
            # only needed for expanding templates.
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
        
        if et_micc.utils.is_project_directory(project_path,self):
            # existing project
            self.micc_logger = et_micc.logging.get_micc_logger(self.options)
            self.version = self.pyproject_toml['tool']['poetry']['version']
        else:
            # not a project directory or not a directory at all
            if options.create:
                if project_path.exists() and os.listdir(str(project_path)):
                    self.error(f"Cannot create project in ({project_path}):\n"
                               f"  Directory must be empty."
                              )
                else:
                    self.create()
            else:
                # all other micc commands require a project directory.
                self.error(f"Not a project directory ({project_path}).")
                
            
    def error(self, msg):
        click.secho("[ERROR]\n" + msg, fg='bright_red')
        self.exit_code = 1

    
    def warning(self, msg):
        click.secho("[WARNING]\n" + msg, fg='green')
        
    
    def create(self):
        """
        """
        project_path = self.options.project_path
        project_path.mkdir(parents=True,exist_ok=True)

        
        if not self.options.allow_nesting:
            # Prevent the creation of a project inside another project    
            p = project_path.parent.resolve()
            while not p.samefile('/'):
                if et_micc.utils.is_project_directory(p):
                    self.error(f"Cannot create project in ({project_path}):\n"
                               f"  Specify '--allow-nesting' to create a et_micc project inside another et_micc project ({p})."
                              )
                    return
                p = p.parent
        

        project_name = project_path.name
        if not et_micc.utils.verify_project_name(project_name):
            self.error(f"Invalid project name ({project_name}):\n"
                       f"  project name must start with char, and contain only chars, digits, hyphens and underscores."
                      )
            return
            
        package_name = et_micc.utils.pep8_module_name(project_name)
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
        self.micc_logger = et_micc.logging.get_micc_logger(self.options)
        with et_micc.logging.logtime():
            with et_micc.logging.log( self.micc_logger.info
                          , f"Creating project ({project_name}):"
                          ):
                self.micc_logger.info(f"Python {self.options.structure} ({package_name}): structure = {structure}")
                template_parameters = { 'project_name' : project_name
                                      , 'package_name' : package_name
                                      }
                template_parameters.update(self.options.template_parameters)
                self.options.template_parameters = template_parameters
                self.options.overwrite = False
             
                self.exit_code = et_micc.expand.expand_templates(self.options)                
                if self.exit_code:
                    self.micc_logger.critical(f"Exiting ({self.exit_code}) ...")
                    return
                
                my_micc_file = project_path / 'micc.json'
                with my_micc_file.open('w') as f:
                    json.dump(template_parameters,f)
                    self.micc_logger.debug(f" . Wrote project template parameters to {my_micc_file}.")
            
                with et_micc.logging.log(self.micc_logger.info,"Creating git repository"):
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
                        et_micc.utils.execute(cmds, self.micc_logger.debug, stop_on_error=False)
                

    def module_to_package_cmd(self):
        """
        """
        if self.package:
            self.warning(f"Project ({self.project_name}) is already a package ({self.package}).")
            return
        
        self.micc_logger.info(
            f"Converting Python module project {self.project_name} to Python package project."
        )

        # add documentation files for general Python project    
        self.options.templates = "package-general-docs"
        self.options.template_parameters.update(
            {'project_short_description' : self.pyproject_toml['tool']['poetry']['description']}
        )
        self.exit_code = et_micc.expand.expand_templates(self.options)
        if self.exit_code:
            self.micc_logger.critical(
                f"Expand failed during Project.module_to_package_cmd for project ({self.project_name})."
            )
            return
        
        # move <package_name>.py to <package_name>/__init__.py 
        package_path = self.options.project_path / self.package_name
        package_path.mkdir(exist_ok=True)
        src = self.options.project_path / (self.package_name + '.py')
        dst = self.options.project_path / self.package_name / '__init__.py'
        shutil.move(src, dst)
        
                
    def info_cmd(self):
        """Output info on the project.
        
        :param types.SimpleNamespace self.options: namespace object with options 
            accepted by (almost) all et_micc commands. Relevant attributes are 
            
            * **verbosity**: If **verbosity** is 0, outputs the project name,
              the project location, the package name and the version number. 
              If **verbosity** is 1, lists also the structure and the applications
              and submodules it contains. If **verbosity** is 2, lists also the
              detailed structure of the package.
            * **project_path**: Path to the project on which the command operates..
        """
        
        if self.options.verbosity>=0:
            self.options.verbosity = 10
    
        if self.options.verbosity>=1:
            click.echo("Project " + click.style(str(self.project_name), fg='green') 
                                  + " located at " 
                                  + click.style(str(self.options.project_path), fg='green')
                      + "\n  package: " + click.style(str(self.package_name), fg='green')
                      + "\n  version: " + click.style(self.version, fg='green')
                      )
                      
        if self.options.verbosity>=2:
            if self.module :
                kind = " (Python module)" 
                source = str(self.module)
            else:
                kind = " (Python package)"
                source = str(self.package)
            click.echo("  structure: " + click.style(source, fg='green') + kind)

        if self.options.verbosity>=3 and self.package:
            package_path = self.options.project_path / self.package_name
            files = []
            files.extend(package_path.glob('**/*.py'))
            files.extend(package_path.glob('**/cpp_*/'))
            files.extend(package_path.glob('**/f2py_*'))
            if len(files)>1: #__init__.py is always there.
                click.echo("  contents:")
                for f in files:
                    # filters
                    if '{' in str(f):
                        continue
                    if 'package-' in str(f): # very ad hoc solution, only relevant to the et_micc project itself
                        continue
                    if f.name=="__init__.py" and f.parent.samefile(package_path): # ignore the top-level __init__.py
                        continue
                    if 'build_' in str(f):
                        continue
                    
                    fg = 'green'
                    extra = ''
                    if f.name.startswith('cli'):
                        kind = "application "
                        fg = 'blue'
                    elif f.name.startswith('cpp_'):
                        kind = "C++ module  "
                        extra = f"{os.sep}{f.name.split('_',1)[1]}.cpp"
                    elif f.name.startswith('f2py_'):
                        kind = "f2py module "
                        extra = f"{os.sep}{f.name.split('_',1)[1]}.f90"
                    elif f.name=='__init__.py':
                        kind = "package     "
                    else:
                        kind = "module      "
                    click.echo("    " + kind + click.style(str(f.relative_to(package_path)) + extra,fg=fg))


    def version_cmd(self):
        """
        Bump the version according to ``rule`` or show the current version if no
        ``rule`` was specified
        
        The version is stored in pyproject.toml in the project directory, and in
        ``__version__`` variable of the top-level package (which is either in file
        ``<package_name>.py`` or ``<package_name>/__init__.py`` 
        
        """
        self.options.verbosity = max(1,self.options.verbosity)
        
        if not self.options.rule:
            if self.options.short:
                print(self.version)
            else:
                click.echo( "Project " + click.style(f"({self.project_name} ", fg='cyan')
                          + "version " + click.style(f"({self.version})"     , fg='cyan')
                          )  
        else:
            r = f"--{self.options.rule}"
            current_semver = semantic_version.Version(self.version)
            if self.options.rule=='patch':
                new_semver = current_semver.next_patch()
            elif self.options.rule=='minor':
                new_semver = current_semver.next_minor()
            elif self.options.rule=='major':
                new_semver = current_semver.next_major()
            else:
                r = f"--rule {self.options.rule}"
                new_semver = semantic_version.Version(self.options.rule)
                
            # update pyproject.toml
            if not self.options.dry_run:
                self.pyproject_toml['tool']['poetry']['version'] = str(new_semver)
                self.pyproject_toml.save()
                # update __version__
                look_for = f'__version__ = "{current_semver}"'
                replace_with = f'__version__ = "{new_semver}"'
                if self.module:
                    # update in <package_name>.py
                    et_micc.utils.replace_in_file(self.options.project_path / self.module, look_for, replace_with)
                else:
                    # update in <package_name>/__init__.py
                    p = self.options.project_path / self.package_name / "__version__.py"
                    if p.exists():
                        et_micc.utils.replace_in_file(p, look_for, replace_with)
                    else:
                        p = self.options.project_path / self.package
                        et_micc.utils.replace_in_file(p, look_for, replace_with)
                
                self.micc_logger.info(f"({self.project_name})> micc version ({current_semver}) -> ({new_semver})")
            else:
                click.echo(f"({self.project_name})> micc version {r} --dry-run : "
                          + click.style(f"({current_semver} ", fg='cyan') + "-> "
                          + click.style(f"({new_semver})"    , fg='cyan')
                          )  
            self.version = str(new_semver) # even if dry run!

    
    def tag_cmd(self):
        """Create and push a version tag ``vM.m.p`` for the current version."""
        tag = f"v{self.version}"
    
        micc_logger = et_micc.logging.get_micc_logger(self.options)
        with et_micc.utils.in_directory(self.options.project_path):
            micc_logger.info(f"Creating git tag {tag} for project {self.project_name}")
            cmd = ['git', 'tag', '-a', tag, '-m', f'"tag version {self.version}"']
            micc_logger.debug(f"Running '{' '.join(cmd)}'")
            completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            micc_logger.debug(completed_process.stdout.decode('utf-8'))
            if completed_process.stderr:
                micc_logger.critical(completed_process.stderr.decode('utf-8'))
    
            micc_logger.debug(f"Pushing tag {tag} for project {self.project_name}")
            cmd = ['git', 'push', 'origin', tag]
            micc_logger.debug(f"Running '{' '.join(cmd)}'")
            completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if completed_process.returncode==0:
                if completed_process.stdout:
                    micc_logger.debug(completed_process.stdout.decode('utf-8'))
            else:
                if completed_process.stdout:
                    micc_logger.warning(completed_process.stdout.decode('utf-8'))
                if completed_process.stderr:
                    micc_logger.warning(completed_process.stderr.decode('utf-8'))
                micc_logger.warning(f"Failed '{' '.join(cmd)}'\nRerun the command later (you must be online).")
                
        micc_logger.info('Done.')


    def add_cmd(self):
        """
        """
        if self.module:
            self.error(f"Cannot add to a module project ({self.module}).\n"
                       f"  Use `micc convert-to-package' on this project to convert it to a package project."
                      )
            return
        
        # set implied flags:
        if self.options.group:
            app_implied = f" [implied by --group   ({int(self.options.group  )})]"
            self.options.app = True
        else:
            app_implied = ""
            
        if self.options.package:
            py_implied  = f" [implied by --package ({int(self.options.package)})]"
            self.options.py = True
        else:
            py_implied = ""

        if (not (self.options.app or self.options.py or self.options.f2py or self.options.cpp) 
            or not xor(xor(self.options.app,self.options.py),xor(self.options.f2py,self.options.cpp))):
            # Do not log, as the state of the project is not changed.
            self.error(f"Specify one and only one of \n"
                       f"  --app  ({int(self.options.app )}){app_implied}\n"
                       f"  --py   ({int(self.options.py  )}){py_implied}\n"
                       f"  --f2py ({int(self.options.f2py)})\n"
                       f"  --cpp  ({int(self.options.cpp )})\n", fg='bright_red'
                      )
            return
    
        if self.options.app:
            app_name = self.options.add_name
            if self.app_exists(app_name):
                self.error(f"Project {self.project_name} has already an app named {app_name}.")
                return
            
            if not et_micc.utils.verify_project_name(app_name):
                self.error(
                    f"Not a valid app name ({app_name}_. Valid names:\n"
                    f"  * start with a letter [a-zA-Z]\n"
                    f"  * contain only [a-zA-Z], digits, hyphens, and underscores\n"
                )
                return
            
            if self.options.group:
                if not self.options.templates:
                    self.options.templates = 'app-sub-commands'
            else:
                if not self.options.templates:
                    self.options.templates = 'app-simple'
                                
            self.add_app()
            
        else:
            module_name = self.options.add_name
            if self.module_exists(module_name):
                self.error(f"Project {self.project_name} has already a module named {module_name}.")
                return
            
            if (not et_micc.utils.verify_project_name(module_name)
                or module_name!=et_micc.utils.pep8_module_name(module_name)):
                self.error(
                    f"Not a valid module name ({module_name}). Valid names:\n"
                    f"  * start with a letter [a-zA-Z]\n"
                    f"  * contain only [a-zA-Z], digits, and underscores\n"
                )
                return
    
#             self.options.template_parameters['path_to_cmake'] = et_micc.utils.path_to_cmake()
            
            if self.options.py:
                self.options.structure = 'package' if self.options.package else 'module'
                if not self.options.templates:
                    self.options.templates = 'module-py'
                self.add_python_module()
                        
            elif self.options.f2py:
                if not self.options.templates:
                    self.options.templates = 'module-f2py'
                self.add_f2py_module()
    
            elif self.options.cpp:
                if not self.options.templates:
                    self.options.templates = 'module-cpp'
                self.add_cpp_module()
    
    
    def add_app(self):
        """Add a console script (app) to the package."""
        project_path = self.options.project_path
        app_name = self.options.add_name
        cli_app_name = 'cli_' + et_micc.utils.pep8_module_name(app_name)
        w = 'with' if self.options.group else 'without' 
        
        micc_logger = et_micc.logging.get_micc_logger(self.options)
        with et_micc.logging.log(micc_logger.info, f"Adding CLI {app_name} {w} sub-commands to project {project_path.name}."):
            self.options.template_parameters.update(
                {'app_name': app_name, 'cli_app_name' : cli_app_name}
            )
         
            self.exit_code = et_micc.expand.expand_templates(self.options)
            if self.exit_code:
                self.micc_logger.critical(
                    f"Expand failed during Project.add_app for project ({self.project_name})."
                )
                return
    
            package_name = self.options.template_parameters['package_name']
            src_file = os.path.join(project_path.name, package_name, f"cli_{app_name}.py")
            tst_file = os.path.join(project_path.name, 'tests', f"test_cli_{app_name}.py")
            micc_logger.info(f"- Python source file {src_file}.")
            micc_logger.info(f"- Python test code   {tst_file}.")
            
            with et_micc.utils.in_directory(project_path):            
                # docs 
                with open('docs/index.rst',"r") as f:
                    lines = f.readlines()
                has_already_apps = False
                
                api_line = -1
                for l,line in enumerate(lines):
                    has_already_apps = has_already_apps or line.startswith("   apps")
                    if line.startswith('   api'):
                        api_line = l
                if not has_already_apps:
                    lines.insert(api_line,'   apps\n')
                    with open('docs/index.rst',"w") as f:
                        for line in lines:
                            f.write(line)
                txt = ''
                if not Path('APPS.rst').exists():
                    title = "Command Line Interfaces (apps)"
                    line = len(title) * '*' + '\n'
                    txt += ( line
                           + title + '\n'
                           + line
                           + '\n'
                           )
                else:
                    txt += (f".. click:: {package_name}.{cli_app_name}:main\n"
                            f"   :prog: {app_name}\n"
                            f"   :show-nested:\n\n"
                           )
                with open("APPS.rst","a") as f:
                    f.write(txt)

                # pyproject.toml
                self.add_dependencies({'click':'^7.0'})
                self.pyproject_toml['tool']['poetry']['scripts'][app_name] = f"{package_name}:{cli_app_name}.main"
                self.pyproject_toml.save()
                
                # TODO: add 'import <package_name>.cli_<app_name> to __init__.py
                line = f"import {package_name}.cli_{app_name}\n"
                file = project_path / self.package
                et_micc.utils.insert_in_file(file, [line], before=True, startswith="__version__")


    def add_python_module(self):
        """Add a python sub-module or sub-package to this project."""
        project_path = self.options.project_path
        module_name = self.options.add_name
        if not module_name==et_micc.utils.pep8_module_name(module_name):
            self.error(f"Not a valid module_name: {module_name}")
            return
            
        source_file = f"{module_name}.py" if self.options.structure=='module' else f"{module_name}{os.sep}__init__.py"
        
        with et_micc.logging.log(self.micc_logger.info,
                f"Adding python module {source_file} to project {project_path.name}."
            ):
            self.options.template_parameters.update({ 'module_name' : module_name })
         
            self.exit_code = et_micc.expand.expand_templates(self.options)
            if self.exit_code:
                self.micc_logger.critical(
                    f"Expand failed during Project.add_python_module for project ({self.project_name})."
                )
                return
    
            package_name = self.options.template_parameters['package_name']
            if self.options.structure=='package':
                self.module_to_package(project_path / package_name / (module_name + '.py'))
    
            package_name = self.options.template_parameters['package_name']
            src_file = os.path.join( project_path.name, package_name, source_file )
            tst_file = os.path.join( project_path.name, 'tests', 'test_' + module_name + '.py' )
                
            self.micc_logger.info(f"- python source in    {src_file}.")
            self.micc_logger.info(f"- Python test code in {tst_file}.")
            
            with et_micc.utils.in_directory(project_path):    
                # docs
                with open("API.rst","a") as f:
                    f.write(f"\n.. automodule:: {package_name}.{module_name}"
                             "\n   :members:\n\n"
                           )

        
    def add_f2py_module(self):
        """Add a f2py module to this project."""
        project_path = self.options.project_path
        module_name = self.options.add_name
        
        with et_micc.logging.log(self.micc_logger.info, 
                f"Adding f2py module {module_name} to project {project_path.name}."
            ):
            self.options.template_parameters.update({ 'module_name' : module_name })
    
            self.exit_code = et_micc.expand.expand_templates(self.options)
            if self.exit_code:
                self.micc_logger.critical(
                    f"Expand failed during Project.add_f2py_module for project ({self.project_name})."
                )
             
            package_name = self.options.template_parameters['package_name']
            src_file = os.path.join(           project_path.name
                                   ,           package_name
                                   , 'f2py_' + module_name
                                   ,           module_name + '.f90'
                                   )
            tst_file = os.path.join(           project_path.name
                                   , 'tests'
                                   , 'test_f2py_' + module_name + '.py'
                                   )
                
            rst_file = os.path.join(           project_path.name
                                   ,           package_name
                                   , 'f2py_' + module_name
                                   ,           module_name + '.rst'
                                   )
            self.micc_logger.info(f"- Fortran source in       {src_file}.")
            self.micc_logger.info(f"- Python test code in     {tst_file}.")
            self.micc_logger.info(f"- module documentation in {rst_file} (restructuredText format).")
            
            with et_micc.utils.in_directory(project_path):
                self.add_dependencies({'et-micc-build':CURRENT_ET_MICC_BUILD_VERSION})
                # docs
                with open("API.rst","a") as f:
                    f.write(f"\n.. include:: ../{package_name}/f2py_{module_name}/{module_name}.rst\n")
        
        
    def add_cpp_module(self):
        """Add a cpp module to this project."""
        project_path = self.options.project_path
        module_name = self.options.add_name
        
        with et_micc.logging.log(self.micc_logger.info,
                f"Adding cpp module cpp_{module_name} to project {project_path.name}."
            ):
            self.options.template_parameters.update({ 'module_name' : module_name })
    
            self.exit_code = et_micc.expand.expand_templates(self.options)
            if self.exit_code:
                self.micc_logger.critical(
                    f"Expand failed during Project.add_cpp_module for project ({self.project_name})."
                )
                return
    
            package_name = self.options.template_parameters['package_name']
            src_file = os.path.join(           project_path.name
                                   ,           package_name
                                   , 'cpp_'  + module_name
                                   ,           module_name + '.cpp'
                                   )
            tst_file = os.path.join(           project_path.name
                                   , 'tests'
                                   , 'test_cpp_' + module_name + '.py'
                                   )
                
            rst_file = os.path.join(           project_path.name
                                   ,           package_name
                                   , 'cpp_'  + module_name
                                   ,           module_name + '.rst'
                                   )
            self.micc_logger.info(f"- C++ source in           {src_file}.")
            self.micc_logger.info(f"- Python test code in     {tst_file}.")
            self.micc_logger.info(f"- module documentation in {rst_file} (restructuredText format).")
            
            with et_micc.utils.in_directory(project_path):
                self.add_dependencies({'et-micc-build':CURRENT_ET_MICC_BUILD_VERSION})
                # docs
                with open("API.rst","a") as f:
                    f.write(f"\n.. include:: ../{package_name}/cpp_{module_name}/{module_name}.rst\n")

    
    def app_exists(self, app_name):
        """Test if there is already an app with name ``app_name`` in this project.
        
        * :file:`<package_name>/cli_<app_name>.py`
            
        :param str app_name: app name
        :returns: bool
        """
        return (self.options.project_path / self.package_name / f"cli_{app_name}.py").is_file()
        

    def module_exists(self, module_name):
        """Test if there is already a module with name py:obj:`module_name` in this project.
    
        :param str module_name: module name
        :returns: bool
        """
        return (self.  py_module_exists(module_name)
             or self. py_package_exists(module_name)
             or self. cpp_module_exists(module_name)
             or self.f2py_module_exists(module_name)
               )
    
    def py_module_exists(self, module_name):
        """Test if there is already a python module with name :py:obj:`module_name` 
        in the project at :file:`project_path`.
            
        :param str module_name: module name
        :returns: bool
        """
        file = self.options.project_path / self.package_name / f'{module_name}.py'
        return file.is_file()
    
    
    def py_package_exists(self, module_name):
        """Test if there is already a python package with name :py:obj:`module_name` 
        in the project at :file:`project_path`.
            
        :param str module_name: module name
        :returns: bool
        """
        return (self.options.project_path / self.package_name / module_name / '__init__.py').is_file()
    
    
    def f2py_module_exists(self, module_name):
        """Test if there is already a f2py module with name py:obj:`module_name` in this project.
            
        :param str module_name: module name
        :returns: bool
        """
        return (self.options.project_path / self.package_name / ('f2py_' + module_name) / f"{ module_name}.f90").is_file() 


    def cpp_module_exists(self, module_name):
        """Test if there is already a cpp module with name py:obj:`module_name` in this project.
            
        :param str module_name: module name
        :returns: bool
        """
        return (self.options.project_path / self.package_name / ('cpp_' + module_name) / f"{ module_name}.cpp").is_file() 
    
    
    def add_dependencies(self,deps):
        """Add dependencies to the pyproject.toms file.
        
        :param dict deps: (package,version_constraint) pairs.
        """
        current_dependencies = self.pyproject_toml['tool']['poetry']['dependencies']
        for pkg,version in deps.items():
            if pkg in current_dependencies:
                current_version = current_dependencies[pkg]
                cv = et_micc.utils.constraint_to_version(current_version)
                v  = et_micc.utils.constraint_to_version(version)
                if cv < v:
                    current_dependencies[pkg] = version
            else:
                current_dependencies[pkg] = version
                
        self.pyproject_toml.save()
        
                
    def module_to_package(self, module_py):
        """Move file :file:`module.py` to :file:`module/__init__.py`.
        
        :param str|Path module_py: path to module.py
        """
        module_py = Path(module_py).resolve()
        
        if not module_py.is_file():
            raise FileNotFoundError(module_py)
        src = str(module_py)
        
        package_name = str(module_py.name).replace('.py','')
        package = module_py.parent / package_name
        package.mkdir()
        dst = str(package / '__init__.py')
        shutil.move(src, dst)
    
        et_micc.logging.log(self.micc_logger.debug, 
            f" . Module {module_py} converted to package {package_name}{os.sep}__init__.py."
        )
#eof