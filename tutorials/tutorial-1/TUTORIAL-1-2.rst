Your first code
---------------
Our module file ``et_dot.py`` looks as follows.

.. code-block:: python

   # -*- coding: utf-8 -*-
   """
   Package et_dot
   =======================================
   
   """
   __version__ = "0.0.0"
   
   # Your code here...
   
Open it in your favourite editor and change it as follows:

.. code-block:: python

   # -*- coding: utf-8 -*-
   """
   Package et_dot
   ==============
   Python module for computing the dot product of two arrays.
   """
   __version__ = "0.0.0"
   
   
   def dot(a,b):
       """computes the dot product of *a* and *b*
       
       :param a: a 1D array.
       :param b: a !D array of the same lenght as *a*.
       :returns: the dot product of *a* and *b*.
       """
       n = len(a)
       if len(b)!=n:
           raise ArithmeticError("dot(a,b) requires len(a)==len(b).")
       d = 0 
       for i in range(n):
           d += a[i]*b[i]
       return d

Then open the file ``tests/test_et_dot.py`` and 

