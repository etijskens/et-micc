# -*- coding: utf-8 -*-
"""
Main module.
"""
#===============================================================================
import os
import json
import subprocess
import shutil
import platform
from pathlib import Path
#===============================================================================
import click
from cookiecutter.main import cookiecutter

# import toml
from micc.tomlfile import TomlFile

from micc import utils

EXIT_CANCEL = -1 # exit code used for action canceled by user
EXIT_ABORT  = -2 # exit code used for action EXIT_CANCELled by user

def exit_msg(exit_code):
    the_micc_logger = utils.get_micc_logger.the_logger
    if exit_code==EXIT_CANCEL:
        the_micc_logger.warning("Command canceled, exiting!")
    elif exit_code!=0:
        the_micc_logger.error  (f"Error {exit_code}, exiting!")
    return exit_code


def resolve_template(template):
    """
    """
    if  template.startswith('~') or template.startswith(os.sep):
        pass # absolute path
    elif os.sep in template:
        # reative path
        template = Path.cwd() / template
    else:
        # just the template name 
        template = Path(__file__).parent / 'templates' / template

    if not template.exists():
        raise AssertionError(f"Inexisting template {template}")
    
    return template


def set_preferences(micc_file):
    """Set the preferences in *micc_file*.
    
    (This function requires user interaction!)
    
    :param Path micc_file: path to a json file.
    """
    with micc_file.open() as f:
        preferences = json.load(f)
        
    for parameter,description in preferences.items():
        if not description['default'].startswith('{{ '):
            answer = click.prompt(**description)
            preferences[parameter]['default'] = answer
            
    with micc_file.open(mode='w') as f:
        json.dump(preferences,f)
        
    return preferences


def get_preferences(micc_file):
    """Get the preferences from *micc_file*.
    
    (This function requires user interaction if no *micc_file* was provided!)

    :param Path micc_file: path to a json file.
    """
    if micc_file.samefile('.'):
        # There is no micc file with preferences yet.
        dotmicc = Path().home() / '.micc'
        dotmicc.mkdir(exist_ok=True)
        dotmicc_miccfile = dotmicc / 'micc.json'
        if dotmicc_miccfile.exists():
            preferences = get_preferences(dotmicc_miccfile)
        else:
            micc_file_template = Path(__file__).parent / 'micc.json'
            shutil.copyfile(str(micc_file_template),str(dotmicc_miccfile))
            preferences = set_preferences(dotmicc_miccfile)
    else:
        with micc_file.open() as f:
            preferences = json.load(f)

    return preferences


def get_template_parameters(preferences):
    """Get the template parameters from the preferences.
    
    :param dict|Path preferenes:
    :returns: dict of (parameter name,parameter value) pairs.
    """
    if isinstance(preferences,dict):
        template_parameters = {}
        for parameter,description in preferences.items():
            template_parameters[parameter] = description['default']
    elif isinstance(preferences,Path):
        with preferences.open() as f:
            template_parameters = json.load(f)
    else:
        raise RuntimeError()
    
    return template_parameters
    
    
