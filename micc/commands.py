# -*- coding: utf-8 -*-
"""
Main module.
"""
#===============================================================================
import os
import sysconfig
import json
import subprocess
import shutil
import platform
import copy
import logging,sys
#===============================================================================
import click
from cookiecutter.main import cookiecutter

from poetry.console.application import Application
from cleo.inputs.argv_input import ArgvInput
from poetry.utils.toml_file import TomlFile
from poetry.console.commands import VersionCommand 
import toml
#===============================================================================
from micc import utils
from micc.utils import in_directory


def verbosity_to_loglevel(verbosity):
    """
    """
    if verbosity==0:
        return logging.CRITICAL
    elif verbosity==1:
        return logging.INFO
    else:
        return logging.DEBUG
     
     
# create logger for micc
micc_logger = logging.getLogger('micc_logger')
micc_logger.setLevel(logging.DEBUG)
# create a console handler 
micc_console_loghandler = logging.StreamHandler(sys.stderr)
micc_console_loghandler.setLevel(verbosity_to_loglevel(verbosity=1))
micc_logger.addHandler(micc_console_loghandler)
# create a logfile handler 
micc_logfile_handler = logging.FileHandler('micc.log')
micc_logger.addHandler(micc_logfile_handler)
micc_logfile_handler.setLevel(logging.DEBUG)
# create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') # add formatter to micc_console_loghandler
formatter = logging.Formatter('[%(levelname)s] %(message)s') # add formatter to micc_console_loghandler
micc_console_loghandler.setFormatter(formatter) 
micc_logfile_handler.setFormatter(formatter) 

EXIT_CANCEL = -1 # exit code used for action EXIT_CANCELled by user
def exit_msg(exit_code):
    if exit_code==EXIT_CANCEL:
        micc_logger.warning("Command canceled, exiting!")
    elif exit_code!=0:
        micc_logger.error(f"Error {exit_code}, exiting!")
    return exit_code

def resolve_template(template):
    """
    """
    if  template.startswith('~') or template.startswith(os.sep):
        pass # absolute path
    elif os.sep in template:
        # reative path
        template = os.path.join(os.getcwd(), template)
    else:
        # jutst the template name 
        template = os.path.join(os.path.dirname(__file__), template)
    return template


def get_template_parameters(template, micc_file, **kwargs):
    """
    Read the template parameter descriptions from the micc file, and
    prompt the user for supplying the values for the parameters with an
    empty string as default.     
    
    :returns: a dict of (parameter,value) pairs.
    """
    micc_file = os.path.join(template, micc_file)
    try:
        f = open(micc_file, 'r')
    except IOError:
        micc_logger.debug(f" . getting template parameters from (None)")
        template_parameters = {}
    else:
        with f:
            micc_logger.debug(f" . getting template parameters from {micc_file}.")
            template_parameters = json.load(f)
      
    for kw,arg in kwargs.items(): 
        template_parameters[kw] = {} 
        template_parameters[kw]['default'] = arg 
    
    for key,value in template_parameters.items():
        default = value['default']
        if bool(default):
            value = default
        else:
            kwargs = value
#             text = kwargs['text']
#             del kwargs['msg']
            if 'type' in kwargs:
                kwargs['type'] = eval(kwargs['type'])
            click.echo('')
            value = False
            while not value:
                value = click.prompt(**kwargs,show_default=False)
        template_parameters[key] = value

    micc_logger.debug(f" . parameters used:\n{json.dumps(template_parameters,indent=4)}")
    return template_parameters


