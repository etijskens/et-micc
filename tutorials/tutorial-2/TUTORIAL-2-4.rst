Specifying compiler options for binary extension modules
--------------------------------------------------------

[ **Advanced Topic** ] 
As we have seen, binary extension modules can be programmed in Fortran and C++. 
Micc_ provides convenient wrappers to build such modules. Fortran source code is
transformed to a python module using f2py_, and C++ source using Pybind11_ and 
CMake_. Obviously, in both cases there is a compiler under the hood doing the 
hard work. By default these tools use the compiler they find on the path, but 
you may as well specify your favorite compiler.

Building a single module only
-----------------------------
If you want to build a single binary extension module rather than all binary
extension modules in the project, add the ``-m|--module`` option:

.. code-block:: 

   > micc build --module my_module <build options>
   
This will only build module *my_module*.

Performing a clean build
------------------------
To perform a clean build, add the ``--clean`` flag to the ``micc build`` command:

.. code-block:: 

   > micc build --clean <other options>

This will remove the previous build directory and as well as the binary extension 
module.

Controlling the build of f2py modules
-------------------------------------
To specify the Fortran compiler, e.g. the GNU fortran compiler:

.. code-block:: 
   
   > micc build --f90exec path/to/gfortran
   
Note, that this exactly how you would have specified it using f2py_ directly.
You can specify the Fortran compiler options you want using the ``--f90flags`` 
option:

.. code-block:: 
   
   > micc build --f90flags "string with all my favourit options"
   
In addition f2py_ (and ``micc build`` for that matter) provides two extra options 
``--opt`` for specifying optimization flags, and ``--arch`` for specifying architecture
dependent optimization flags. These flags can be turned off by adding ``--noopt`` and 
``--noarch``, respectively. This can be convenient when exploring compile options. 
Finally, the ``--debug`` flag adds debug information during the compilation.

``Micc_ build`` also provides a ``--build-type`` options which accepts ``release`` and
``debug`` as value (case insensitive). Specifying ``debug`` is equivalent to 
``--debug --noopt --noarch``.

.. note:: ALL f2py modules are built with the same options. To specify separate options 
   for a particular module use the ``-m|--module`` option. 

.. note:: Although there are some commonalities between the compiler options of the 
   various compilers, you will most probably have to change the compiler options when 
   you change the compiler.

Controlling the build of cpp modules
------------------------------------
The C++ compiler, e.g. the Intel C++ compiler, is specified as:

.. code-block:: 
   
   > micc build --cxx-compiler path/to/icpc
   
Here, the ``--cxx-compiler``'s value is tranferred to the CMake_ variable 
``CMAKE_CXX_COMPILER``. 

CMake_ provides default build options for four build types:

* ``CMAKE_CXX_FLAGS_DEBUG     ``: ``-g``
* ``CMAKE_CXX_FLAGS_MINSIZEREL``: ``-Os -DNDEBUG``
* ``CMAKE_CXX_FLAGS_RELEASE   ``: ``-O3 -DNDEBUG``
* ``CMAKE_CXX_FLAGS_RELWITHDEBINFO``: ``-O2 -g -DNDEBUG``

You can overwrite their value by specifying ``--build-type`` (to select the build type)
and ``--cxx-flags`` to set the appropriate value. These variables are merged with the 
CMake_ variable ``CMAKE_CXX_FLAGS``, which is empty by default. This variable can be 
overwritten by using the ``--cxx-flags-all`` option,
   
.. note:: ALL cpp modules are built with the same options. To specify separate options 
   for a particular module use the ``-m|--module`` option. 

.. note:: CMake_ selects reasonable options for the four build types above, taking into 
   account the chosen compiler. For tweeking, however, you will most probably have to 
   change the compiler options when you change the compiler.

Save and Load build options to/from file
----------------------------------------
With the ``--save`` option you can save the current build options to a file in .json 
format. This acts on a per project basis. E.g.:

.. code-block:: 
  
   > micc build <my build options> --save build[.json]

will save the *<my build options>* to the file :file:`build.json` in every binary module
directory (the .json extension is added if omitted). You can restrict this to a single 
module with the ``--module`` option (see above). The saved options can be reused in a 
later build as:
 
.. code-block:: 
  
   > micc build --load build[.json]

Installing packages with binary extension modules
-------------------------------------------------
Normally, installation would be performed with poetry_, but as this part of poetry_ is
not implemented yet, we have to rely on workarounds. 

If your package contains CLIs, you must run (in the project directory):

.. code-block:: 
  
   > micc build 
   > make [re]install
   > micc dev-install
   
The last step replaces the directory :file:`site-packages/micc` in your current Python
environment by the directory structure of the :file:`micc` package, but replaces all files
with symlinks. 

Alternatively, instead of the last step, you may move/copy/symlink the :file:`.so` files 
in the :file:`micc` package manually to :file:`site-packages/micc` in your current Python 
environment.


Currently, there are two options