def expand_templates(templates, template_parameters, global_options):
    """
    Expand a list of cookiecutter ``templates`` in directory ``project_path``. 

    If ``global_options.overwrite==False`` it is verified that no files will be over
    written inadvertently. In that case you get the option to EXIT_CANCEL the command, 
    or overwrite the files with our without creating backup files. If, on the other
    hand, ``global_options.overwrite==true``, pre-existing files are overwritten
    without warning.
    
    :param list templates: ordered list of (paths to) cookiecutter templates that 
        will be expanded as they appear. The template parameters are propagated 
        from each template to the next.
    :param dict template_parameters: the (template parameter,value) pairs.
    :param types.SimpleNamespace: command line options accessible to all micc
        commands
    """
    
    if not isinstance(templates, list):
        templates = [templates]
    project_path = global_options.project_path
    project_path.mkdir(parents=True, exist_ok=True)
    output_dir = project_path.parent
    micc_logger = utils.get_micc_logger.the_logger

    # list existing files that would be overwritten if global_options.overwrite==True
    existing_files = {}
    for template in templates:
        template = resolve_template(template)             
        # write a cookiecutter.json file in the cookiecutter template directory
        cookiecutter_json = template / 'cookiecutter.json'
        with open(cookiecutter_json,'w') as f:
            json.dump(template_parameters, f, indent=2)
        
        # run cookiecutter in an empty temporary directory to check if there are any
        # existing project files that would be overwritten.
        tmp = output_dir / '_cookiecutter_tmp_'
        if tmp.exists():
            shutil.rmtree(tmp)
        tmp.mkdir(parents=True, exist_ok=True)

        # expand the Cookiecutter template in a temporary directory,
        cookiecutter( str(template)
                    , no_input=True
                    , overwrite_if_exists=True
                    , output_dir=str(tmp)
                    )
        
        # find out if there are any files that would be overwritten.
        os_name = platform.system()
        for root, _, files in os.walk(tmp):
            if root==tmp:
                continue
            else:
                root2 = os.path.relpath(root,tmp)
            for f in files:
                if os_name=="Darwin" and f==".DS_Store":
                    continue
                file = output_dir / root2 / f
                if file.exists():
                    if not template in existing_files:
                        existing_files[template] = []
                    existing_files[template].append(file)
    
        if existing_files:
            if global_options.backup:
                micc_logger.warning(f"'--backup' specified: pre-existing files in {output_dir} will be backed up (*.bak):\n")
                for files in existing_files.values():
                    for src in files:
                        dst = src + '.bak'
                        shutil.copyfile(src, dst)
                        micc_logger.warning(f"     {src} -> {dst}")
                
            elif not global_options.overwrite:
                micc_logger.warning(f"'pre-existing files in {output_dir} that would be overwrtitten:\n")
                for files in existing_files.values():
                    for src in files:
                        micc_logger.warning(f"     {src}")
                click.secho("Aborting because 'overwrite==False'.\n"
                            "  Rerun the command with the '--overwrite' flag to overwrite these files.\n"
                            "  Rerun the command with the '--backup' flag to first backup these files (*.bak).\n"
                            "Aborting."
                           , fg='bright_red'
                           )
                return EXIT_ABORT
            else:
                micc_logger.warning(f"'--overwrite' specified: pre-existing files in {output_dir} will be overwritten WITHOUT backup:\n")
                for files in existing_files.values():
                    for src in files:
                        micc_logger.warning(f"     overwriting {src}")
                
    # Now we can safely overwrite pre-existing files.
    micc_logger.debug(f" . Expanding templates using these parameters:\n{json.dumps(template_parameters,indent=11)}")
    for template in templates:
        template = resolve_template(template)
        micc_logger.debug(f" . Expanding template {template}.")
        cookiecutter( str(template)
                    , no_input=True
                    , overwrite_if_exists=True
                    , output_dir=str(output_dir)
                    )
        # Clean up (see issue #7)
        cookiecutter_json = template / 'cookiecutter.json'
        cookiecutter_json.unlink()

    # Clean up
    if tmp.exists():
        shutil.rmtree(str(tmp))
        
    return 0


def msg_NotAProjectDirectory(path):
    return f"Invalid project directory {path}."


def msg_CannotAddToSimpleProject(path):
    return f"Cannot add components to simple project ({path})."


def msg_NotAPackageProject(path):
    return f"Not a package project ({path})."
    
