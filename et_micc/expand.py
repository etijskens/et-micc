# -*- coding: utf-8 -*-
"""
Module et_micc.expand
=====================

Helper functions for dealing with *Cookiecutter* templates.
"""

import os, shutil, platform
from pathlib import Path
import json

import click
from cookiecutter.main import cookiecutter

import et_micc.logger

EXIT_OVERWRITE = -3


def resolve_template(template):
    """Compose the absolute path of a template."""
    
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

    ty = None
    for parameter,description in preferences.items():
        if not description['default'].startswith('{{ '):
            if 'type' in description:
                ty = description['type']
                description['type'] = eval(ty)
            answer = click.prompt(**description)
            if ty:
                # set the string back
                description['type'] = ty
            preferences[parameter]['default'] = answer
            
    with micc_file.open(mode='w') as f:
        json.dump(preferences, f, indent=2)
        
    return preferences


def get_preferences(micc_file):
    """Get the preferences from *micc_file*.
    
    (This function requires user interaction if no *micc_file* was provided!)

    :param Path micc_file: path to a json file.
    """
    if micc_file.samefile('.'):
        # There is no et_micc file with preferences yet.
        dotmicc = Path().home() / '.et_micc'
        dotmicc.mkdir(exist_ok=True)
        dotmicc_miccfile = dotmicc / 'micc.json'
        if dotmicc_miccfile.exists():
            preferences = get_preferences(dotmicc_miccfile)
        else:
            preferences = None
            # micc_file_template = Path(__file__).parent / 'micc.json'
            # shutil.copyfile(str(micc_file_template),str(dotmicc_miccfile))
            # preferences = set_preferences(dotmicc_miccfile)
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
    
    
def expand_templates(options):
    """Expand a list of cookiecutter :py:obj:`templates` in directory :py:obj:`project_path`. 

    Expanding templates may require overwriting pre-existing files. *Micc* handles this
    situation in different ways:

    * If :py:obj:`options.overwrite` equals :py:const:`False` the exansion will
      fail without overwriting any pre-existing files. The project is not modified. A
      warning is produced. This is the default. To continue, rerun the command with one
      of the two options below.
    * If :py:obj:`options.overwrite` equals :py:const:`True` the exansion will
      overwrite any pre-existing files without backup, and produce a warning, listing
      the overwritten files.
    * If :py:obj:`options.backup` equals :py:const:`True` pre-existing files
      will be backed up (.bak) before the new files are expanded. If anything went
      wrong, you can inspect the backup files, and correct the errors manually.
      
    :param types.SimpleNamespace options: namespace object with
        options accepted by et_micc commands. Relevant attributes are 
        
        * templates: ordered list of (paths to) cookiecutter templates that 
          will be expanded as they appear. The template parameters are propagated 
          from each template to the next.
        * **verbosity**
        * **project_path**: Path to the project on which the command operates.
        * **template_parameters**: extra template parameters not read from *micc_file*
    """
    templates = options.templates
    if not isinstance(templates, list):
        templates = [templates]
    project_path = options.project_path
    project_path.mkdir(parents=True, exist_ok=True)
    output_dir = project_path.parent
    micc_logger = options.logger

    # list existing files that would be overwritten if options.overwrite==True
    existing_files = {}
    for template in templates:
        template = resolve_template(template)             
        # write a cookiecutter.json file in the cookiecutter template directory
        cookiecutter_json = template / 'cookiecutter.json'
        with open(cookiecutter_json,'w') as f:
            json.dump(options.template_parameters, f, indent=2)
        
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
            if options.backup:
                micc_logger.warning("Pre-existing files that will be backed up ('--backup' specified):\n")
                micc_logger.indent(2)
                for files in existing_files.values():
                    for src in files:
                        src = str(src)
                        dst = src + '.bak'
                        shutil.copyfile(src, dst)
                        micc_logger.warning(f"{src} -> {dst}")
                micc_logger.dedent()
                
            elif not options.overwrite:
                micc_logger.warning("Pre-existing files that would be overwritten:\n")
                micc_logger.indent(2)
                for files in existing_files.values():
                    for src in files:
                        micc_logger.warning(str(src))
                micc_logger.dedent()
                click.secho("Aborting because 'overwrite==False'.\n"
                            "  Rerun the command with the '--backup' flag to first backup these files (*.bak).\n"
                            "  Rerun the command with the '--overwrite' flag to overwrite these files without backup.\n"
                            "Aborting."
                           , fg='bright_red'
                           )
                return EXIT_OVERWRITE
            else:
                micc_logger.warning(f"'--overwrite' specified: pre-existing files will be overwritten WITHOUT backup:\n")
                for files in existing_files.values():
                    for src in files:
                        micc_logger.warning(f"     overwriting {src}")
                
    # Now we can safely overwrite pre-existing files.
    micc_logger.debug(f"Expanding templates using these parameters:\n{json.dumps(options.template_parameters,indent=2)}")
    for template in templates:
        template = resolve_template(template)
        micc_logger.debug(f"Expanding template {template}.")
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


#eof