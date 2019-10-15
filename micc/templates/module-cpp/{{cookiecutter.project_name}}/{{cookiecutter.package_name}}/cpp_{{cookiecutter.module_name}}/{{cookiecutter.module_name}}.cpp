/*
 *  C++ source file for module {{ cookiecutter.package_name }}.{{ cookiecutter.module_name }}
 */


// See http://people.duke.edu/~ccc14/cspy/18G_C++_Python_pybind11.html for examples on how to use pybind11.
// The example below is modified after http://people.duke.edu/~ccc14/cspy/18G_C++_Python_pybind11.html#More-on-working-with-numpy-arrays
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

void
add ( py::array_t<double> x
    , py::array_t<double> y
    , py::array_t<double> z
    )
{
    auto bufx = x.request()
       , bufy = y.request()
       , bufz = z.request()
       ;
    if( bufx.ndim != 1
     || bufy.ndim != 1
     || bufz.ndim != 1 ) 
    {
        throw std::runtime_error("Number of dimensions must be one");
    }

    if( (bufx.shape[0] != bufy.shape[0])
     || (bufx.shape[0] != bufz.shape[0]) )
    {
        throw std::runtime_error("Input shapes must match");
    }
 // because the Numpy arrays are mutable by default, py::array_t is mutable too.
 // Below we declare the raw C++ arrays for x and y as const to make their intent clear.
    double const *ptrx = static_cast<double const *>(bufx.ptr);
    double const *ptry = static_cast<double const *>(bufy.ptr);
    double       *ptrz = static_cast<double       *>(bufz.ptr);

    for (size_t i = 0; i < bufx.shape[0]; i++)
        ptrz[i] = ptrx[i] + ptry[i];
}


PYBIND11_MODULE({{ cookiecutter.module_name }}, m)
{// optional module doc-string
    m.doc() = "pybind11 {{ cookiecutter.module_name }} plugin"; // optional module docstring
 // list the functions you want to expose:
 // m.def("exposed_name", function_pointer, "doc-string for the exposed function");
    m.def("add", &add, "A function which adds two arrays 'x' and 'y' and stores the result in the third, 'z'.");
}