def micc_create( templates
               , micc_file
               , global_options
               ):
    """
    Create a new project skeleton for a general Python project. This is a
    Python package with a ``<package_name>/__init__.py`` structure, to wich 
    other modules and applications can be added.
    
    :param str templates: ordered list of paths to a Cookiecutter template. a single 
        path is ok too.
    :param str micc_file: name of the json file with the default values in the template directories. 
    :param types.SimpleNamespace global_options: namespace object with options accepted by (almost) all micc commands. 
    """
    project_path = global_options.project_path
    project_path.mkdir(parents=True,exist_ok=True)
    contents = os.listdir(str(project_path))
    if contents:
        click.secho(f"Cannot create project in ({project_path}):\n"
                    f"  Directory must be empty."
                   , fg='bright_red'
                   )
        return 1
    if not global_options.allow_nesting:
        # Prevent the creation of a project inside another project    
        p = project_path.parent.resolve()
        while not p.samefile('/'):
            if utils.is_project_directory(p):
                click.secho(f"Cannot create project in ({project_path}):\n"
                            f"  Specify '--allow-nesting' to create a micc project inside another micc project ({p})."
                           , fg='bright_red'
                           )
                return 1
            p = p.parent
    
    project_name  = project_path.name
    package_name = utils.convert_to_valid_module_name(project_name)
    relative_project_path = project_path.relative_to(Path.cwd())
    if global_options.structure=='module':
        structure = f"({relative_project_path}{os.sep}{package_name}.py)"
    elif global_options.structure=='package':
        structure = f"({relative_project_path}{os.sep}{package_name}{os.sep}__init__.py)"
    else:
        structure = ''
    
    global_options.verbosity = max(1,global_options.verbosity)
    micc_logger = utils.get_micc_logger(global_options)
    with utils.logtime():
        with utils.log( micc_logger.info
                      , f"Creating project ({project_name}):"
                      ):
            micc_logger.info(f"Python {global_options.structure} ({package_name}): structure = {structure}")
            template_parameters = { 'project_name' : project_name
                                  , 'package_name' : package_name
                                  }
            template_parameters.update(global_options.template_parameters)
            template_parameters.update(get_template_parameters(get_preferences(micc_file)))
            global_options.overwrite = False
         
            exit_code = expand_templates( templates, template_parameters, global_options  )                
            
            if exit_code:
                return exit_msg(exit_code)
            
            my_micc_file = project_path / 'micc.json'
            with my_micc_file.open('w') as f:
                json.dump(template_parameters,f)
                micc_logger.debug(f" . Wrote project template parameters to {my_micc_file}.")
        
            with utils.log(micc_logger.debug,"Creating git repository"):
                with utils.in_directory(project_path):
                    cmds = [ ['git', 'init']
                           , ['git', 'add', '*']
                           , ['git', 'add', '.gitignore']
                           , ['git', 'commit', '-m', '"first commit"']
                           , ['git', 'remote', 'add', 'origin', f"https://github.com/{template_parameters['github_username']}/{project_name}"]
                           , ['git', 'push', '-u', 'origin', 'master']
                           ]
                    utils.execute(cmds, micc_logger.debug, stop_on_error=False)
    
    return 0


def micc_app( app_name
            , templates
            , global_options
            ):
    """
    Micc app subcommand, add a console script (app) to the package. 
    
    :param str app_name: name of the applicatiom to be added.
    :param str templates: ordered list of paths to a Cookiecutter template. a 
        single path is ok too.
    :param str micc_file: name of the json file with the default values in the 
        template directories.
    :param types.SimpleNamespace global_options: namespace object with options 
        accepted by (almost) all micc commands.
    """
    project_path = global_options.project_path

    utils.is_project_directory(project_path, raise_if=False)
    utils.is_package_project  (project_path, raise_if=False)
    utils.is_module_project   (project_path, raise_if=True )

    cli_app_name = 'cli_' + utils.convert_to_valid_module_name(app_name)
    
    micc_logger = utils.get_micc_logger(global_options)
    with utils.log(micc_logger.info, f"Creating app {app_name} in Python package {project_path.name}."):
        template_parameters = { 'app_name'     : app_name
                              , 'cli_app_name' : cli_app_name
                              }
        template_parameters.update(global_options.template_parameters)
     
        exit_code = expand_templates( templates, template_parameters, global_options )                

        if exit_code:
            micc_logger.critical(f"Exiting ({exit_code}) ...")
            return exit_code

        package_name = template_parameters['package_name']
        with utils.in_directory(project_path):            
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
            with open("APPS.rst","a") as f:
                title = f"\nApplication {app_name}"
                uline = len(title) * '='
                f.write(title + '\n')
                f.write(uline + '\n\n')
                f.write(f".. click:: {package_name}.{cli_app_name}\n")
                f.write(f"   :prog: {app_name}\n")
                f.write(f"   :show-nested:\n\n")
                
            micc_logger.debug(f" . documentation for application '{app_name}' added.")
            
            # pyproject.toml
            # in the [toolpoetry.scripts] add a line 
            #    {app_name} = "{package_name}:{cli_app_name}"
            pyproject_toml = TomlFile(project_path / 'pyproject.toml')
            pyproject_toml_content = pyproject_toml.read()
            pyproject_toml_content['tool']['poetry']['scripts'][app_name] = f'{package_name}:{cli_app_name}'
            pyproject_toml.write(pyproject_toml_content)

    return 0


