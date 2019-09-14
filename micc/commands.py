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
from types import SimpleNamespace
#===============================================================================
# logging commmands to follow cookiecutter.generate
dbgcc = False 
if dbgcc:
    import logging,sys
    logger = logging.getLogger('cookiecutter.generate')
    logger.setLevel(9)
    stderr_hand = logging.StreamHandler(sys.stderr)
    stderr_hand.setLevel(9) 
    logger.addHandler(stderr_hand)    
#===============================================================================
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
#===============================================================================
def apply_templates(templates, micc_file, project_path, global_options, **kwargs):
    """
    Expand a list of cookiecutter templates in directory ``project_path``.
    """
    if not isinstance(templates, list):
        templates = [templates]
    extra_parameters = kwargs
    
    # list existing files that would be overwritten
    all_dirs = [] 
    existing_files = {}
    for template in templates:
        template = resolve_template(template)             
        template_parameters = utils.get_template_parameters( template, micc_file, global_options
                                                           , **extra_parameters
                                                           )  
        extra_parameters = template_parameters
        # write a cookiecutter.json file in the cookiecutter template directory
        cookiecutter_json = os.path.join(template, 'cookiecutter.json')
        with open(cookiecutter_json,'w') as f:
            json.dump(template_parameters, f, indent=2)
        
        # run cookiecutter in a temporary directory to check if there are any
        # existing project files that woud be overwritten.
        with in_directory(os.path.join(project_path,'..')):
            # expand the Cookiecutter template in a temporary directory,
            tmp = '_cookiecutter_tmp_'
            if os.path.exists(tmp):
                shutil.rmtree(tmp)
            os.makedirs(tmp, exist_ok=True)
            cookiecutter( template
                        , no_input=True
                        , overwrite_if_exists=True
                        , output_dir=tmp
                        )
            # find out if there are any files that would be overwritten.
            os_name = platform.system()
            for root, dirs, files in os.walk(tmp):
                if root==tmp:
                    continue
                else:
                    root2 = os.path.join(*root.split(os.sep)[1:])
                for d in dirs:
                    all_dirs.append(os.path.join(root2,d))
                for f in files:
                    if os_name=="Darwin" and f==".DS_Store":
                        continue
                    file = os.path.join(root2,f)
#                     print('FILE',file, 'exists =', os.path.exists(file))
                    if os.path.exists(file):                            
                        if not template in existing_files:
                            existing_files[template] = []
                        existing_files[template].append(file)
    
    if existing_files:
        click.echo("The following files will be overwritten:")
        for template, files in existing_files.items():
            t = os.path.basename(template)
            for f in files:
                click.echo(f"    {t} : {f}")
        answer = click.prompt("Press 'c' to continue\n"
                              "      'a' to abort\n"
                              "      'b' to keep the original files with .bak extension\n"
                             ,type=click.Choice(['c', 'a','b'])
                             ,default='a'
                             ,show_choices=True
                             ).lower()
        if answer=='a':
            print('abort')
            exit(CANCEL)
        elif answer=='b':
            print('make .bak files')
        exit(CANCEL)
        
        
    for template in templates:
        cookiecutter( template
                    , no_input=True
                    , overwrite_if_exists=True
                    , output_dir=project_path
                    )
        # Clean up (see issue #7)
        os.remove(cookiecutter_json)
    return template_parameters
#===============================================================================
def _msg_NotAProjectDirectory(path):
    return f"Invalid project directory {path}."
