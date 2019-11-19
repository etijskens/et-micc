# -*- coding: utf-8 -*-
"""
Module et_micc.commands
=======================

Implementation of the commands in :file:`et_micc/cli.py`
"""
import os
import json
import subprocess
import shutil
from pathlib import Path

import click

import et_micc_tools.utils
import et_micc_tools.logging_tools
import et_micc.expand
from et_micc_tools.tomlfile import TomlFile


def micc_create( templates
               , micc_file
               , global_options
               ):
    """Create a new project skeleton for a Python project.
        
    :param str templates: Ordered list of paths to a Cookiecutter template. 
        A single path is ok too.
    :param str micc_file: Name of the json file with the default template parameter values. 
    :param types.SimpleNamespace global_options: namespace object with
        options accepted by (almost) all et_micc commands. Relevant attributes are 
        
        * **verbosity**
        * **project_path**: Path to the project on which the command operates.
        * **structure**: ``'module'`` | ``'package'``, wether a simple module
          :file:`<module_name>.py` or a package :file:`<module_name>/__init__.py`
          will be generated. 
        * **template_parameters**: extra template parameters not read from **micc_file**
        * **allow_nesting**: allow creation of project in the tree of another project.
    """
    project_path = global_options.project_path
    project_path.mkdir(parents=True,exist_ok=True)
    contents = os.listdir(str(project_path))
    if contents:
        # do not log here, because project is not created yet.
        click.secho(f"Cannot create project in ({project_path}):\n"
                    f"  Directory must be empty."
                   , fg='bright_red'
                   )
        return 1
    if not global_options.allow_nesting:
        # Prevent the creation of a project inside another project    
        p = project_path.parent.resolve()
        while not p.samefile('/'):
            if et_micc_tools.utils.is_project_directory(p):
                click.secho(f"Cannot create project in ({project_path}):\n"
                            f"  Specify '--allow-nesting' to create a et_micc project inside another et_micc project ({p})."
                           , fg='bright_red'
                           )
                return 1
            p = p.parent
    
    project_name  = project_path.name
    package_name = et_micc_tools.utils.convert_to_valid_module_name(project_name)
    try:
        relative_project_path = project_path.relative_to(Path.cwd())
    except ValueError:
        # project_path was specified relative to cwd using ../
        # use full path instead.
        relative_project_path = project_path
        
    if global_options.structure=='module':
        structure = f"({relative_project_path}{os.sep}{package_name}.py)"
    elif global_options.structure=='package':
        structure = f"({relative_project_path}{os.sep}{package_name}{os.sep}__init__.py)"
    else:
        structure = ''
    
    global_options.verbosity = max(1,global_options.verbosity)
    micc_logger = et_micc_tools.logging_tools.get_micc_logger(global_options)
    with et_micc_tools.logging_tools.logtime():
        with et_micc_tools.logging_tools.log( micc_logger.info
                      , f"Creating project ({project_name}):"
                      ):
            micc_logger.info(f"Python {global_options.structure} ({package_name}): structure = {structure}")
            template_parameters = { 'project_name' : project_name
                                  , 'package_name' : package_name
                                  }
            template_parameters.update(global_options.template_parameters)
            global_options.template_parameters = template_parameters
            global_options.overwrite = False
         
            exit_code = et_micc.expand.expand_templates( templates, global_options  )                
            if exit_code:
                micc_logger.critical(f"Exiting ({exit_code}) ...")
                return exit_code
            
            my_micc_file = project_path / 'micc.json'
            with my_micc_file.open('w') as f:
                json.dump(template_parameters,f)
                micc_logger.debug(f" . Wrote project template parameters to {my_micc_file}.")
        
            with et_micc_tools.logging_tools.log(micc_logger.info,"Creating git repository"):
                with et_micc_tools.utils.in_directory(project_path):
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
                    et_micc_tools.utils.execute(cmds, micc_logger.debug, stop_on_error=False)
    
    return 0