def micc_module_py( module_name
                  , templates
                  , global_options
                  ):
    """
    ``micc module`` subcommand, add a Python module to the package. 
    
    :param str module_name: name of the module to be added.
    :param bool simple: create simple (``<module_name>.py``) or general python module 
    :param str templates: ordered list of paths to a Cookiecutter template. a 
        single path is ok too.
    :param str micc_file: name of the json file with the default values in the 
        template directories. 
    :param types.SimpleNamespace global_options: namespace object with options 
        accepted by (almost) all micc commands.
    """
    project_path = global_options.project_path
    
    utils.is_project_directory(project_path, raise_if=False)
    utils.is_package_project  (project_path, raise_if=False)
    utils.is_module_project   (project_path, raise_if=True )
    
    if not module_name==utils.convert_to_valid_module_name(module_name):
        raise AssertionError(f"Not a valid module_name: {module_name}")

    global_options.module_kind = 'python module'
    
    source_file = f"{module_name}.py" if global_options.structure=='module' else f"{module_name}/__init__.py"
    
    micc_logger = utils.get_micc_logger(global_options)
    with utils.log(micc_logger.info,f"Creating python module {source_file} in Python package {project_path.name}."):
        template_parameters = { 'module_name' : module_name }
        template_parameters.update(global_options.template_parameters)
     
        exit_code = expand_templates( templates, template_parameters, global_options )                        
        if exit_code:
            micc_logger.critical(f"Exiting ({exit_code}) ...")
            return exit_code

        package_name = template_parameters['package_name']
        if global_options.structure=='package':
            module_to_package(project_path / package_name / (module_name + '.py'))

        with utils.in_directory(project_path):    
            # docs
            with open("API.rst","a") as f:
                f.write(f"\n.. automodule:: {package_name}.{module_name}"
                         "\n   :members:\n\n"
                       )
            utils.log(micc_logger.debug,f" . documentation entries for Python module {module_name} added.")
    return 0


def micc_module_f2py( module_name
                    , templates
                    , global_options
                    ):
    """
    ``micc module --f2py`` subcommand, add a f2py module to the package. 
    
    :param str module_name: name of the module to be added.
    :param str templates: ordered list of paths to a Cookiecutter template. a 
        single path is ok too.
    :param str micc_file: name of the json file with the default values in the 
        template directories. 
    :param types.SimpleNamespace global_options: namespace object with options 
        accepted by (almost) all micc commands.
    """
    project_path = global_options.project_path
    
    utils.is_project_directory(project_path, raise_if=False)
    utils.is_package_project  (project_path, raise_if=False)
    utils.is_module_project   (project_path, raise_if=True )
    
    if not module_name==utils.convert_to_valid_module_name(module_name):
        raise AssertionError(f"Not a valid module_name {module_name}")

    global_options.module_kind = 'f2py module'
    
    micc_logger = utils.get_micc_logger(global_options)
    with utils.log(micc_logger.info,f"Creating f2py module f2py_{module_name} in Python package {project_path.name}."):
        template_parameters = { 'module_name' : module_name }
        template_parameters.update(global_options.template_parameters)

        exit_code = expand_templates( templates, template_parameters, global_options )                        
        if exit_code:
            micc_logger.critical(f"Exiting ({exit_code}) ...")
            return exit_code
            
        package_name = template_parameters['package_name']
        with utils.in_directory(project_path):
            # docs
            with open("API.rst","a") as f:
                f.write(f"\n.. include:: ../{package_name}/f2py_{module_name}/{module_name}.rst\n")
            micc_logger.warning(f" .  Documentation template for f2py module '{module_name}' added.\n"
                                f"    Because recent versions of sphinx are incompatible with sphinxfortran,\n"
                                f"    you are required to enter the documentation manually in file\n"
                                f"    '{project_path.name}/{package_name}/{module_name}.rst' in reStructuredText format.\n"
                                f"    A suitable example is pasted.\n"
                               )
    return 0