#===============================================================================
_global_options = SimpleNamespace(verbose=1)
CANCEL = -1
#===============================================================================
def micc_create( project_name
               , output_dir
               , templates
               , micc_file
               , project_type
               , global_options=_global_options
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
    if global_options.verbose>0:
        click.echo(f"Creating {project_type} Python package {project_name}")
        if global_options.verbose>1:
            if project_type == 'simple':
                click.echo(f"    ( structure: {project_name}/{utils.python_name(project_name)}.py )")
            else:
                click.echo(f"    ( structure: {project_name}/{utils.python_name(project_name)}/__init__.py )")

    output_dir = os.path.abspath(output_dir)
    
    # Prevent the creation of a project inside another project    
    # (add a 'dummy' leaf so the first directory checked is output_dir itself)
    project_path = os.path.join(output_dir,project_name) 
    p = copy.copy(project_path)
    while p:
        assert not utils.is_project_directory(p),f"Cannot create a project inside another project ({p})."
        p = utils.get_parent_dir(p)
        
    template_parameters = apply_templates( templates, micc_file, project_path, global_options
                                         # template parameters to be added: 
                                         , project_name=project_name
                                         )                
        
    with utils.in_directory(os.path.join(output_dir,project_name)):
        cmds = [ ['git', 'init']
               , ['git', 'add', '*']
               , ['git', 'add', '.gitignore']
               , ['git', 'add', '.flake8']
               , ['git', 'commit', '-m', '"first commit"']
               , ['git', 'remote', 'add', 'origin', f"https://github.com/{template_parameters['github_username']}/{project_name}"]
               , ['git', 'push', '-u', 'origin', 'master']
               ]
        for cmd in cmds:
            click.echo('(micc create) > ' + ' '.join(cmd))
            completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            click.echo(completed_process.stdout)
        if completed_process.stderr:
            click.echo(completed_process.stderr)
    return 0
#===============================================================================
def micc_app( app_name
            , project_path
            , templates
            , micc_file
            , overwrite=False
            , global_options=_global_options
            ):
    """
    Micc app subcommand, add a console script (app) to the package. 
    
    :param str app_name: name of the applicatiom to be added.
    :param str project_path: path to the project where the app will be created. 
    :param str templates: ordered list of paths to a Cookiecutter_ template. a single 
        path is ok too.
    :param str micc_file: name of the json file with the default values in the template directories. 
    :param bool overwrite: allow overwriting exixting files.
    :param types.SimpleNamespace global_options: namespace object with options accepted by all micc commands.
    """
    assert utils.is_project_directory(project_path),_msg_NotAProjectDirectory(project_path)

    project_name = os.path.basename(project_path)
    if global_options.verbose>0:
        click.echo(f"Creating app {app_name} in Python package {project_name}")
    

    template_parameters = apply_templates( templates, micc_file, project_path, global_options
                                         # template parameters to be added: 
                                         , app_name=app_name
                                         )                
    app_name = template_parameters['app_name']

    exit_code = utils.generate( project_path
                              , template
                              , template_parameters
                              , overwrite
                              , quiet=global_options.quiet
                              )
    if exit_code:
        return exit_code

    with in_directory(project_path):
        cli_app_name = 'cli_' + utils.python_name(app_name)
        package_name =          utils.python_name(project_name)
        
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
        if global_options.verbose:
            utils.info(f"INFO: documentation for application '{app_name}' added.")
        
        # pyproject.toml
        # in the [toolpoetry.scripts] add a line 
        #    {app_name} = "{package_name}:{cli_app_name}"
        tomlfile = TomlFile('pyproject.toml')
        content = tomlfile.read()
        content['tool']['poetry']['scripts'][app_name] = f'{package_name}:{cli_app_name}'
        tomlfile.write(content)
        if global_options.verbose:
            utils.info(f"INFO: application '{app_name}' added to pyproject.toml.")
    return 0
#===============================================================================
INFO = {'fg':'green'}
#===============================================================================
def micc_module( module_name
               , project_path='.'
               , overwrite=False
               , global_options=_global_options
               , template='micc-module', micc_file='micc.json'
               ):
    """
    Micc module subcommand, add a module to the package. 
    
    :param str module_name: name of the module.
    :param str project_path: if empty, use the current working directory
    """
    assert utils.is_project_directory(project_path),_msg_pyproject_toml_missing(project_path)

    project_path = os.path.abspath(project_path)
    project_name = os.path.basename(project_path)     
    template = resolve_template(template)
    template_parameters = utils.get_template_parameters( template, micc_file
                                                       , module_name=module_name
                                                       , project_name=project_name
                                                       )   
    module_name = template_parameters['module_name']
    template_parameters['module_kind'] = 'python'
    
    py_name = utils.python_name(module_name)
    if not py_name==module_name:
        msg  = f"Not a valid module name: {module_name}\n"
        msg += f"Use {py_name} instead?"
        if not click.confirm(msg):
            click.echo(f"Canceled: 'micc module {module_name}'")
            return CANCEL
        else:
            module_name = py_name
            template_parameters['module_name'] = py_name
           
    exit_code = utils.generate( project_path
                              , template
                              , template_parameters
                              , overwrite
                              , quiet=global_options.quiet
                              )
    if exit_code:
        return exit_code
    
    with in_directory(project_path):        
        # docs
        package_name = template_parameters['project_name'].lower().replace('-', '_')
        with open("API.rst","a") as f:
            f.write(f"\n.. automodule:: {package_name}.{module_name}"
                     "\n   :members:\n\n"
                   )
        if global_options.verbose:
            utils.info(f"INFO: documentation for Python module '{module_name}' added.")
    return 0
#===============================================================================
def micc_module_f2py( module_name
                    , project_path='.'
                    , overwrite=False
                    , global_options=_global_options
                    , template='micc-module-f2py', micc_file='micc.json'
                    ):
    """
    Micc module subcommand, add a f2py module to the package. 
    
    :param str module_name: name of the module.
    :param str project_path: if empty, use the current working directory
    """
    assert utils.is_project_directory(project_path),_msg_pyproject_toml_missing(pyproject_path)

    project_path = os.path.abspath(project_path)
    project_name = os.path.basename(project_path)        
    template = resolve_template(template)
    template_parameters = utils.get_template_parameters( template, micc_file
                                                       , module_name=module_name
                                                       , project_name=project_name
                                                       )
    module_name = template_parameters['module_name']
    template_parameters['module_kind'] = 'f2py'
    template_parameters['path_to_cmake_tools'] = utils.path_to_cmake_tools()
                
    py_name = utils.python_name(module_name)
    if not py_name==module_name:
        msg  = f"Not a valid module name: {module_name}\n"
        msg += f"Use {py_name} instead?"
        if not click.confirm(msg):
            click.echo(f"Canceled: 'micc module {module_name}'")
            return CANCEL
        else:
            module_name = py_name
            template_parameters['module_name'] = py_name

    exit_code = utils.generate( project_path
                              , template
                              , template_parameters
                              , overwrite
                              , quiet=global_options.quiet
                              )
    if exit_code:
        return exit_code
    
    with in_directory(project_path):
        # docs
        package_name = template_parameters['project_name'].lower().replace('-', '_')
        with open("API.rst","a") as f:
            f.write(f"\n.. include:: ../{package_name}/f2py_{module_name}/{module_name}.rst\n")
        if global_options.verbose:
            utils.info(f"INFO: Documentation template for f2py module '{module_name}' added.\n"
                       f"      Because recent versions of sphinx are incompatible with sphinxfortran,\n"
                       f"      you are required to enter the documentation manually in file\n"
                       f"      '{project_name}/{package_name}/{module_name}.rst' in reStructuredText format.\n"
                       f"      A suitable example is pasted.\n"
                      )
    return 0
#===============================================================================
def micc_module_cpp( module_name
                   , project_path='.'
                   , overwrite=False
                   , global_options=_global_options
                   , template='micc-module-cpp', micc_file='micc.json'
                   ):
    """
    Micc module subcommand, add a C++ module to the package. 
    
    :param str module_name: name of the module.
    :param str project_path: if empty, use the current working directory
    """
    assert utils.is_project_directory(project_path),_msg_pyproject_toml_missing(pyproject_path)

    project_path = os.path.abspath(project_path)
    project_name = os.path.basename(project_path)        
    template = resolve_template(template)
    template_parameters = utils.get_template_parameters( template, micc_file
                                                       , module_name=module_name
                                                       , project_name=project_name
                                                       )
    module_name = template_parameters['module_name']
    template_parameters['module_kind'] = 'cpp'
    
    py_name = utils.python_name(module_name)
    if not py_name==module_name:
        msg  = f"Not a valid module name: {module_name}\n"
        msg += f"Use {py_name} instead?"
        if not click.confirm(msg):
            click.echo(f"Canceled: 'micc module {module_name}'")
            return CANCEL
        else:
            module_name = py_name
            template_parameters['module_name'] = py_name

    exit_code = utils.generate( project_path
                              , template
                              , template_parameters
                              , overwrite
                              , quiet=global_options.quiet
                              )
    if exit_code:
        return exit_code

    with in_directory(project_path):
        # docs
        package_name = template_parameters['project_name'].lower().replace('-', '_')
        with open("API.rst","a") as f:
            f.write(f"\n.. include:: ../{package_name}/cpp_{module_name}/{module_name}.rst\n")
        if global_options.verbose:
            utils.info(f"INFO: Documentation template for cpp module '{module_name}' added.\n"
                       f"      Because recent versions of sphinx are incompatible with sphinxfortran,\n"
                       f"      you are required to enter the documentation manually in file\n"
                       f"      '{project_name}/{package_name}/{module_name}.rst' in reStructuredText format.\n"
                       f"      A suitable example is pasted.\n"
                      )
    return 0
#===============================================================================
def micc_version(project_path='.', rule=None, global_options=_global_options):
    """
    Bump the version according to *rule*, and modify the pyproject.toml in 
    *project_path*.
    
    :param str project+path: path to a pyproject.toml file or its parent directory. 
    :param str rule: one of the valid arguments for the ``poetry version <rule>``
        command.
    """
    assert utils.is_project_directory(project_path),_msg_pyproject_toml_missing(pyproject_path)

    path_to_pyproject_toml = os.path.join(project_path,'pyproject.toml')
    pyproject_toml = toml.load(path_to_pyproject_toml)
    project_name    = pyproject_toml['tool']['poetry']['name']
    current_version = pyproject_toml['tool']['poetry']['version']
    package_name    = utils.python_name(project_name)

    if rule is None:
        click.echo(f"Current version: {project_name} v{current_version}")
    else:
        new_version = VersionCommand().increment_version(current_version, rule)
        if not global_options.quiet:
            msg = f"Package {project_name} v{current_version}\n"\
                  f"Are you sure to move to v{new_version}'?"
            if not click.confirm(msg,default=False):
                click.echo(f"Canceled: 'micc version {rule}'")
                return CANCEL
            else:
                click.echo("Proceeding...")                    
        else:
            click.echo(f"{project_name} v{current_version} -> v{new_version}")

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
        click.echo(f'    Updating : {path_to_pyproject_toml}')
            
        # update version in package
        if not utils.replace_version_in_file( os.path.join(project_path, package_name, '__init__.py')
                                            , current_version, new_version):
            if not utils.replace_version_in_file( os.path.join(project_path, package_name + '.py')
                                                , current_version, new_version):
                click.echo(f"Warning: No package {package_name}/__init__.py and no modute {package_name}.py found.")
    return 0
#===============================================================================
def micc_tag(project_path='.', global_options=_global_options):
    """
    Create and push a version tag ``vM.m.p`` for the current version.
    
    :param str project_path: path to the project that must be tagged. 
    """
    assert utils.is_project_directory(project_path),_msg_pyproject_toml_missing(pyproject_path)
    
    # There is not really a reason to be careful when creating a tag
    # if not global_options.quiet:
    #     project_name, version = utils.get_name_version(project_path)
    #     msg = f"Are you sure to create tag 'v{version}' for project '{project_name}'?"
    #     if not click.confirm(msg,default=False):
    #         click.echo("Canceled: 'micc tag'")
    #         return -1
    #     else:
    #         click.echo("Proceeding...")
        
    with utils.in_directory(project_path):
        path_to_pyproject_toml = os.path.join(project_path,'pyproject.toml')
        pyproject_toml = toml.load(path_to_pyproject_toml)
        project_name    = pyproject_toml['tool']['poetry']['name']
        current_version = pyproject_toml['tool']['poetry']['version']

        click.echo(f"Creating tag {current_version} for project {project_name}")
        cmd = ['git', 'tag', '-a', f'v{current_version}', '-m', f'"tag version {current_version}"']
        if global_options.verbose:
            click.echo(f"Running '{' '.join(cmd)}'")
        completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        click.echo(completed_process.stdout)
        if completed_process.stderr:
            click.echo(completed_process.stderr)

        click.echo(f"Pushing tag {current_version} for project {project_name}")
        cmd = ['git', 'push', 'origin', f'v{current_version}']
        if global_options.verbose:
            click.echo(f"Running '{' '.join(cmd)}'")
        completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        click.echo(completed_process.stdout)
        if completed_process.stderr:
            click.echo(completed_process.stderr)
    return 0
#===============================================================================
def micc_build(project_path='.', soft_link=False, global_options=_global_options):
    """
    Build all binary extions, i.e. f2py modules and cpp modules.
    
    :param str project_path: path to the project that must be tagged. 
    """
    assert utils.is_project_directory(project_path),_msg_pyproject_toml_missing(pyproject_path)
    
    path_to_pyproject_toml = os.path.join(project_path,'pyproject.toml')
    pyproject_toml = toml.load(path_to_pyproject_toml)
    project_name   = pyproject_toml['tool']['poetry']['name']
#     current_version = pyproject_toml['tool']['poetry']['version']
    package_name    = utils.python_name(project_name)
    package_dir = os.path.join(project_path,package_name)

    my_env = os.environ.copy()
    extension_suffix = sysconfig.get_config_var('EXT_SUFFIX')
    
    dirs = os.listdir(package_dir)
    for d in dirs:
        if os.path.isdir(os.path.join(package_dir,d)) and (d.startswith("f2py_") or d.startswith("cpp_")):
            module_type,module_name = d.split('_',1)
            click.echo(f"\nBuilding {module_type} {module_name}:\n")
            build_dir = os.path.join(package_dir,d,'build_')
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
                        click.echo(f"micc build : {module_type} >>> os.remove({destination})\n")
                        os.remove(destination)
                # WARNING: for these commands to work in eclipse, eclipse must have
                # started from the shell with the appropriate environment activated.
                # Otherwise subprocess starts out with the wrong environment. It 
                # may not pick the right Python version, and may not find pybind11.
                for cmd in cmds:
                    click.echo(f'micc build : {module_type} > ' + ' '.join(cmd))
                    completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=my_env)
                    click.echo(completed_process.stdout)
                    if completed_process.stderr:
                        click.echo(completed_process.stderr)
                        break
                if not soft_link:
                    click.echo(f"micc build : {module_type} >>> shutil.copyfile({cextension}, {destination})\n")
                    shutil.copyfile(cextension, destination)
