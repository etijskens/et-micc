Can I use Anaconda Python distributions?
----------------------------------------
Yes, both `Micc <https://micc.readthedocs.io>`_ and `Poetry <https://python-poetry.org/>`_
play well together with conda environments, as long as you installed the Anaconda Python
distributions in your user space. So, on your local machine there is no problem. On a
cluster installing your own conda distribution is not recommended because it uses a lot
of disk space. If you cannot avoid it, install on the local scratch file system.

Using the Intel Distribution for Python, which is also a conda based, did not work out at the
time of writing (September 2020). Working around Poetry_ by manually creating conda virtual
environments and managing dependencies manually failed.

Can I use micc_ on the (VSC) clusters?
--------------------------------------
Yes, see `Tutorial 7 - Using micc projects on the VSC clusters`_.

Why doesn't micc_ have rename and remove commands?
--------------------------------------------------
While renaming a submodule or a removing a submodule would be valuable additions, it is very
complicated to retrieve all references to a submodule in a project correctly. See
https://github.com/etijskens/et-micc/issues/29 and https://github.com/etijskens/et-micc/issues/32.

If refactoring is necessary, we strongly recommend creating a new project and subprojects with
the correct names and manually copying stuff from the original to the refactored project.

