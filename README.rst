micc
====

This is work in progress!

.. image:: https://img.shields.io/pypi/v/micc.svg
        :target: https://pypi.python.org/pypi/micc

.. image:: https://img.shields.io/travis/etijskens/micc.svg
        :target: https://travis-ci.org/etijskens/micc

.. image:: https://readthedocs.org/projects/micc/badge/?version=latest
        :target: https://micc.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Micc is a wrapper around Cookiecutter_. Whereas Cookiecutter_ asks 
the user to enter every template parameter or confirm the default,  
micc automatically accepts all the defaults and only prompts the user
when a parameter has no default.  

* Free software: MIT license.
* `Documentation <https://micc.readthedocs.io/en/latest/>`_.

Features
********

* The ``micc.json`` file is conceptually similar to cookiecutter.json, in that
  it describes a dict whose keys are the names of the Cookiecutter_ template 
  variables, but the corresponding values are dicts describing the
  ``click.prompt()`` parameters use when de user is prompted for input.
* TODO

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