# Adding dependencies like this doesn't work
# def add_dependencies(deps,global_options):
#     """
#     We want to call ``poetry add dep`` for every dep in :py:obj:`deps`.
#     This fails with :py:obj:`ConnectionError` if you are offline, which would 
#     normally leave the project in inconsistent state. In addition this prohibits 
#     the user to use micc when he is off-line. 
# 
#     Therefor, we propose a two-step scenario.
#     
#     * First, if the dependency is written to :file:`new-deps.txt`
#     * then, the new dependencies are added by poetry and installed
#     
#     if this fails, the dep is added in pyproject.toml 
#     """
#     if not isinstance(deps, list):
#         deps = [deps]
#     current_deps = et_micc_tools.utils.get_dependencies()
#     new_deps = []
#     for dep in deps:
#         if not dep in current_deps:
#             new_deps.append(dep)
#     if new_deps:
#         poetry_add_dependencies(new_deps,global_options)
#        
#        
# def poetry_add_dependencies(new_deps,global_options=None):
#     """
#     :param Path path: path to :file:`<project_dir>/new_dependencies.txt`
#     :param list new_deps: list of dependencies to be added with poetry, if None, to be read from *path*.
#     """
#     new_dependencies_txt = Path('new_dependencies.txt')
#     if new_deps:
#         new_deps_ = new_deps
#     else:
#         with new_dependencies_txt.open() as f:
#             new_deps_ = json.load(f)
#            
#     failed = []
#     for dep in new_deps_:
#         try:
#             micc_poetry('add',dep,global_options=global_options)
#             
#         except Exception as e:
#             print(e) 
#             failed.append(dep)
#     if failed:
#         with open(new_dependencies_txt,'w') as f:
#             json.dump(failed,f)
#     else:
#         new_dependencies_txt.unlink(missing_ok=True)

def add_dependencies(deps):
    """
    :param dict deps: dict of (package,version) pairs
    """
    pyproject_toml = TomlFile(Path('pyproject.toml'))
    for key,value in deps.items():
        pyproject_toml['tool']['poetry']['dependencies'][key] = value
    pyproject_toml.save()
    
    
def micc_app( app_name
            , templates
            , global_options
            ):
    """Add a console script (app) to the package. 
    
    :param str app_name: name of the applicatiom to be added.
    :param str templates: ordered list of paths to a Cookiecutter template. a 
        single path is ok too.
    :param types.SimpleNamespace global_options: namespace object with
        options accepted by (almost) all et_micc commands. Relevant attributes are 
        
        * **verbosity**
        * **project_path**: Path to the project on which the command operates.
        * **template_parameters**: extra template parameters not read from *micc_file*
        * **group**: click CLI with/wihtout sub-commands
    """
    project_path = global_options.project_path

    et_micc_tools.utils.is_project_directory(project_path, raise_if=False)
    et_micc_tools.utils.is_package_project  (project_path, raise_if=False)
    et_micc_tools.utils.is_module_project   (project_path, raise_if=True )

    cli_app_name = 'cli_' + et_micc_tools.utils.convert_to_valid_module_name(app_name)
    w = 'with' if global_options.group else 'without' 
    
    micc_logger = et_micc_tools.logging_tools.get_micc_logger(global_options)
    with et_micc_tools.logging_tools.log(micc_logger.info, f"Adding CLI {app_name} {w} sub-commands to project {project_path.name}."):
        global_options.template_parameters.update({ 'app_name'     : app_name
                                                  , 'cli_app_name' : cli_app_name
                                                  })
     
        exit_code = et_micc.expand.expand_templates( templates, global_options )                
        if exit_code:
            micc_logger.critical(f"Exiting ({exit_code}) ...")
            return exit_code

        package_name = global_options.template_parameters['package_name']
        src_file = os.path.join(project_path.name, package_name, f"cli_{app_name}.py")
        tst_file = os.path.join(project_path.name, 'tests', f"test_cli_{app_name}.py")
        micc_logger.info(f"- Python source file {src_file}.")
        micc_logger.info(f"- Python test code   {tst_file}.")
        
        with et_micc_tools.utils.in_directory(project_path):            
            # add dependencies:
            add_dependencies({'click','^7.0'})
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
            # in the [toolpoetry.scripts] add a line 
            #    {app_name} = "{package_name}:{cli_app_name}"
            pyproject_toml = TomlFile(project_path / 'pyproject.toml')
            pyproject_toml['tool']['poetry']['scripts'][app_name] = f'{package_name}:{cli_app_name}.main'
            pyproject_toml.save()

    return 0