def expand_templates(templates, micc_file, project_path, global_options, **extra_parameters):
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
    :param str micc_file: name of the micc file in all templates. Usually, this is
        ``'micc.json'``.
    :param str project_path: path to the project directory where the templates 
        will be expanded
    :param types.SimpleNamespace: command line options accessible to all micc
        commands
    :param dict extra_parameters: extra template parameters that have to be set 
        before 
        expanding.
    """
    if not isinstance(templates, list):
        templates = [templates]
    output_dir = os.path.abspath(os.path.join(project_path, '..'))
    os.makedirs(project_path, exist_ok=True)

    # get the template parameters,
    # list existing files that would be overwritten if global_options.overwrite==True
    existing_files = {}
    for template in templates:
        micc_logger.debug(f" . Expanding template {template} in temporary directory")
        template = resolve_template(template)             
        template_parameters = get_template_parameters( template, micc_file
                                                     , **extra_parameters
                                                     )
        # Store the template parameters from this template for the the next
        # template in the templates list
        extra_parameters = template_parameters
        # write a cookiecutter.json file in the cookiecutter template directory
        cookiecutter_json = os.path.join(template, 'cookiecutter.json')
        with open(cookiecutter_json,'w') as f:
            json.dump(template_parameters, f, indent=2)
        
        # run cookiecutter in an empty temporary directory to check if there are any
        # existing project files that woud be overwritten.
        if not global_options.overwrite:
            tmp = os.path.join(output_dir, '_cookiecutter_tmp_')
            if os.path.exists(tmp):
                shutil.rmtree(tmp)
            os.makedirs(tmp, exist_ok=True)
    
            # expand the Cookiecutter template in a temporary directory,
            cookiecutter( template
                        , no_input=True
                        , overwrite_if_exists=True
                        , output_dir=tmp
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
                    file = os.path.join(output_dir, root2, f)
    #                     print('FILE',file, 'exists =', os.path.exists(file))
                    if os.path.exists(file):                            
                        if not template in existing_files:
                            existing_files[template] = []
                        existing_files[template].append(file)
    
        if existing_files:
            msg = f"The following pre-existing files will be overwritten in {output_dir}:\n"
            for template, files in existing_files.items():
                t = os.path.basename(template)
                for f in files:
                    msg += f"    {t} : {f}\n"
            micc_logger.warning(msg)
            answer = click.prompt("Press 'c' to continue\n"
                                  "      'a' to abort\n"
                                  "      'b' to keep the original files with .bak extension\n"
                                 ,type=click.Choice(['c', 'a','b'])
                                 ,default='a'
                                 ,show_choices=True
                                 ).lower()
            if answer=='a':
                micc_logger.critical("Exiting.")
                return EXIT_CANCEL,extra_parameters
            elif answer=='b':
                micc_logger.warning(f"Making backup files in {project_path}:")
                for files in existing_files.values():
                    for src in files:
                        dst = src + '.bak'
                        shutil.copyfile(src, dst)
                        micc_logger.warning(f"     created backup file: {dst}")
                micc_logger.warning(f"Overwriting files ...")
            else:
                micc_logger.warning("Overwriting files ... (no backup)")
            micc_logger.warning('Overwriting files ... Done.')
            
    # Now we can safely overwrite pre-existing files.
    for template in templates:
        template = resolve_template(template)
        micc_logger.debug(f" . Expanding template {template} in project directory.")
        cookiecutter( template
                    , no_input=True
                    , overwrite_if_exists=True
                    , output_dir=output_dir
                    )
        # Clean up (see issue #7)
        cookiecutter_json = os.path.join(template, 'cookiecutter.json')
        os.remove(cookiecutter_json)

    # Clean up
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
        
    return 0,extra_parameters


def msg_NotAProjectDirectory(path):
    return f"Invalid project directory {path}."


def msg_CannotAddToSimpleProject(path):
    return f"Cannot add components to simple project ({path})."


def micc_create( project_name
               , output_dir
               , templates
               , micc_file
               , global_options
    ):
    """
    Create a new project skeleton for a general Python project. This is a
    Python package with a ``<package_name>/__init__.py`` structure, to wich 
    other modules and applications can be added.
    
    :param str project_name: the name of the project to be created.
    :param str output_dir: path where the project will be created. 
    :param str templates: ordered list of paths to a Cookiecutter_ template. a single 
        path is ok too.
    :param str micc_file: name of the json file with the default values in the template directories. 
    :param types.SimpleNamespace global_options: namespace object with options accepted by all micc commands. 
    """
    
    micc_console_loghandler.setLevel(verbosity_to_loglevel(global_options.verbose))
    if global_options.structure=='module':
        structure = f" ({project_name}.py)" 
    elif global_options.structure=='package':
        structure = f" ({project_name}/__init__.py)"
    else:
        structure = ''
    with utils.log(micc_logger.info, f"Creating Python package '{project_name}' as a {global_options.structure}{structure}"):

        output_dir = os.path.abspath(output_dir)
        project_path = os.path.join(output_dir,project_name) 
        assert not utils.is_project_directory(project_path),f"Project {project_path} exists already."
        # Prevent the creation of a project inside another project    
        # (add a 'dummy' leaf so the first directory checked is output_dir itself)
        if not global_options.allow_nesting:
            p = copy.copy(output_dir)
            while p:
                assert not utils.is_project_directory(p),f"Cannot create a project inside another project ({p})."
                p = utils.get_parent_dir(p)
            
        global_options.overwrite = False
     
        ( exit_code
        , template_parameters
        ) = expand_templates( templates, micc_file, project_path, global_options
                            # extra template parameters:
                            , project_name=project_name
                            )                
        if exit_code:
            return exit_msg(exit_code)

        with utils.log(micc_logger.info,"Creating git repository"):
            with utils.in_directory(os.path.join(output_dir,project_name)):
                cmds = [ ['git', 'init']
                       , ['git', 'add', '*']
                       , ['git', 'add', '.gitignore']
                       , ['git', 'commit', '-m', '"first commit"']
                       , ['git', 'remote', 'add', 'origin', f"https://github.com/{template_parameters['github_username']}/{project_name}"]
                       , ['git', 'push', '-u', 'origin', 'master']
                       ]
                for cmd in cmds:
                    cmdstr = ' '.join(cmd)
                    with utils.log(micc_logger.debug, f'> {cmdstr}', end_msg=None):
                        completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        if completed_process.stdout:
                            micc_logger.debug(' (stdout)\n' + completed_process.stdout.decode('ascii'))
                        if completed_process.stderr:
                            micc_logger.debug(' (stderr)\n' + completed_process.stderr.decode('ascii'))
    
    return 0


def micc_app( app_name
            , project_path
            , templates
            , micc_file
            , global_options
            ):
    """
    Micc app subcommand, add a console script (app) to the package. 
    
    :param str app_name: name of the applicatiom to be added.
    :param str project_path: path to the project where the app will be created. 
    :param str templates: ordered list of paths to a Cookiecutter_ template. a 
        single path is ok too.
    :param str micc_file: name of the json file with the default values in the 
        template directories. 
    :param types.SimpleNamespace global_options: namespace object with options 
        accepted by all micc commands.
    """
    project_path = os.path.abspath(project_path)
    assert utils.is_project_directory(project_path), msg_NotAProjectDirectory(project_path)
    assert not utils.is_simple_project(project_path), msg_CannotAddToSimpleProject(project_path)
    
    project_name = os.path.basename(project_path)
    micc_console_loghandler.setLevel(verbosity_to_loglevel(global_options.verbose))
    micc_logger.info(f"Creating app {app_name} in Python package {project_name}.")
    
    app_name = utils.verify_name(app_name, 'app')
    if not isinstance(app_name,str):
        # return exit_code
        return app_name
    
    ( exit_code
    , _ # template_parameters
    ) = expand_templates( templates, micc_file, project_path, global_options
                        # extra template parameters:
                        , project_name=project_name
                        , package_name=utils.convert_to_valid_module_name(project_name)
                        , app_name=app_name
                        )                
    if exit_code:
        micc_logger.critical(f"Exiting ({exit_code}) ...")
        return exit_code

    with in_directory(project_path):
        cli_app_name = 'cli_' + utils.convert_to_valid_module_name(app_name)
        package_name =          utils.convert_to_valid_module_name(project_name)
        
        # docs 
        with open('docs/api.rst',"r") as f:
            lines = f.readlines()
        has_already_apps = False
        for line in lines:
            has_already_apps = has_already_apps or line.startswith(".. include:: ../APPS.rst")
        if not has_already_apps:        
            with open('docs/api.rst',"w") as f:
                f.write(".. include:: ../APPS.rst\n\n")
                f.write(".. include:: ../API.rst\n\n")
        with open("APPS.rst","a") as f:
            f.write(f".. automodule:: {package_name}.{cli_app_name}\n")
            f.write( "   :members:\n\n")
        micc_logger.debug(f"INFO: documentation for application '{app_name}' added.")
        
        # pyproject.toml
        # in the [toolpoetry.scripts] add a line 
        #    {app_name} = "{package_name}:{cli_app_name}"
        tomlfile = TomlFile('pyproject.toml')
        content = tomlfile.read()
        content['tool']['poetry']['scripts'][app_name] = f'{package_name}:{cli_app_name}'
        tomlfile.write(content)

    micc_logger.debug(f"    application '{app_name}' added to pyproject.toml.")
    return 0


def micc_module_py( module_name
                  , project_path
                  , simple
                  , templates
                  , micc_file
                  , global_options
                  ):
    """
    ``micc module`` subcommand, add a Python module to the package. 
    
    :param str module_name: name of the module to be added.
    :param str project_path: path to the project where the app will be created. 
    :param bool simple: create simple (``<module_name>.py``) or general python module 
    :param str templates: ordered list of paths to a Cookiecutter_ template. a 
        single path is ok too.
    :param str micc_file: name of the json file with the default values in the 
        template directories. 
    :param types.SimpleNamespace global_options: namespace object with options 
        accepted by all micc commands.
    """
    if simple:
        module_type = f"{module_name}.py"
    else:
        module_type = f"{module_name}/__init__.py"
    micc_console_loghandler.setLevel(verbosity_to_loglevel(global_options.verbose))
    micc_logger.info(f"Creating python module {module_type} in Python package {project_name}.")
        
    global_options.simple = simple
    global_options.module_kind = 'python module'
    ( exit_code
    , template_parameters
    ) = expand_module_templates( 
            module_name, project_path,
            templates, micc_file, 
            global_options
        )
    if exit_code:
        micc_logger.critical(f"Exiting ({exit_code}) ...")
        return exit_code
    
    with in_directory(project_path):
        package_name = template_parameters['package_name']
        if not simple:
            module_py = os.path.join(project_path,package_name,module_name)
            simple_to_general(module_py)
        
        # docs
        with open("API.rst","a") as f:
            f.write(f"\n.. automodule:: {package_name}.{module_name}"
                     "\n   :members:\n\n"
                   )
        micc_logger.debug(f"    documentation entries for Python module {module_type} added.")
    return 0


def micc_module_f2py( module_name
                    , project_path
                    , templates
                    , micc_file
                    , global_options
                    ):
    """
    ``micc module --f2py`` subcommand, add a f2py module to the package. 
    
    :param str module_name: name of the module to be added.
    :param str project_path: path to the project where the app will be created. 
    :param str templates: ordered list of paths to a Cookiecutter_ template. a 
        single path is ok too.
    :param str micc_file: name of the json file with the default values in the 
        template directories. 
    :param types.SimpleNamespace global_options: namespace object with options 
        accepted by all micc commands.
    """

    global_options.module_kind = 'f2py module'
    
    ( exit_code
    , template_parameters
    ) = expand_module_templates( 
            module_name, project_path,
            templates, micc_file, 
            global_options
        )
    if exit_code:
        micc_logger.critical(f"Exiting ({exit_code}) ...")
        return exit_code
    
    project_name = template_parameters['project_name']
    package_name = template_parameters['package_name']
    with in_directory(project_path):
        # docs
        with open("API.rst","a") as f:
            f.write(f"\n.. include:: ../{package_name}/f2py_{module_name}/{module_name}.rst\n")
        micc_logger.warning(f"    Documentation template for f2py module '{module_name}' added.\n"
                            f"    Because recent versions of sphinx are incompatible with sphinxfortran,\n"
                            f"    you are required to enter the documentation manually in file\n"
                            f"    '{project_name}/{package_name}/{module_name}.rst' in reStructuredText format.\n"
                            f"    A suitable example is pasted.\n"
                           )
    micc_logger.info(f"F2py module {module_name} created.")
    return 0


def micc_module_cpp( module_name
                   , project_path
                   , templates
                   , micc_file
                   , global_options
                   ):
    """
    ``micc module --cpp`` subcommand, add a C++ module to the package. 
    
    :param str module_name: name of the module to be added.
    :param str project_path: path to the project where the app will be created. 
    :param str templates: ordered list of paths to a Cookiecutter_ template. a 
        single path is ok too.
    :param str micc_file: name of the json file with the default values in the 
        template directories. 
    :param types.SimpleNamespace global_options: namespace object with options 
        accepted by all micc commands.
    """
    global_options.module_kind = 'cpp_module'

    ( exit_code
    , template_parameters
    ) = expand_module_templates( 
            module_name, project_path,
            templates, micc_file, 
            global_options
        )
    if exit_code:
        msg = f"Exiting ({exit_code}) ..."
        if exit_code == EXIT_CANCEL:
            utils.warning(msg)
        else:
            utils.error(msg)
        return exit_code

    project_name = template_parameters['project_name']
    package_name = template_parameters['package_name']
    with in_directory(project_path):
        # docs
        with open("API.rst","a") as f:
            f.write(f"\n.. include:: ../{package_name}/cpp_{module_name}/{module_name}.rst\n")
        micc_logger.warning(f"    Documentation template for cpp module '{module_name}' added.\n"
                            f"    Because recent versions of sphinx are incompatible with sphinxfortran,\n"
                            f"    you are required to enter the documentation manually in file\n"
                            f"    '{project_name}/{package_name}/{module_name}.rst' in reStructuredText format.\n"
                            f"    A suitable example is pasted.\n"
                           )
    micc_logger.info(f"C++ module {module_name} created.")
    return 0


def expand_module_templates( module_name
                           , project_path
                           , templates
                           , micc_file
                           , global_options
                           ):
    """
    common part of 
    
    * ``micc_module_py``
    * ``micc_module_f2py``
    * ``micc_module_cpp``
    
    :param str module_name: name of the module to be added.
    :param str project_path: path to the project where the app will be created. 
    :param str templates: ordered list of paths to a Cookiecutter_ template. a 
        single path is ok too.
    :param str micc_file: name of the json file with the default values in the 
        template directories. 
    :param types.SimpleNamespace global_options: namespace object with options 
        accepted by all micc commands.
    """
    project_path = os.path.abspath(project_path)
    assert utils.is_project_directory(project_path), msg_NotAProjectDirectory(project_path)
    assert not utils.is_simple_project(project_path), msg_CannotAddToSimpleProject(project_path)
    
    project_name = os.path.basename(project_path)
    package_name = utils.convert_to_valid_module_name(project_name)
    module_name = utils.verify_name(module_name, 'module')
    if not isinstance(module_name,str):
        # return exit_code
        return module_name
        
    micc_console_loghandler.setLevel(verbosity_to_loglevel(global_options.verbose))
    
    if global_options.module_kind=='python module':
        if global_options.simple:
            module_structure = f"{module_name}.py"
        else:
            module_structure = f"{module_name}/__init__.py"
        micc_logger.info(f"Creating python module {module_structure} in Python package {project_name}.")
    elif global_options.module_kind=='f2py module':
        micc_logger.info(f"Creating f2py module {module_name} in Python package {project_name}\n"
                         f"    Source files in {project_name}/{package_name}/f2py_{module_name}."
                        )
    elif global_options.module_kind=='cpp_module':
        micc_logger.info(f"Creating C++ module {module_name} in Python package {project_name}\n"
                         f"    Source files in {project_name}/{package_name}/cpp_{module_name}."
                        )
    return expand_templates( templates, micc_file, project_path, global_options
                           # extra template parameters:
                           , project_name=project_name
                           , package_name=package_name
                           , module_name=module_name
                           )                


def micc_version( project_path
                , rule
                , global_options
                ):
    """
    Bump the version according to *rule*, and modify the pyproject.toml in 
    *project_path*.
    
    :param str project+path: path to a pyproject.toml file or its parent directory. 
    :param str rule: one of the valid arguments for the ``poetry version <rule>``
        command.
    """
    assert utils.is_project_directory(project_path),msg_NotAProjectDirectory(project_path)

    path_to_pyproject_toml = os.path.join(project_path,'pyproject.toml')
    pyproject_toml = toml.load(path_to_pyproject_toml)
    project_name    = pyproject_toml['tool']['poetry']['name']
    current_version = pyproject_toml['tool']['poetry']['version']
    package_name    = utils.convert_to_valid_module_name(project_name)

    micc_console_loghandler.setLevel(verbosity_to_loglevel(global_options.verbose))
    if rule is None:
        micc_logger.info(f"Current version: {project_name} v{current_version}")
    else:
        new_version = VersionCommand().increment_version(current_version, rule)
        msg = (f"Package {project_name} v{current_version}\n"
               f"Are you sure to move to v{new_version}'?")
        micc_logger.warning(msg)
        if not click.confirm("Confirm to continue",default=False):
            micc_logger.warning(f"EXIT_CANCELed: 'micc version {rule}'")
            return EXIT_CANCEL
        micc_logger.warning(f"{project_name} v{current_version} -> v{new_version}")

        # wrt poetry issue #1182. This issue is finally solved, boils down to 
        # tomlkit expecting the sections to appear grouped in pyproject.toml.
        # Our pyproject.toml contained a [tool.poetry.scripts] section AFTER 
        # the [build-system] section. when running E.g. poetry --version patch 
        # the version stringiest is NOT updated, but pyproject.toml is REWRITTEN
        # and now the [tool.poetry.scripts] section appears BEFORE the [build-system] 
        # section, nicely grouped with the other [tool.poetry.*] sections. Running 
        # poetry --version patch a second time then updates the version string 
        # correctly. 
        # This took me quite a few days find out ...
         
        # update version in pyproject.toml (using poetry code for good :)
        with utils.in_directory(project_path): 
            i = ArgvInput(['poetry','version',rule])
            app = Application()
            app._auto_exit = False
            app.run(i)       
        micc_logger.debug(f'    Updating : {path_to_pyproject_toml}')
            
        # update version in package
        if not utils.replace_version_in_file( os.path.join(project_path, package_name, '__init__.py')
                                            , current_version, new_version):
            if not utils.replace_version_in_file( os.path.join(project_path, package_name + '.py')
                                                , current_version, new_version):
                micc_logger.warning(f"Warning: No package {package_name}/__init__.py and no modute {package_name}.py found.")
    return 0


def micc_tag( project_path
            , global_options):
    """
    Create and push a version tag ``vM.m.p`` for the current version.
    
    :param str project_path: path to the project that must be tagged. 
    """
    assert utils.is_project_directory(project_path),msg_NotAProjectDirectory(project_path)
            
    path_to_pyproject_toml = os.path.join(project_path,'pyproject.toml')
    pyproject_toml = toml.load(path_to_pyproject_toml)
    project_name    = pyproject_toml['tool']['poetry']['name']
    current_version = pyproject_toml['tool']['poetry']['version']
    tag = f"v{current_version}"
    micc_console_loghandler.setLevel(verbosity_to_loglevel(global_options.verbose))
    
    with utils.in_directory(project_path):
    
        micc_logger.info(f"Creating git tag {tag} for project {project_name}")
        cmd = ['git', 'tag', '-a', tag, '-m', f'"tag version {current_version}"']
        micc_logger.debug(f"Running '{' '.join(cmd)}'")
        completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        micc_logger.debug(completed_process.stdout.decode('ascii'))
        if completed_process.stderr:
            micc_logger.critical(completed_process.stderr.decode('ascii'))

        micc_logger.debug(f"Pushing tag {tag} for project {project_name}")
        cmd = ['git', 'push', 'origin', tag]
        micc_logger.debug(f"Running '{' '.join(cmd)}'")
        completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        micc_logger.debug(completed_process.stdout.decode('ascii'))
        if completed_process.stderr:
            micc_logger.error(completed_process.stderr.decode('ascii'))
            
    micc_logger.info('Done.')
    return 0


def micc_build( project_path
              , module_to_build
              , soft_link
              , global_options
              ):
    """
    Build all binary extions, i.e. f2py modules and cpp modules.
    
    :param str module_to_build: name of the only module to build (the prefix cpp_ or f2py_ may be omitted)
    :param str project_path: path to the project that must be built.
    :param bool soft_link: if False, the binary extension modules are copied
        into the package directory. Otherwise a soft link is provided.
    """
    assert utils.is_project_directory(project_path),msg_NotAProjectDirectory(project_path)
    
    project_path = os.path.abspath(project_path)
    project_name = os.path.basename(project_path)
    package_name = utils.convert_to_valid_module_name(project_name)
    package_path = os.path.join(project_path,package_name)

    build_log = logging.getLogger(f"micc-build")
    build_log.setLevel(1)
    # add a handler that accepts messages based on verbosity and writes to stderr
    stderr_handler = logging.StreamHandler(sys.stderr)
    if global_options.verbose==0:
        stderr_handler.setLevel(logging.CRITICAL)
    elif global_options.verbose==1:
        stderr_handler.setLevel(logging.INFO)
    else:
        stderr_handler.setLevel(logging.DEBUG)
    build_log.addHandler(stderr_handler)
        
    # get extension for binary extensions (depends on OS and python version)
    extension_suffix = sysconfig.get_config_var('EXT_SUFFIX')

    my_env = os.environ.copy()
    dirs = os.listdir(package_path)
    for d in dirs:
        if os.path.isdir(os.path.join(package_path,d)) and (d.startswith("f2py_") or d.startswith("cpp_")):
            
            if module_to_build and not d.endswith(module_to_build): # build only this module
                continue

            logfile_name = f"micc-build-{d}.log"
            if os.path.exists(logfile_name):
                os.remove(logfile_name)
            # add a handler that accepts all messages and can be consulted later in case of problems
            logfile_handler = logging.FileHandler(logfile_name)
            logfile_handler.setLevel(logging.DEBUG) # let all messags pass.
            build_log.addHandler(logfile_handler)
 
            module_type,module_name = d.split('_',1)
            build_dir = os.path.join(package_path,d,'build_')
            build_log.info(f"\nBuilding {module_type} module {module_name} in directory '{build_dir}'\n    (see {logfile_name})\n")
            os.makedirs(build_dir,exist_ok=True)
            with utils.in_directory(build_dir):
                cextension = module_name + extension_suffix
                destination = os.path.join('..','..',cextension)
                cmds = [ ['cmake','CMAKE_BUILD_TYPE','=','RELEASE', '..']
                       , ['make']
                       ]
                if soft_link:
                    cmds.append(['ln', '-sf', os.path.abspath(cextension), destination])
                else:
                    if os.path.exists(destination):
                        build_log.debug(f">>> os.remove({destination})\n")
                        os.remove(destination)
                # WARNING: for these commands to work in eclipse, eclipse must have
                # started from the shell with the appropriate environment activated.
                # Otherwise subprocess starts out with the wrong environment. It 
                # may not pick the right Python version, and may not find pybind11.
                for cmd in cmds:
                    build_log.debug(f"> {' '.join(cmd)}")
                    completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=my_env)
                    build_log.debug(completed_process.stdout.decode('ascii'))
                    if completed_process.stderr:
                        build_log.error(completed_process.stderr.decode('ascii'))
                        build_log.removeHandler(logfile_handler)
                        break
                        
                if not soft_link:
                    build_log.debug(f">>> shutil.copyfile( '{cextension}', '{destination}' )\n")
                    shutil.copyfile(cextension, destination)
            build_log.removeHandler(logfile_handler)
    build_log.info('build finished.')
    return 0


def simple_to_general(module_py):
    """
    move file module.py to module/__init__.py
    """
    module_path = os.path.abspath( module_py.replace('.py','') )
    os.makedirs(module_path)
    src = os.path.join(module_path + '.py')
    dst = os.path.join(module_path, '__init__.py')
    shutil.move(src, dst)


def micc_convert_simple(project_path, overwrite, global_options):
    """
    Convert simple python package to general python package.
    
    :param str project_path: path to the project that must be tagged. 
    """
    project_path = os.path.abspath(project_path)
    project_name = os.path.basename(project_path)
    assert utils.is_project_directory(project_path),msg_NotAProjectDirectory(project_path)
    assert utils.is_simple_project(project_path), f"Project {project_name} is already a general Python package."
    
    if global_options.verbose>0:
        click.echo(f"Converting simple Python project {project_name} to general Python project.")
    global_options.overwrite = overwrite
    
    # add documentation files for general Python project
    tomlfile = TomlFile('pyproject.toml')
    content = tomlfile.read()

    ( exit_code
    , _ # template_parameters
    ) = expand_templates("template-package-general-docs", 'micc.json', project_path, global_options
                        # extra template parameters:
                        , project_name=project_name
                        , project_short_description=content['tool']['poetry']['description']
                        )                
    if exit_code:
        return exit_code
    
    package_name = utils.convert_to_valid_module_name(project_name)
    package_path = os.path.join(project_path,package_name)
    os.makedirs(package_path)
    src = os.path.join(project_path,package_name + '.py')
    dst = os.path.join(project_path,package_name, '__init__.py')
    shutil.move(src, dst)
    
    if global_options.verbose>0:
        click.echo("Done.")
    
    return 0