def micc_module_cpp( module_name
                   , templates
                   , global_options
                   ):
    """
    ``micc module --cpp`` subcommand, add a C++ module to the package. 
    
    :param str module_name: name of the module to be added.
    :param str templates: ordered list of paths to a Cookiecutter template. a 
        single path is ok too.
    :param str micc_file: name of the json file with the default values in the 
        template directories. 
    :param types.SimpleNamespace global_options: namespace object with options 
        accepted by (almost) all micc commands.
    """
    project_path = global_options.project_path

    utils.is_project_directory(project_path, raise_if=False)
    utils.is_package_project  (project_path, raise_if=False)
    utils.is_module_project   (project_path, raise_if=True )

    if not module_name==utils.convert_to_valid_module_name(module_name):
        raise AssertionError(f"Not a valid module_name {module_name}")

    global_options.module_kind = 'f2py module'
    
    micc_logger = utils.get_micc_logger(global_options)
    with utils.log(micc_logger.info,f"Creating f2py module f2py_{module_name} in Python package {project_path.name}."):
        template_parameters = { 'module_name' : module_name }
        template_parameters.update(global_options.template_parameters)

        exit_code = expand_templates( templates, template_parameters, global_options )
        if exit_code:
            micc_logger.critical(f"Exiting ({exit_code}) ...")
            return exit_code

        package_name = template_parameters['package_name']
        with utils.in_directory(project_path):
            # docs
            with open("API.rst","a") as f:
                f.write(f"\n.. include:: ../{package_name}/cpp_{module_name}/{module_name}.rst\n")
            micc_logger.warning(f"    Documentation template for cpp module '{module_name}' added.\n"
                                f"    Because recent versions of sphinx are incompatible with sphinxfortran,\n"
                                f"    you are required to enter the documentation manually in file\n"
                                f"    '{project_path.name}/{package_name}/{module_name}.rst' in reStructuredText format.\n"
                                f"    A suitable example is pasted.\n"
                               )
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
    :param types.SimpleNamespace global_options: namespace object with options 
        accepted by (almost) all micc commands.
    """
    project_path = global_options.project_path
    utils.is_project_directory(project_path, raise_if=False)

    pyproject_toml = TomlFile(project_path / 'pyproject.toml')
    pyproject_toml_content = pyproject_toml.read()
    current_version = pyproject_toml_content['tool']['poetry']['version']
    package_name    = utils.convert_to_valid_module_name(project_path.name)

    global_options.verbosity = max(1,global_options.verbosity)
    micc_logger = utils.get_micc_logger(global_options)
    
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
                rc = utils.execute(cmd)
                if rc:
                    return rc
                bumped_files.append(f)
        
        pyproject_toml = TomlFile(project_path / 'pyproject.toml')
        pyproject_toml_content = pyproject_toml.read()
        new_version = pyproject_toml_content['tool']['poetry']['version']
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
        pyproject_toml_content = pyproject_toml.read()
        new_version = pyproject_toml['tool']['poetry']['version']
            
        # update version in package                    
        for f in files[1:]: # skip pyproject.toml
            if f.exists():
                utils.replace_version_in_file(f, current_version, new_version)
                micc_logger.debug(f" . Updated {f.relative_to(project_path)}")

    return 0


def micc_tag( global_options):
    """
    Create and push a version tag ``vM.m.p`` for the current version.
    
    :param types.SimpleNamespace global_options: namespace object with options 
        accepted by (almost) all micc commands.
    """
    project_path = global_options.project_path
    utils.is_project_directory(project_path, raise_if=False)
            
    pyproject_toml = TomlFile(project_path / 'pyproject.toml')
    pyproject_toml_content = pyproject_toml.read()
    project_name    = pyproject_toml_content['tool']['poetry']['name']
    current_version = pyproject_toml_content['tool']['poetry']['version']
    tag = f"v{current_version}"

    micc_logger = utils.get_micc_logger(global_options)
    
    with utils.in_directory(project_path):
    
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
        micc_logger.debug(completed_process.stdout.decode('utf-8'))
        if completed_process.stderr:
            micc_logger.error(completed_process.stderr.decode('utf-8'))
            
    micc_logger.info('Done.')
    return 0


def micc_build( module_to_build
              , soft_link
              , global_options
              ):
    """
    Build all binary extions, i.e. f2py modules and cpp modules.
    
    :param str module_to_build: name of the only module to build (the prefix 
        ``cpp_`` or ``f2py_`` may be omitted)
    :param bool soft_link: if False, the binary extension modules are copied
        into the package directory. Otherwise a soft link is provided.
    :param types.SimpleNamespace global_options: namespace object with options 
        accepted by (almost) all micc commands.
    """
    project_path = global_options.project_path

    utils.is_project_directory(project_path, raise_if=False)
    utils.is_package_project  (project_path, raise_if=False)
    utils.is_module_project   (project_path, raise_if=True )
    
    package_path = project_path / utils.convert_to_valid_module_name(project_path.name)
        
    # get extension for binary extensions (depends on OS and python version)
    extension_suffix = utils.get_extension_suffix()

    dirs = os.listdir(package_path)
    for d in dirs:
        if (     (package_path / d).is_dir() 
             and (d.startswith("f2py_") or d.startswith("cpp_"))
           ):
            if module_to_build and not d.endswith(module_to_build): # build only this module
                continue

            build_log_file = project_path / f"micc-build-{d}.log"
            build_logger = utils.create_logger( build_log_file, filemode='w' )
 
            module_type,module_name = d.split('_',1)
            build_dir = package_path / d / 'build_'
            build_dir.mkdir(parents=True, exist_ok=True)

            with utils.log(build_logger.info,f"\nBuilding {module_type} module {module_name} in directory '{build_dir}'"):
                with utils.in_directory(build_dir):
                    cextension = module_name + extension_suffix
                    destination = (Path('../../') / cextension).resolve()
                    cmds = [ ['cmake','CMAKE_BUILD_TYPE','=','RELEASE', '..']
                           , ['make']
                           ]
                    if soft_link:
                        cmds.append(['ln', '-sf', str(cextension), str(destination)])
                    else:
                        if destination.exists():
                            build_logger.debug(f">>> os.remove({destination})\n")
                            destination.unlink()
                    # WARNING: for these commands to work in eclipse, eclipse must have
                    # started from the shell with the appropriate environment activated.
                    # Otherwise subprocess starts out with the wrong environment. It 
                    # may not pick the right Python version, and may not find pybind11.
                    returncode = utils.execute(cmds, build_logger.debug, stop_on_error=True, env=os.environ.copy())
                    if not returncode:
                        if not soft_link:
                            build_logger.debug(f">>> shutil.copyfile( '{cextension}', '{destination}' )\n")
                            shutil.copyfile(cextension, destination)
            build_logger.info(f"Check {build_log_file} for details.\n")

    return 0


def module_to_package(module_py):
    """
    Move file module.py to module/__init__.py
    
    :param str|Path module_py
    
    """
    if not isinstance(module_py, Path):
        module_py = Path(module_py)
    if not module_py.is_file():
        raise FileNotFoundError(module_py)
    src = str(module_py.resolve())
    
    package_name = str(module_py.name).replace('.py','')
    package = module_py.parent / package_name
    package.mkdir()
    dst = str(package / '__init__.py')
    shutil.move(src, dst)

    micc_logger = utils.get_micc_logger.the_logger
    utils.log(micc_logger.debug,f" . Module {module_py} converted to package {package_name}{os.sep}__init__.py.")


def micc_convert_simple(global_options):
    """
    Convert simple python package to general python package.

    :param types.SimpleNamespace global_options: namespace object with options 
        accepted by (almost) all micc commands.
    """
    project_path = global_options.project_path

    utils.is_project_directory(project_path, raise_if=False)
    utils.is_package_project  (project_path, raise_if=False)
    utils.is_module_project   (project_path, raise_if=True )
    
    if global_options.verbosity>0:
        click.echo(f"Converting simple Python project {project_path.name} to general Python project.")
    
    # add documentation files for general Python project
    pyproject_toml = TomlFile(project_path / 'pyproject.toml')
    pyproject_toml_content = pyproject_toml.read()

    template_parameters = {'project_short_description' : pyproject_toml_content['tool']['poetry']['description']}
    template_parameters.update(global_options.template_parameters)

    exit_code = expand_templates( "templates/package-general-docs", template_parameters, global_options )
    if exit_code:
        return exit_code
    
    package_name = utils.convert_to_valid_module_name(project_path.name)
    package_path = project_path / package_name
    os.makedirs(package_path)
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
        accepted by (almost) all micc commands.
    """
    
    project_path = global_options.project_path
    utils.is_project_directory(project_path, raise_if=False)

    micc_logger = utils.get_micc_logger(global_options)
    if not formats:
        micc_logger.info("No documentation format specified, using --html")
        formats.append('html')
        
    # this is still using the Makefile
    cmds = []
    for fmt in formats:
        cmds.append(['make',fmt])
        
    with utils.in_directory(project_path / 'docs'):
        with utils.log(micc_logger.info,f"Building documentation for project {project_path.name}."):
            utils.execute(cmds, micc_logger.debug, env=os.environ.copy())
    return 0


