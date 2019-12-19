2.5 Documenting binary extension modules
----------------------------------------

For Python modules the documentation is automatically extracted from the doc-strings 
in the module. However, when it comes to documenting binary extension modules, this
does not seem a good option. Ideally, the source files :file:`ET-dot/et_dot/f2py_dotf/dotf.f90` 
amnd :file:`ET-dot/et_dot/cpp_dotc/dotc.cpp` should document the Fortran functions and 
subroutines, and C++ functions, respectively, rahter than the Python interface. Yet 
from the perspective of ET-dot being a Python project, the users is only interested
in the documentation of the Python interface to those functions and subroutines. 
Therefore, micc_ requires you to document the Python interface in separate :file:`.rst`
files:

* :file:`ET-dot/et_dot/f2py_dotf/dotf.rst` 
* :file:`ET-dot/et_dot/cpp_dotc/dotc.rst`

Here are the contents, respectively, for :file:`ET-dot/et_dot/f2py_dotf/dotf.rst`:

.. code-block:: rst
   
   Module et_dot.dotf
   ******************
   
   Module :py:mod:`dotf` built from fortran code in :file:`f2py_dotf/dotf.f90`.
   
   .. function:: dotf(a,b)
      :module: et_dot.dotf
      
      Compute the dot product of *a* and *b* (in Fortran.)
   
      :param a: 1D Numpy array with ``dtype=numpy.float64``
      :param b: 1D Numpy array with ``dtype=numpy.float64``
      :returns: the dot product of *a* and *b*
      :rtype: ``numpy.float64``

and for :file:`ET-dot/et_dot/cpp_dotc/dotc.rst`:

.. code-block:: rst
   
   Module et_dot.dotc
   ******************
   
   Module :py:mod:`dotc` built from fortran code in :file:`cpp_dotc/dotc.cpp`.
   
   .. function:: dotc(a,b)
      :module: et_dot.dotc
      
      Compute the dot product of *a* and *b* (in C++.)
   
      :param a: 1D Numpy array with ``dtype=numpy.float64``
      :param b: 1D Numpy array with ``dtype=numpy.float64``
      :returns: the dot product of *a* and *b*
      :rtype: ``numpy.float64``  
      
Note that the documentation must be entirely in :file:`.rst` format (see
restructuredText_).

Build the documentation::

    (.venv) > cd docs && make html
    Already installed: click
    Already installed: sphinx-click
    Already installed: sphinx
    Already installed: sphinx-rtd-theme
    Running Sphinx v2.2.2
    making output directory... done
    WARNING: html_static_path entry '_static' does not exist
    building [mo]: targets for 0 po files that are out of date
    building [html]: targets for 7 source files that are out of date
    updating environment: [new config] 7 added, 0 changed, 0 removed
    reading sources... [100%] readme
    looking for now-outdated files... none found
    pickling environment... done
    checking consistency... /Users/etijskens/software/dev/workspace/tmp/ET-dot/docs/apps.rst: WARNING: document isn't included in any toctree
    done
    preparing documents... done
    writing output... [100%] readme
    generating indices...  genindex py-modindexdone
    highlighting module code... [100%] et_dot.dotc
    writing additional pages...  search/Users/etijskens/software/dev/workspace/tmp/ET-dot/.venv/lib/python3.7/site-packages/sphinx_rtd_theme/search.html:20: RemovedInSphinx30Warning: To modify script_files in the theme is deprecated. Please insert a <script> tag directly in your theme instead.
      {{ super() }}
    done
    copying static files... ... done
    copying extra files... done
    dumping search index in English (code: en)... done
    dumping object inventory... done
    build succeeded, 2 warnings.

    The HTML pages are in _build/html.

The documentation is built using ``make``. The :file:`Makefile` checks that the necessary components
sphinx_, click_, sphinx-click_and `sphinx-rtd-theme <https://sphinx-rtd-theme.readthedocs.io/en/stable/>`_ are installed.

You can view the result in your favorite browser::

    (.venv) > open _build/html/index.html

The filepath is made evident from the last output line above.
This is what the result looks like (html):

.. image:: ../tutorials/tutorial-2/img3.png

Increment the version string:

    (.venv) > micc version -M -t
    [ERROR]
    Not a project directory (/Users/etijskens/software/dev/workspace/tmp/ET-dot/docs).
    (.venv) > cd ..
    (.venv) > micc version -M -t
    [INFO]           (ET-dot)> micc version (0.3.0) -> (1.0.0)
    [INFO]           Creating git tag v1.0.0 for project ET-dot
    [INFO]           Done.

Note that we first got an error because we are still in the docs directory, and not in
the project root directory.