#                 click.echo
    
    return 0
#===============================================================================
def extend_doc(project_path):
    """
    """
    # this may give troubel if the .rst files in doxs have been touched but
    # that is not meant to happen. Changes should have been made to 
    #     <project_name>/README.rst and 
    #     <project_name>/API.rst and 
    template = 'micc-package'
    template = resolve_template(template)
    template_docs_dir = os.path.join(template,'{{cookiecutter.project_name}}','docs')

    click.echo(f"extending documentation of project:\n              {project_path}")

    files = os.listdir(template_docs_dir)
    for file in files:
        if file.endswith('.rst'):
            s = os.path.join(template_docs_dir,file)
            d = os.path.join(project_path,'docs',file)
            if os.path.exists(d):
                click.echo(f"> Overwriting {d}")
            else:
                click.echo(f"> Adding      {d}")                
            shutil.copyfile(s,d)

    template_dir = os.path.abspath(os.path.join(template_docs_dir,'..'))
    files = os.listdir(template_dir)
    for file in files:
        if file.endswith('.rst'):
            s = os.path.join(template_docs_dir,file)
            d = os.path.join(project_path,'docs',file)
            if not os.path.exists(d):
                click.echo(f"> Adding      {d}")                
            shutil.copyfile(s,d)
#===============================================================================
def micc_convert_simple(project_path='.', global_options=_global_options):
    """
    Convert simple python package to general python package.
    
    :param str project_path: path to the project that must be tagged. 
    """
    assert utils.is_project_directory(project_path),_msg_pyproject_toml_missing(project_path)
    path_to_pyproject_toml = os.path.join(project_path,'pyproject.toml')
    pyproject_toml = toml.load(path_to_pyproject_toml)
    project_name = pyproject_toml['tool']['poetry']['name']
    package_name = utils.python_name(project_name)
    assert utils.is_simple_project(project_path), f"Project {project_name} is not a simple python package. (missing '{package_name}.py')"

    add_extra_doc(os.path.abspath(project_path))
#         with utils.in_directory(project_name):
            
        
#===============================================================================