def micc_module_py( module_name
                  , templates
                  , global_options
                  ):
    """Add a Python module to the package. 
    
    :param str module_name: name of the module to be added.
    :param str templates: ordered list of paths to a Cookiecutter template. a 
        single path is ok too.
    :param types.SimpleNamespace global_options: namespace object with
        options accepted by (almost) all et_micc commands. Relevant attributes are 
        
        * **verbosity**
        * **project_path**: Path to the project on which the command operates.
        * **structure**: ``'module'`` | ``'package'``: wether a simple module
          :file:`<module_name>.py` or a package :file:`<module_name>/__init__.py`
          will be generated. 
        * **template_parameters**: extra template parameters not read from *micc_file*
    """
    project_path = global_options.project_path
    
    try:
        et_micc_tools.utils.is_project_directory(project_path, raise_if=False)
    except Exception as x:
        click.secho(f"ERROR: {x}", fg='bright_red')
        if global_options.verbosity>1:
            raise
        else:
            return 1
        
    try:
        et_micc_tools.utils.is_package_project(project_path, raise_if=False)
    except Exception as x:
        click.secho(f"ERROR: {x}", fg='bright_red')
        if global_options.verbosity>1:
            raise
        else:
            return 1
        
    try:
        et_micc_tools.utils.is_module_project(project_path, raise_if=True )
    except Exception as x:
        click.secho(f"ERROR: {x}", fg='bright_red')
        if global_options.verbosity>1:
            raise 
        else:
            return 1
    
    if not module_name==et_micc_tools.utils.convert_to_valid_module_name(module_name):
        msg = f"Not a valid module_name: {module_name}"
        click.secho("ERROR: " + msg, fg='bright_red')
        if global_options.verbosity>1:
            raise AssertionError(msg)
        else:
            return 1 
        
    source_file = f"{module_name}.py" if global_options.structure=='module' else f"{module_name}{os.sep}__init__.py"
    
    micc_logger = et_micc_tools.logging_tools.get_micc_logger(global_options)
    with et_micc_tools.logging_tools.log(micc_logger.info,f"Adding python module {source_file} to project {project_path.name}."):
        global_options.template_parameters.update({ 'module_name' : module_name })
     
        exit_code = et_micc.expand.expand_templates( templates, global_options )                        
        if exit_code:
            micc_logger.critical(f"Exiting ({exit_code}) ...")
            return exit_code

        package_name = global_options.template_parameters['package_name']
        if global_options.structure=='package':
            module_to_package(project_path / package_name / (module_name + '.py'))

        package_name = global_options.template_parameters['package_name']
        src_file = os.path.join( project_path.name, package_name, source_file )
        tst_file = os.path.join( project_path.name, 'tests', 'test_' + module_name + '.py' )
            
        micc_logger.info(f"- python source in    {src_file}.")
        micc_logger.info(f"- Python test code in {tst_file}.")
        
        with et_micc_tools.utils.in_directory(project_path):    
            # docs
            with open("API.rst","a") as f:
                f.write(f"\n.. automodule:: {package_name}.{module_name}"
                         "\n   :members:\n\n"
                       )
    return 0


