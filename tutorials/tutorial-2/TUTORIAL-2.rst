Tutorial 2: Adding binary extensions
====================================

Suppose for a moment that *Numpy* did not have a dot product implementation and that the
implementation provided in Tutorial-1 is way too slow to be practical for your
research project. For the reasons mention you would have to provide your own low-level 
implementation yourself in Fortran, C or C++. Such modules arr called *binary extensions*.
*Micc* can assist you with  building binary extensions and gives you the option to choose 
between Fortran and C++. As C is approximately a subset of C++ there is little reason to 
provide support for both C++ and C.

*Micc* provides boilerplate code for binary extensions as well as some practical wrappers
around top-notch tools for building binary extensions from Fortran and C++. Fortran code 
is compiled into a Python module using `f2py <https://docs.scipy.org/doc/numpy/f2py/>`_ 
(which comes with Numpy_) and `CMake <https://cmake.org>`_. For C++ we use pybind11_ and 
CMake_.

Choosing between Fortran and C++ for binary extension modules
-------------------------------------------------------------
Here are a number of arguments that you may wish to take into account for choosing the
programming language for your binary extension modules:  

* Fortran is a simpler languages than C++
* It is easier to write efficient code in Fortran than C++
* C++ is a much more expressive language
* C++ comes with a huge standard library, providing lots of data structures and algorithms
  that are hard to match in Fortran. If the standard library is not enough, there is 
  `Boost <https://boost.org>`_ and many other domain specific libraries. There are also 
  domain specific libraries in Fortran, but the amount differs by an order of magnitude at
  least.
* With *pybind11* you can almost expose anything from the C++ side to Python, not just 
  functions. 
* Modern Fortran is (imho) not as good documented as C++. Useful place to look for 
  language features and idioms are:
  
  * https://www.fortran90.org/
  * http://www.cplusplus.com/
  * https://en.cppreference.com/w/
  
In short, C++ provides much more possibilities, but it is not for the novice.   
 
