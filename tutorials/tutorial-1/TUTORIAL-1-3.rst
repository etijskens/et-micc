1.3 Improving efficiency
------------------------
There are times when a correct solution - i.e. a code that solves the problem correctly - 
is sufficient. Most of the time, however, the solution also needs use resources efficiently, 
runtime, memory, ... Especially in High Performance Computing, where compute tasks may run 
for several days and use hundreds of compute nodes, and resources are to be sharede wiht 
may researchers, using the resources efficiently is of utmost importance. 

However important efficiency may be, it is nevertheless a good strategy for developing a
new piece of code, to start out with a simple, even naive implementation in Python, neglecting
all efficiency considerations, but focussing on correctness. Python has a reputation of being 
an extremely productive programming language. Once you have proven the correctness of this first 
version it can serve as a reference solution to verify the correctness of later efficiency 
improvements. In addition, the analysis of this version can highlight the sources of 
inefficiency and help you focus your attention to the parts that really need it.
    
1.3.1 Timing your code
^^^^^^^^^^^^^^^^^^^^^^
The simplest way to probe the efficiency of your code is to time it: write a simple script 
and record how long it takes to execute. Let us first look at the structure of a Python script. 

Here's a script (using the above structure) that computes the dot product of two long arrays 
of random numbers. 

.. code-block:: python

   """file ET_dot/prof/run1.py"""
   import random
   from et_dot import dot
   
   def random_array(n=1000):
       """Initialize an array with n random numbers in [0,1[."""
       # Below we use a list comprehension (a Python idiom for creating a list from an iterable object). 
       a = [random.random() for i in range(n)]
       return a
   
   if __name__=='__main__':
       a = random_array()
       b = random_array()
       print(dot(a,b))
       print('-*# done #*-')       
     
We store this file, which we rather simply called :file:`run1.py`, in a directory :file:`prof` 
in the project directory where we intend to keep all our profiling work. 
You can execute the script from the command line (with the project directory as the current
working directory:
       
.. code-block:: bash

   (.venv) > python ./prof/run1.py
   251.08238559724717
   -*# done #*-
      
.. note:: As our script does not fix the random number seed, every run has a different outcome.
   
We are now ready to time our script. Micc_ provides a practical context manager class 
:py:class:`et_micc.Stopwatch` to time pieces of code. 

.. code-block:: python

   """file ET_dot/prof/run1.py"""
   from et_micc.stopwatch import Stopwatch
   
   ...   
   
   if __name__=='__main__':
       with Stopwatch() as timer:
           a = random_array()
           b = random_array()
           print("init:",timer.timelapse(),'s')
           dot(a,b)
           print("dot :",timer.timelapse(),'s')
       print('-*# done #*-')
       
When the script is exectuted the two print statements will print the duration of the 
initalisation of *a* and *b* and of the computation of the dot product of *a* and *b*.
Finally, upon exit the :py:obj:`Stopwatch` will print the total time.

.. code-block:: bash

   (.venv) > python ./prof/run1.py
   init: 0.000281 s
   dot : 0.000174 s
   0.000465 s
   -*# done #*-
   >

Note that the initialization phase took longer than the computation. Random number 
generation is rather expensive. The last number is the total time spent inside the 
stopwatch body, and is printed automatically. If you like you can customise this 
message by setting the ``message`` parameter in the constructor of the stopwatch:

.. code-block:: python

   with Stopwatch(message="total") as timer:
      ...

which would have output:

.. code-block:: bash

   (.venv) > python ./prof/run1.py
   init: 0.000281 s
   dot : 0.000174 s
   total 0.000465 s
   -*# done #*-
   >

1.3.2 Comparing to Numpy
^^^^^^^^^^^^^^^^^^^^^^^^
As said earlier, our implementation of the dot product is rather naive. If you want 
to become a good programmer, you should understand that you are probably not the 
first researcher in need of a dot product implementation. For most linear algebra 
problems, `Numpy <https://numpy.org>`_ provides very efficient implementations. 
Below the :file:`run1.py` script adds timing results for the Numpy_ equivalent of 
our code.

.. code-block:: python

   """file ET_dot/prof/run1.py"""
   import numpy as np
   
   ...   
   
   if __name__=='__main__':
       with Stopwatch() as timer:
           a = random_array()
           b = random_array()
           print("et init:",timer.timelapse(),'s')
           dot(a,b)
           print("et dot :",timer.timelapse(),'s')

       with Stopwatch() as timer:
           a = np.random.rand(1000)
           b = np.random.rand(1000)
           print("np init:",timer.timelapse(),'s')
           np.dot(a,b)
           print("np dot :",timer.timelapse(),'s')
       
       print('-*# done #*-') 
       
When you run this code, you will get a :py:exc:`ModuleNotFoundError` for Numpy_, as it 
it not yet a dependency of our ET-dot project and Numpy_ is not yet installed in our 
virtual environment. If you do not want Numpy_ to become a dependency of ET-dot, just
install it in the virtual environment ::

.. code-block:: bash

   (.venv) > pip install numpy
   Collecting numpy
   
     Using cached https://files.pythonhosted.org/packages/60/9a/a6b3168f2194fb468dcc4cf54c8344d1f514935006c3347ede198e968cb0/numpy-1.17.4-cp37-cp37m-macosx_10_9_x86_64.whl
     
   Installing collected packages: numpy
   Successfully installed numpy-1.17.4
   Here are the results. Note that the Numpy_ version is significantly faster, both for 
   initialization (x3.2) and for the dot product (x6.8). 
   (.venv) >
  
If, on the other hand, you want Numpy_ to become a dependency of ET-dot, and have 
it always automatically installed together with ET-dot, you must run:"

.. code-block:: bash

   (.venv) > poetry add numpy
   Using version ^1.17.4 for numpy
   
   Updating dependencies
   Resolving dependencies... (0.2s)
   
   Writing lock file
   
   
   Package operations: 1 install, 0 updates, 0 removals
   
     - Installing numpy (1.17.4)
   
   (.venv) >
 
Here are the results of the modified script:

.. code-block:: bash

   (.venv) > python ./prof/run1.py
   et init: 0.000252 s
   et dot : 0.000219 s
   0.000489 s
   np init: 7.8e-05 s
   np dot : 3.2e-05 s
   0.00012 s
   -*# done #*-
   >
       
Obviously, Numpy_ does significantly better than our naive dot product implementation. 
The reasons for this improvement are:

* Numpy_ arrays are contiguous data structures of floating point numbers, unlike Python's
  :py:class:`list`. Contiguous memory access is far more efficient.
* The loop over Numpy_ arrays is implemented in a low-level programming languange.
  This allows to make full use of the processors hardware features, such as vectorization and
  fused multiply-add (FMA).
  