def micc_module_f2py( module_name
                    , templates
                    , global_options
                    ):
    """
    ``et_micc module --f2py`` subcommand, add a f2py module to the package. 
    
    :param str module_name: name of the module to be added.
    :param str templates: ordered list of paths to a Cookiecutter template. a 
        single path is ok too.
    :param types.SimpleNamespace global_options: namespace object with
        options accepted by (almost) all et_micc commands. Relevant attributes are 
        
        * **verbosity**
        * **project_path**: Path to the project on which the command operates.
        * **template_parameters**: extra template parameters not read from *micc_file*
    """
    project_path = global_options.project_path
    
    et_micc_tools.utils.is_project_directory(project_path, raise_if=False)
    et_micc_tools.utils.is_package_project  (project_path, raise_if=False)
    et_micc_tools.utils.is_module_project   (project_path, raise_if=True )
    
    if not module_name==et_micc_tools.utils.convert_to_valid_module_name(module_name):
        raise AssertionError(f"Not a valid module_name {module_name}")
    
    micc_logger = et_micc_tools.logging_tools.get_micc_logger(global_options)
    with et_micc_tools.logging_tools.log(micc_logger.info,f"Adding f2py module {module_name} to project {project_path.name}."):
        global_options.template_parameters.update({ 'module_name' : module_name })

        exit_code = et_micc.expand.expand_templates( templates, global_options )                        
        if exit_code:
            micc_logger.critical(f"Exiting ({exit_code}) ...")  
            return exit_code
         
        package_name = global_options.template_parameters['package_name']
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
        micc_logger.info(f"- Fortran source in       {src_file}.")
        micc_logger.info(f"- Python test code in     {tst_file}.")
        micc_logger.info(f"- module documentation in {rst_file} (restructuredText format).")
        
        with et_micc_tools.utils.in_directory(project_path):
            # add dependencies:
            add_dependencies({'et-micc-build':'^0.0.1',
                              'numpy'        :'^1.17.4',
                             })
            # docs
            with open("API.rst","a") as f:
                f.write(f"\n.. include:: ../{rst_file}\n")
    return 0


def micc_module_cpp( module_name
                   , templates
                   , global_options
                   ):
    """
    ``et_micc module --cpp`` subcommand, add a C++ module to the package. 
    
    :param str module_name: name of the module to be added.
    :param str templates: ordered list of paths to a Cookiecutter template. a 
        single path is ok too.
    :param str micc_file: name of the json file with the default values in the 
        template directories. 
    :param types.SimpleNamespace global_options: namespace object with
        options accepted by (almost) all et_micc commands. Relevant attributes are 
        
        * **verbosity**
        * **project_path**: Path to the project on which the command operates.
        * **template_parameters**: extra template parameters not read from *micc_file*
    """
    project_path = global_options.project_path

    et_micc_tools.utils.is_project_directory(project_path, raise_if=False)
    et_micc_tools.utils.is_package_project  (project_path, raise_if=False)
    et_micc_tools.utils.is_module_project   (project_path, raise_if=True )

    if not module_name==et_micc_tools.utils.convert_to_valid_module_name(module_name):
        raise AssertionError(f"Not a valid module_name {module_name}")
    
    micc_logger = et_micc_tools.logging_tools.get_micc_logger(global_options)
    with et_micc_tools.logging_tools.log(micc_logger.info,f"Adding cpp module cpp_{module_name} to project {project_path.name}."):
        global_options.template_parameters.update({ 'module_name' : module_name })

        exit_code = et_micc.expand.expand_templates( templates, global_options )
        if exit_code:
            micc_logger.critical(f"Exiting ({exit_code}) ...")
            return exit_code

        package_name = global_options.template_parameters['package_name']
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
        micc_logger.info(f"- C++ source in           {src_file}.")
        micc_logger.info(f"- Python test code in     {tst_file}.")
        micc_logger.info(f"- module documentation in {rst_file} (restructuredText format).")
        
        with et_micc_tools.utils.in_directory(project_path):
            # add dependencies:
                        # add dependencies:
            add_dependencies({'et-micc-tools':'^0.1.0',
                              'numpy'        :'^1.17.4',
                              'cmake'        :'^3.15.3',
                              'pybind11'     :'^2.2.4',
                             })
            # docs
            with open("API.rst","a") as f:
                f.write(f"\n.. include:: ../{package_name}/cpp_{module_name}/{module_name}.rst\n")
    return 0


