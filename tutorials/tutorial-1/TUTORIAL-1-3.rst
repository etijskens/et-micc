Improving efficiency
--------------------
There are times when a correct solution - i.e. a code that solves the problem correctly - 
is sufficient. Most of the time, however, the solution also needs use resources efficiently, 
runtime, memory, ... Especially in High Performance Computing, where compute tasks may run 
for several days and use hundreds of compute nodes, and resources are to be sharede wiht 
may researchers, using the resources efficiently is of utmost importance. 

However important efficiency may be, it is nevertheless a good strategy for developing a
new piece of code, to start out with a simple, even naive implementation in Python, neglecting
all efficiency considerations, but focussing on correctness. Python has a reputation of being 
an extremely productive programming language. Once you have proven the correctness of this first version
it can serve as a reference solution to verify the correctness of later efficiency improvements.
In addition, the analysis of this version can highlight the sources of inefficiency and help
you focus your attention to the parts that really need it.
    
Timing your code
^^^^^^^^^^^^^^^^
The simplest way to probe the efficiency of your code is to time it: write a simple script 
and record how long it takes to execute. Let us first look at the structure of a Python script. 

   **Python tip: structuring a script**
   
   Here's a neat way of structuring a Python script:
   
   .. code-block:: python
      
      """file: my_script.py"""
      
      # imports
      
      # function and class definitions your script needs
      def hello(arg="world"):
         print("hello",arg)
      
      if __name__=="__main__":
         # your script
         hello("from my_script")
         print("-*# done #*-") 
         
   There are two interesting points in this file. 
   
   #. The body of the if statement ``if __name__=="__main__":`` is only executed if the file is run as a script:
   
      .. code-block:: bash
      
         > python my_script.py
         hello from my_script
         -*# done #*-
         >
   
      Thus, if the file is imported in some other Python file that body is not executed, but all 
      de function and class definitions, such as :py:meth:`hello` are made available to the importing 
      file. In this way your file can both behave as a script and as a module.
      
      .. code-block:: python
      
         >>> import my_script
         >>> my_script.hello()
         hello world
         >>>
      
      Note that import script does not generate output as the statements ``hello("from my_script")``
      and ``print("-*# done #*-")`` are not executed.
     
      This trick comes in handy in unit test scripts. If you add these lines to a test file,
      
      .. code-block:: python
      
         if __name__ == "__main__":
            the_test_you_want_to_debug = test_dot_aa

            print("__main__ running", the_test_you_want_to_debug)
            the_test_you_want_to_debug()
            print('-*# finished #*-')
                   
      Executing this file as a script will execute only the test ``test_dot_aa``, 
      
      .. code-block:: bash
      
         > python test_ET_dot.py
         __main__ running <function test_dot_aa at 0x1065064d0>
         -*# finished #*-
         >
         
      You can use this to debug a failing test. Just make the variable ``the_test_you_want_to_debug``
      point to the test you want to debug.
         
   #. It is recommended that the last line that your script executes is a print statement 
      that assures you that the script has done its work and that is is not lost in an infinite 
      loop or waiting for something. 

Here's a script (using the above structure) that computes the dot product of two long arrays 
of random numbers. 

.. code-block:: python

   """file ET_dot/prof/run1.py"""
   import random
   from et_dot import dot
   
   def random_array(n=1000):
       """Initialize an array with n random numbers in [0,1[."""
       # Below we use a list comprehension. That is a Python idiom that creates a list. 
       a = [random.random() for i in range(n)]
       return a
   
   if __name__=='__main__':
       a = random_array()
       b = random_array()
       print(dot(a,b))
       print('-*# done #*-')       
     
We created a directory :file:`prof` in the project directory (using the command line or any
kind of file manager) to store the script, which we rather simply called :file:`run1.py`.
You can execute the script from the command line (with the project directory as the current
working directory:
       
.. code-block:: bash

   > PYTHONPATH='.' python ./prof/run1.py
   251.08238559724717
   -*# done #*-
   
The command ``PYTHONPATH='.'`` in front of the ``python command`` sets the ``PYTHONPATH``
environment variable for the lifetime of the ``python command``. It extends the path 
where Python looks for imports with the current directory, which is where it should find
:file:`ET_dot.py`. You can also set the variable for the lifetime of the terminal session:  

.. code-block:: bash

   > export PYTHONPATH='.'
   > python ./prof/run1.py
   247.11469232296827
   -*# done #*-
   
As our script did not fix the random number seed, every run has a different outcome.
A third option is to extend the path in your script:

.. code-block:: python

   """file ET_dot/prof/run1.py"""
   # add the current working directory to the import search path:
   import sys
   sys.path.insert(0,'.')
   
   import random
   from et_dot import dot
   
We are now ready to time our script. *Micc* provides a practical context manager class 
:py:class:`micc.stopwatch` to time pieces of code. 

.. code-block:: python

   """file ET_dot/prof/run1.py"""
   import random
   from et_dot import dot
   from micc.stopwatch import Stopwatch
   
   def random_array(n=1000):
       """Initialize an array with n random numbers in [0,1[."""
       # Below we use a list comprehension. That is a Python idiom that creates a list. 
       a = [random.random() for i in range(n)]
       return a
   
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

   > python ./prof/run1.py
   init: 0.000281 s
   dot : 0.000174 s
   0.000465 s
   -*# done #*-
   >

Note that the initialization phase took longer than the computation. Random number 
generation is rather expensive. 

As said earlier, our implementation of the dot product is rather naive. If you want to
become a good programmer, you should understand that you are probably not first researcher
in need of a dot product implementation. For most linear algebra problems, `Numpy <https://numpy.org>`_
provides very efficient implementations. Below the :file:`run1.py` script adds timing results
for the *numpy* equivalent of our code.

.. code-block:: python

   """file ET_dot/prof/run1.py"""
   import random
   from et_dot import dot
   from micc.stopwatch import Stopwatch
   
   import numpy as np
   
   def random_array(n=1000):
       """Initialize an array with n random numbers in [0,1[."""
       # Below we use a list comprehension. That is a Python idiom that creates a list. 
       a = [random.random() for i in range(n)]
       return a
   
   
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
       
Here are the results. Note that the *Numpy* version is significantly faster, both for 
initialization (x3.2) and for the dot product (x6.8). 

.. code-block:: bash

   > python ./prof/run1.py
   et init: 0.000252 s
   et dot : 0.000219 s
   0.000489 s
   np init: 7.8e-05 s
   np dot : 3.2e-05 s
   0.00012 s
   -*# done #*-
   >
       
The reasons for this improvement are:

* *Numpy* arrays are contiguous data structures of floating point numbers, unlike Python's
  :py:class:`list`. Contiguous memory access ifs far more efficient.
* The loop over *Numpy* arrays is implemented in a low-level programming languange (C).
  This allows to make full use of the processors hardware features, such as vectorization and
  fused multiply-add (FMA).
  