**********
Change log
**********

v2.0.0
------
Prior to v2 micc-build and micc were added as a dependency of every micc project with binary
extensions. As a consequence all their subdependencies were added too. Amongst others:

* numpy
* pybind11
* sphinx
* pytest
* sphinx-click
* sphinx-rt-theme
* ...

When creating a virtual environment these dependencies put the file systems of the VSC clusters
pressure.
