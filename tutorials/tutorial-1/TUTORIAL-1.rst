
Tutorial 1: a simple project
============================

Let's start with a simple problem: a Python module that computes the 
`dot product of two arrays <https://en.wikipedia.org/wiki/Dot_product>`_. 
This not a very rewarding goal, as there are already many Python packages, 
e.g. Numpy_, that solve this problem in an elegant and efficient way. 

However, because the dot product is such a simple concept in linear algebra, 
it allows us to illustrate the usefulness of Python as a language for High 
Performance Computing, as well as the capabilities of 
`micc <https://et-micc.readthedocs.io/en/latest/>`_.

Here are a number of interesting links covering Python as a language for
High Performance Computing:

* `Performance Python: Seven Strategies for Optimizing Your Numerical Code <https://www.youtube.com/watch?v=zQeYx87mfyw>`_
* `High performance Python 1 <http://www.admin-magazine.com/HPC/Articles/High-Performance-Python-1>`_
* `High performance Python 2 <http://www.admin-magazine.com/HPC/Articles/High-Performance-Python-2>`_
* `High performance Python 3 <http://www.admin-magazine.com/HPC/Articles/High-Performance-Python-3>`_
* `High performance Python 4 <http://www.admin-magazine.com/HPC/Articles/High-Performance-Python-4>`_
* `Why you should use Python for scientific research <https://developer.ibm.com/dwblog/2018/use-python-for-scientific-research/>`_

Development environment
-----------------------

For Python development, we highly recommend to set up your development environment as described in 
`My Python Development Environment <https://jacobian.org/2019/nov/11/python-environment-2020/>`_
by Jacob Kaplan-Moss. We will assume that this is indeed the case for all tutorials here. In 
particular:

* We are using `pyenv <https://github.com/pyenv/pyenv>`_ to manage different Python versions on 
  our system.
* We use `pipx <https://github.com/pipxproject/pipx/>`_ to install applications like  Micc_ system-wide with their own 
  virtual environment.
* `Poetry <https://poetry.eustace.io/docs/pyproject/>`_ is used to set up virtual environments for the projects we are working, for managing
  their dependencies and for publishing them to PyPI_. 
* Micc_ is used to set up the project structure, as the basis of everything that will be described
  in the tutorials below.
* For Micc_ projects with binary extension the necessary compilers must be installed on the system.
  In addition `CMake <https://cmake.org>`_ must installed, either system-wide, or in the virtual environmnet of your project. 
  (Currently, Poetry_ has some issues with installing CMake_ in a cross-platform setting. That is 
  expected to change in the future at which point CMake_ will automatically be added as a dependency
  of Micc_ projects with binary extension modules compiled from C++ code.)  

.. note:: 
   
   Poetry_ is a recent tool that has not yet matured. One of the areas where it is still
   quite rough around the edges is its treatment of pyenv_ python versions, and pyenv-virtualenv.
   At the time of writing, poetry_ does not recognize these, but that will 
   probably change in the future as poetry_ matures. 
   
   We solve this problem by installing poetry in every pyenv Python version, e.g.
   
   .. code-block:: bash
   
      > pyenv install 3.8.0
      ...
      > pyenv global 3.8.0
      > pip install poetry==1.0.0b5 
      
   This installs poetry_ in the pyenv Python version 3.8.0. This procedure must be repeated with
   every Python version you want to use with Poetry_. E.g., if we want to use Python 3.8.0 for project
   *foo*:
   
   .. code-block:: bash
   
      > cd path/to/foo
      > pyenv local 3.8.0
      
   When you now call any poetry command in the :file:`foo` directory it will the the poetry installed
   with Python 3.8.0. E.g., ``poetry install`` will create a virtual environment using Python 3.8.0 
   and install the project's dependencies in that environment.
  
     