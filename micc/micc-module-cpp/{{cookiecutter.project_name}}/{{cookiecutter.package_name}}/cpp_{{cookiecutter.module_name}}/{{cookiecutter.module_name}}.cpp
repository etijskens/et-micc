/*
 *  C++ source file for module {{ cookiecutter.package_name }}.{{ cookiecutter.module_name }}
 *
 *  Remarks:
 *    . documentation?
 */

#include <pybind11/pybind11.h>

int add(int i, int j) {
    return i + j;
}

PYBIND11_MODULE({{ cookiecutter.module_name }}, m) {
    m.doc() = "pybind11 {{ cookiecutter.module_name }} plugin"; // optional module docstring

    m.def("add", &add, "A function which adds two numbers");
}
