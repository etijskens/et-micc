Version management
==================

when you create a new project, Micc_ immediately provides a local git_ repository for 
you and commits the initial files Micc_ set up for you. If you have git_ account you 
can register it in the preferences file :file:`~/.micc/micc.json`, using the 
``github_username`` entry::

   {
   ...
   , "github_username"  : {"default":"etijskens"
                          ,"text"   :"your github username"
                          }
   ...
   }

Micc_ does not creat a remote github repository for you, but if you registered your 
``github_username`` in the preferences file, it will add a remote origin at
``https://github.com/etijskens/<your_project_name>/`` As soon as you create
that repository at github your can push your local commits 
 Version control is done with git_. 
