# -*- coding: utf-8 -*-
"""
Module et_micc.db
=================

This submodule implements the database that is needed for safe refactoring of
submodules and CLIs.
"""

class Database:
    def __init__(self,project):
        self.project = project

    def add_app(self):
        """Database action when an app (CLI) is added."""

    def add_python_module(self):
        """Database action when a python module is added."""

    def add_f90_module(self):
        """Database action when a f90 module is added."""

    def add_cpp_module(self):
        """Database action wehn a C++ module is added."""

    def remove_app(self):
        """Database action when an app (CLI) is removed."""

    def remove_python_module(self):
        """Database action when a python module is removed."""

    def remove_f90_module(self):
        """Database action when a f90 module is removed."""

    def remove_cpp_module(self):
        """Database action wehn a C++ module is removed."""

    def rename_app(self):
        """Database action when an app (CLI) is renamed."""

    def rename_python_module(self):
        """Database action when a python module is renamed."""

    def rename_f90_module(self):
        """Database action when a f90 module is renamed."""

    def rename_cpp_module(self):
        """Database action wehn a C++ module is renamed."""