def micc_version( rule, short, poetry, global_options):
    """
    Bump the version according to ``rule`` or show the current version if no
    ``rule`` was specified
    
    The version is stored in pyproject.toml in the project directory, and in
    ``__version__`` variable of the top-level package (which is either in file
    ``<package_name>.py`` or ``<package_name>/__init__.py`` 
    
    :param str rule: one of the valid arguments for the ``poetry version <rule>``
        command.
    :param bool short: if true only prints the current version to stdout.
    :param bool poetry: use poetry instead of bumpversion to bump the version.
    :param types.SimpleNamespace global_options: namespace object with
        options accepted by (almost) all et_micc commands. Relevant attributes are 
        
        * **verbosity**
        * **project_path**: Path to the project on which the command operates.
        * **template_parameters**: extra template parameters not read from *micc_file*
    """
    project_path = global_options.project_path
    et_micc_tools.utils.is_project_directory(project_path, raise_if=False)

    pyproject_toml = TomlFile(project_path / 'pyproject.toml')
    current_version = pyproject_toml['tool']['poetry']['version']
    package_name    = et_micc_tools.utils.convert_to_valid_module_name(project_path.name)

    global_options.verbosity = max(1,global_options.verbosity)
    micc_logger = et_micc_tools.logging_tools.get_micc_logger(global_options)
    
    if short:
        print(current_version)
        return 0
    
    if not rule:
        micc_logger.info(f"Project ({project_path.name}) version ({current_version})")
        return 0

    files = [ project_path / 'pyproject.toml'
            , project_path / package_name / '__init__.py'
            , project_path / (package_name + '.py')
            ]
    
    bumpversion = not poetry
    if bumpversion:
        # Use bump(2)version for bumping versions
        bumped_files = []
        for f in files:
            if f.exists():
                cmd = ['bumpversion','--allow-dirty','--verbose'
                      ,'--current-version',current_version,rule,str(f)]
                rc = et_micc_tools.utils.execute(cmd)
                if rc:
                    return rc
                bumped_files.append(f)
        
        pyproject_toml = TomlFile(project_path / 'pyproject.toml')
        new_version = pyproject_toml['tool']['poetry']['version']
        micc_logger.info(f"bumping version ({current_version}) -> ({new_version})")
        for f in bumped_files:
            micc_logger.debug(f". Updated ({f})")
    
    else:    
        # Use poetry to update version in pyproject.toml
        myenv = os.environ.copy()
        cmd = ['poetry','version',rule]
        result = subprocess.run(cmd, capture_output=True, cwd=str(project_path), env=myenv)
        if result.returncode:
            return result.returncode
        micc_logger.warning(result.stdout.decode('utf-8'))
        micc_logger.debug(" . Updated pyproject.toml")
                    
        pyproject_toml = TomlFile(project_path / 'pyproject.toml')
        new_version = pyproject_toml['tool']['poetry']['version']
            
        # update version in package                    
        for f in files[1:]: # skip pyproject.toml
            if f.exists():
                et_micc_tools.utils.replace_version_in_file(f, current_version, new_version)
                micc_logger.debug(f" . Updated {f.relative_to(project_path)}")

    return 0


def micc_tag(global_options):
    """Create and push a version tag ``vM.m.p`` for the current version.
    
    :param types.SimpleNamespace global_options: namespace object with
        options accepted by (almost) all et_micc commands. Relevant attributes are 
        
        * **verbosity**
        * **project_path**: Path to the project on which the command operates.
        * **template_parameters**: extra template parameters not read from *micc_file*
    """
    project_path = global_options.project_path
    et_micc_tools.utils.is_project_directory(project_path, raise_if=False)
            
    pyproject_toml = TomlFile(project_path / 'pyproject.toml')
    project_name    = pyproject_toml['tool']['poetry']['name']
    current_version = pyproject_toml['tool']['poetry']['version']
    tag = f"v{current_version}"

    micc_logger = et_micc_tools.logging_tools.get_micc_logger(global_options)
    
    with et_micc_tools.utils.in_directory(project_path):
    
        micc_logger.info(f"Creating git tag {tag} for project {project_name}")
        cmd = ['git', 'tag', '-a', tag, '-m', f'"tag version {current_version}"']
        micc_logger.debug(f"Running '{' '.join(cmd)}'")
        completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        micc_logger.debug(completed_process.stdout.decode('utf-8'))
        if completed_process.stderr:
            micc_logger.critical(completed_process.stderr.decode('utf-8'))

        micc_logger.debug(f"Pushing tag {tag} for project {project_name}")
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
    return 0




