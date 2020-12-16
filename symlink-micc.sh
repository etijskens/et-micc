#!/bin/bash

# Execute this script in a micc project to test micc and micc-build on the current project.
# Any changes in:
#   . ~/software/dev/workspace/et-micc/et_micc/
#   . ~/software/dev/workspace/et-micc-build/et_micc_build/
# will be immediately visible in the project's virtual environment.

# Behaviour: The script replaces the installed python packages et_micc and et_micc_build,
# if present, with symbolic links to ~/software/dev/workspace/et-micc/et_micc/ and
# ~/software/dev/workspace/et-micc-build/et_micc_build/, respectively.
# If the current project is et_micc or et_micc_build, the script prints an error\
# message and exits.


current_project=$(micc info --name)

if [[ "$current_project" = et_micc ]]
then
  echo "ERROR: it is not allowed to do this in project et_micc"
  exit 1
fi

if [[ "$current_project" = et_micc_build ]]
then
  echo "ERROR: it is not allowed to do this in project et_micc_build"
  exit 1
fi

# The location of the et-micc and et-micc-build projects
# (adjust this to your needs):
workspace="/Users/etijskens/software/dev/workspace"

site_packages=$(python -c 'import site; print(site.getsitepackages()[0])')
cd ${site_packages}
#echo "site-packages = ${site_packages}"

if [[ -d et_micc ]]
then
  echo "sym-linking ~/software/dev/workspace/et-micc/et_micc/"
  rm -rf et_micc
  ln -s ${workspace}/et-micc/et_micc/
else
  echo "WARNING: micc is not installed in the current project, hence it cannot be sym-linked for testing."
  echo "         You may want to run 'pip install et-micc' first, and rerun the script."
fi

if [[ -d et_micc_build ]]
then
  echo "sym-linking ~/software/dev/workspace/et-micc-build/et_micc_build/"
  rm -rf et_micc_build
  ln -s ${workspace}/et-micc-build/et_micc_build/
else
  echo "WARNING: micc-build is not installed in the current project, hence it cannot be sym-linked for testing."
  echo "         You may want to run 'pip install et-micc-build' first, and rerun the script."
fi