def micc_info(global_options):
    """
    Output info on the project.

    * If global_options.verbosity is 0, outputs the project name, the project location, 
      the package name and the version number
    * If global_options.verbosity is 1, lists also the structure and the applications
      and submodulesn it contains
    * If global_options.verbosity is 2, lists also the detailed structure of the package
    
    :param types.SimpleNamespace global_options: namespace object with options 
        accepted by (almost) all micc commands.
    """
    project_path = global_options.project_path
    utils.is_project_directory(project_path, raise_if=False)
    micc_logger = utils.get_micc_logger(global_options)
    package_name = utils.convert_to_valid_module_name(project_path.name)
    pyproject_toml = TomlFile(project_path / 'pyproject.toml')
    pyproject_toml_content = pyproject_toml.read()

    if global_options.verbosity>=0:
        global_options.verbosity = 10

    if global_options.verbosity>=1:
        click.echo("Project " + click.style(str(project_path.name),fg='green')+" located at "+click.style(str(project_path),fg='green'))
        click.echo("  package: " + click.style(str(package_name),fg='green'))
        click.echo("  version: " + click.style(pyproject_toml_content['tool']['poetry']['version'],fg='green'))
                  
    if global_options.verbosity>=2:
        has_py_module  = utils.is_module_project (project_path)
        has_py_package = utils.is_package_project(project_path)
        if has_py_module:
            structure = package_name + ".py"
            kind = " (Python module)"
        if has_py_package:
            structure = package_name + os.sep + "__init__.py"
            kind = " (Python package)"
        click.echo("  structure: " + click.style(structure,fg='green')+kind)
        if has_py_module and has_py_package:
            utils.log(micc_logger.warning, "\nFound both module and package structure."
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
                if 'package-' in str(f): # very ad hoc solution, only relevant to the micc project itself
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
    """
    """
    system = global_options.system
    if utils.is_poetry_available(system):
        if utils.is_conda_python():
            if 'install' in args:
                click.secho("WARNING: The command\n"
                            "  >  poetry install\n"
                            "is strongly discouraged in a conda Python environment!"
                           , fg='bright_red'
                           )
                return 1
        if system:
            cmd = ['poetry_',*args]
        else:
            cmd = ['poetry',*args]
        print(cmd)
        myenv = os.environ.copy()
        subprocess.run(cmd,env=myenv)
    else:
        click.secho("WARNING: poetry is not available in the environment."
                   , fg='bright_red'
                   )
        return 1

# EOF #