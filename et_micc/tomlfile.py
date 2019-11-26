# -*- coding: utf-8 -*-
"""
Module et_micc.tomlfile
=======================
"""
# This is a copy of poetry/utils/toml_file.py
# It is there to avoid introducing a dependency on poetry in et_micc.
from tomlkit.toml_file import TOMLFile as BaseTOMLFile
from typing import Union

# from ._compat import Path
from pathlib import Path


class TomlFile(BaseTOMLFile):
    """Read/write access to :file:`.toml` files (:file:`pyproject.toml` in particular).
    
    Open a :file:`.toml` file and read its content
    
    The content is accessed by subscripting:
    
    .. code-block:: python
    
       toml = TomlFile('path/to/toml')
       # Read an item from the .toml file's content:
       old_name = toml['tool']['poetry']['name']
       # Modify an item in the .toml file's content (but not yet in the file):
       toml['tool']['poetry']['name'] = 'new_name'
       # Now modify the file with the modified content:
       toml.save()
        
    :param str|Path path: path to the .toml file.
    :raises: FileNotFoundError if the file does not exist.
    """
    def __init__(self, path):  # type: (Union[str, Path]) -> None
        super(TomlFile, self).__init__(str(path))

        self._path_ = Path(path)
        if self.exists():
            self._content_ = self.read()
        else:
            raise FileNotFoundError(str(self._path_))

    @property
    def path(self):  # type: () -> Path
        """Path object of the :file:`.toml` file"""
        return self._path_

    def exists(self):  # type: () -> bool
        """Does the :file:`.toml` file exist?"""
        return self._path_.exists()

    def __getattr__(self, item):
        """Delegate to self.path."""
        return getattr(self._path_, item)

    def __str__(self):
        """string representation of self.path"""
        return str(self._path)
    
    def __getitem__(self,item):
        """Read access the content of the :file:`.toml` file."""
        return self._content_[item]

    def __setitem__(self,item,value):
        """Write access the content of the :file:`.toml` file."""
        self._content_[item] = value

    def save(self):
        """Write the current content of the :file:`.toml` file back to file."""
        self.write(self._content_)\
        
# eof