def module_to_package(module_py):
    """Move file :file:`module.py` to :file:`module/__init__.py`.
    
    :param str|Path module_py: path to module.py
    
    """
    module_py = Path(module_py)
    if not module_py.is_file():
        raise FileNotFoundError(module_py)
    src = str(module_py.resolve())
    
    package_name = str(module_py.name).replace('.py','')
    package = module_py.parent / package_name
    package.mkdir()
    dst = str(package / '__init__.py')
    shutil.move(src, dst)

    micc_logger = et_micc_tools.logging_tools.get_micc_logger()
    et_micc_tools.logging_tools.log(micc_logger.debug,f" . Module {module_py} converted to package {package_name}{os.sep}__init__.py.")


def micc_convert_simple(global_options):
    """Convert simple python package to general python package.

    :param types.SimpleNamespace global_options: namespace object with options 
        accepted by (almost) all et_micc commands. Relevant options are:
        
        * 
    """
    project_path = global_options.project_path

    et_micc_tools.utils.is_project_directory(project_path, raise_if=False)
    et_micc_tools.utils.is_package_project  (project_path, raise_if=True )
    et_micc_tools.utils.is_module_project   (project_path, raise_if=False)
    
    if global_options.verbosity>0:
        click.echo(f"Converting simple Python project {project_path.name} to general Python project.")
    
    # add documentation files for general Python project
    pyproject_toml = TomlFile(project_path / 'pyproject.toml')

    global_options.template_parameters.update(
        {'project_short_description' : pyproject_toml['tool']['poetry']['description']}
    )

    exit_code = et_micc.expand.expand_templates( "package-general-docs", global_options )
    if exit_code:
        et_micc_tools.logging_tools.get_micc_logger().critical(f"Exiting ({exit_code}) ...")
        return exit_code
    
    package_name = et_micc_tools.utils.convert_to_valid_module_name(project_path.name)
    package_path = project_path / package_name
    os.makedirs(package_path,exist_ok=True)
    src = project_path /(package_name + '.py')
    dst = project_path / package_name / '__init__.py'
    shutil.move(src, dst)
    
    return 0


def micc_docs(formats, global_options):
    """
    Build documentation for the project.
    
    :param list formats: list of formats to build documentation with. Valid
        formats are ``'html'``, ``'latexpdf'``.
    :param types.SimpleNamespace global_options: namespace object with options 
        accepted by (almost) all et_micc commands. Relevant attributes are 
        
        * **verbosity**
        * **project_path**: Path to the project on which the command operates.
    """
    
    project_path = global_options.project_path
    et_micc_tools.utils.is_project_directory(project_path, raise_if=False)

    micc_logger = et_micc_tools.logging_tools.get_micc_logger(global_options)
    if not formats:
        micc_logger.info("No documentation format specified, using --html")
        formats.append('html')
        
    # this is still using the Makefile
    cmds = []
    for fmt in formats:
        cmds.append(['make',fmt])
        
    with et_micc_tools.utils.in_directory(project_path / 'docs'):
        with et_micc_tools.logging_tools.log(micc_logger.info,f"Building documentation for project {project_path.name}."):
            et_micc_tools.utils.execute(cmds, micc_logger.debug, env=os.environ.copy())
    return 0


