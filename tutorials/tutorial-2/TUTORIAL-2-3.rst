2.3 Intermediate topics
-----------------------

2.3.1 Binary extension modules and data types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An importand point of attention when writing binary extension modules - and a
common source of problems - is that the data types of the variables passed in from
Python must match the data types of the Fortran or C++ routines.

Here is a table with the most relevant numeric data types in Python, Fortran and C++.
 
================  ============   =========   ====================
kind              Numpy/Python   Fortran     C++
================  ============   =========   ====================
unsigned integer  uint32         N/A         signed long int
unsigned integer  uint64         N/A         signed long long int
signed integer    int32          integer*4   signed long int
signed integer    int64          integer*8   signed long long int
floating point    float32        real*4      float
floating point    float64        real*8      double
complex           complex64      complex*4   std::complex<float>
complex           complex128     complex*8   std::complex<double>
================  ============   =========   ====================
               
2.3.2 F2py
^^^^^^^^^^
   
F2py_ is very flexible with respect to data types. In between the
Fortran routine and Python call is a wrapper function which translates the
function call, and if it detects that the data type on the Python sides and
the Fortran sideare different, the wrapper function is allowed to copy/convert
the variable when passing it to Fortran routine both, and also when passing the
result back from the Fortran routine to the Python caller. When the input/output
variables are large arrays copy/conversion operations can have a detrimental
effect on performance and this is in HPC highly undesirable. Micc_ runs f2py_ with
the ``-DF2PY_REPORT_ON_ARRAY_COPY=1`` option. This causes your code to produce a
warning everytime the wrapper decides to copy an array. Basically, this warning
means that you have to modify your Python data structure to have the same data
type as the Fortran source code, or vice versa.

2.3.4 Returning large data structures
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The result of a Fortran function and a C++ function is **always** copied back to the 
Python variable that will hold it. As copying large data structures is detrimental
to performance this shoud be avoided. The solution to this problem is to write 
Fortran functions or subroutines and C++ functions that accept the result variable 
as an argument and modify it in place, so that the copy operaton is avoided. Consider
this example of a Fortran subroutine that computes the sum of two arrays.
are some examples of array addition:

.. code-block:: fortran
   
   subroutine add(a,b,sumab,n)
     ! Compute the sum of arrays a and b and overwrite array sumab with the result
       implicit none
     
       integer*4              , intent(in)    :: n
       real*8   , dimension(n), intent(in)    :: a,b
       real*8   , dimension(n), intent(inout) :: sumab
       
     ! declare local variables
       integer*4 :: i
     
       do i=1,n
           sumab(i) = a(i) + b(i)
       end do
   end subroutine add
   
The crucial issue here is that the result array *sumab* has ``intent(inout)``. If
you qualify the intent of *sumab* as ``in`` you will not be able to overwrite it,
whereas - surprisingly - qualifying it with ``intent(out)`` will force f2py to consider
it as a left hand side variable, which implies copying the result on returning.

The code below does exactly the same but uses a function, not to return the result
of the computation, but an error code.

.. code-block:: fortran
   
   function add(a,b,sumab,n)
     ! Compute the sum of arrays a and b and overwrite array sumab with the result
       implicit none
     
       integer*4              , intent(in)    :: n,add
       real*8   , dimension(n), intent(in)    :: a,b
       real*8   , dimension(n), intent(inout) :: sumab
     
     ! declare local variables
       integer*4 :: i
     
       do i=1,n
           sumab(i) = a(i) + b(i)
       end do
       
       add = ... ! set return value, e.g. an error code. 
    
   end function add

The same can be accomplished in C++:

.. code-block:: c++

   #include <pybind11/pybind11.h>
   #include <pybind11/numpy.h>
   
   namespace py = pybind11;
   
   void
   add ( py::array_t<double> a
       , py::array_t<double> b
       , py::array_t<double> sumab
       )
   {// request buffer description of the arguments
       auto buf_a = a.request()
          , buf_b = b.request()
          , buf_sumab = sumab.request()
          ;
       if( buf_a.ndim != 1
        || buf_b.ndim != 1
        || buf_sumab.ndim != 1 ) 
       {
           throw std::runtime_error("Number of dimensions must be one");
       }
   
       if( (buf_a.shape[0] != buf_b.shape[0])
        || (buf_a.shape[0] != buf_sumab.shape[0]) )
       {
           throw std::runtime_error("Input shapes must match");
       }
    // because the Numpy arrays are mutable by default, py::array_t is mutable too.
    // Below we declare the raw C++ arrays for a and b as const to make their intent clear.
       double const *ptr_a     = static_cast<double const *>(buf_a.ptr);
       double const *ptr_b     = static_cast<double const *>(buf_b.ptr);
       double       *ptr_sumab = static_cast<double       *>(buf_sumab.ptr);
   
       for (size_t i = 0; i < buf_a.shape[0]; i++)
           ptr_sumab[i] = ptr_a[i] + ptr_b[i];
   }
   
   
   PYBIND11_MODULE({{ cookiecutter.module_name }}, m)
   {// optional module doc-string
       m.doc() = "pybind11 {{ cookiecutter.module_name }} plugin"; // optional module docstring
    // list the functions you want to expose:
    // m.def("exposed_name", function_pointer, "doc-string for the exposed function");
       m.def("add", &add, "A function which adds two arrays 'a' and 'b' and stores the result in the third, 'sumab'.");
   }

Here, care must be taken that when casting ``buf_sumab.ptr`` one does not cast to const.