def micc_info(global_options):
    """Output info on the project.
    
    :param types.SimpleNamespace global_options: namespace object with options 
        accepted by (almost) all et_micc commands. Relevant attributes are 
        
        * **verbosity**: If **verbosity** is 0, outputs the project name,
          the project location, the package name and the version number. 
          If **verbosity** is 1, lists also the structure and the applications
          and submodules it contains. If **verbosity** is 2, lists also the
          detailed structure of the package.
        * **project_path**: Path to the project on which the command operates..
    """
    project_path = global_options.project_path
    et_micc_tools.utils.is_project_directory(project_path, raise_if=False)
    micc_logger = et_micc_tools.logging_tools.get_micc_logger(global_options)
    package_name = et_micc_tools.utils.convert_to_valid_module_name(project_path.name)
    pyproject_toml = TomlFile(project_path / 'pyproject.toml')

    if global_options.verbosity>=0:
        global_options.verbosity = 10

    if global_options.verbosity>=1:
        click.echo("Project " + click.style(str(project_path.name),fg='green')+" located at "+click.style(str(project_path),fg='green'))
        click.echo("  package: " + click.style(str(package_name),fg='green'))
        click.echo("  version: " + click.style(pyproject_toml['tool']['poetry']['version'],fg='green'))
                  
    if global_options.verbosity>=2:
        has_py_module  = et_micc_tools.utils.is_module_project (project_path)
        has_py_package = et_micc_tools.utils.is_package_project(project_path)
        if has_py_module:
            structure = package_name + ".py"
            kind = " (Python module)"
        if has_py_package:
            structure = package_name + os.sep + "__init__.py"
            kind = " (Python package)"
        click.echo("  structure: " + click.style(structure,fg='green')+kind)
        if has_py_module and has_py_package:
            et_micc_tools.logging_tools.log(micc_logger.warning, "\nFound both module and package structure."
                                           "\nThis will give import problems.")
    if global_options.verbosity>=3:
        package_path = project_path / package_name
        files = []
        files.extend(package_path.glob('**/*.py'))
        files.extend(package_path.glob('**/cpp_*/'))
        files.extend(package_path.glob('**/f2py_*'))
        if files:
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
    return 0


def micc_poetry(*args, global_options):
    """Execute a poetry commanbd.
    
    If you are working in a conda Python environment, using poetry commaands
    that cause trouble is prohibited.
    """
    if et_micc_tools.utils.is_conda_python():
        if 'install' in args:
            click.secho("WARNING: The command\n"
                        "  >  poetry install\n"
                        "is strongly discouraged in a conda Python environment!"
                       , fg='bright_red'
                       )
            return 1
    cmd = ['poetry',*args]
    print(' '.join(cmd))
    myenv = os.environ.copy()
    completed_process = subprocess.run(cmd, env=myenv) #capture_output=True, 
    if completed_process.returncode:
        raise Exception()


import site
import walkdir

def link_files(source,destination,logger=None):
    """
    This method creates a copy of the directory structure at *source*, 
    and create a symlink for every file in the directory structure

    :param Path source: in dev-install the path to a package directory
    :param Path destination: in dev-install the path to the current environment's :file:`site-packages:
    """
    dd = destination / source.name
    dd.mkdir(exist_ok=True)
    if logger:
        logger.debug(f"Creating directory {dd}")
    for root, dirs, files in walkdir.filtered_walk(str(source)
                                                  , excluded_dirs=['f2py_*','cpp_*','__pycache__']
                                                  , excluded_files=['.DS_Store','*.json']
                                                  ):
        r = Path(root).relative_to(source.parent)
        for d in dirs:                
            dd = ( destination / r / d)
            dd.mkdir(exist_ok=True)
            if logger:
                logger.debug(f"Creating directory {dd}")
        for f in files:
            src = Path(root) / f
            df = (destination / r /f )
            df.symlink_to(src) 
            if logger:
                logger.debug(f"Creating symlink {df}")
        
    logger.debug(f"Creating directory {dd}")
            
def micc_dev_install(global_options, install=True):
    """
    """
    project_path = global_options.project_path
    et_micc_tools.utils.is_project_directory(project_path, raise_if=False)
    micc_logger = et_micc_tools.logging_tools.get_micc_logger(global_options)
    package_name = et_micc_tools.utils.convert_to_valid_module_name(project_path.name)

    site_packages = Path(site.getsitepackages()[0])
    
    un = '' if install else 'un'
    when = 'before' if install else 'after'
    with et_micc_tools.logging_tools.log(micc_logger.info, f"dev-install of {package_name}"):
        micc_logger.warning(f"Run 'make {un}install' {when} 'et_micc dev-{un}install'")
        dst_package = site_packages / package_name
        if dst_package.is_dir():
            micc_logger.debug(f"Removing directory {dst_package} + all contents.")
            shutil.rmtree(dst_package)
        if install:
            link_files(project_path / package_name, site_packages, micc_logger)
    
    
# EOF #