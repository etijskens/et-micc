Your first code
---------------
   
Open module file :file:`et_dot.py` in your favourite editor and change it as follows:

.. code-block:: python

   # -*- coding: utf-8 -*-
   """
   Package et_dot
   ==============
   Python module for computing the dot product of two arrays.
   """
   __version__ = "0.0.0"
   
   def dot(a,b):
       """Compute the dot product of *a* and *b*.
       
       :param a: a 1D array.
       :param b: a !D array of the same lenght as *a*.
       :returns: the dot product of *a* and *b*.
       :raises: ArithmeticError if ``len(a)!=len(b)``.
       """
       n = len(a)
       if len(b)!=n:
           raise ArithmeticError("dot(a,b) requires len(a)==len(b).")
       d = 0 
       for i in range(n):
           d += a[i]*b[i]
       return d

We could use the dot method in a script as follows

.. code-block:: python

   from et_dot import dot
   
   a = [1,2,3]
   b = [4.1,4.2,4.3]
   a_dot_b = dot(a,b) 

.. note::
   This implementation is naive for many reasons:
   
   * Python is very slow at executing loops, as compared to Fortran or C++. 
   * The objects we are passing in are plain Python :py:obj:`list`s. A :py:obj:`list`
     is a very powerfull data structure, with array-like properties, but it is not
     exactly an array. A :py:obj:`list` is in fact an array of pointers to Python
     objects, and therefor list elements can reference anything, not just a numeric 
     value as we would expect from an array. Elements being pointers, looping over the
     array elements implies non-contiguous memory access, another source of inefficiency.   
   * The dot product is a subject of Linear Algebra. Many excellent libraries have been
     designed for this purpose. Numpy_ should be your starting
     point because it is well integrated with many other Python packages. There is also
     `Eigen <http://eigen.tuxfamily.org/index.php?title=Main_Page>`_
     a C++ library for linear algebra that is neatly exposed to Python by 
     pybind11_.
      
   
In order to verify that our implementation of the dot product is correct, we write a 
test. For this we open the file ``tests/test_et_dot.py``. Remove the original tests, 
and add a new one: 

.. code-block:: python

   def test_dot_aa():
       a = [1,2,3]
       expected = 14
       result = dot(a,a)
       assert result==expected

Save the file, and run the test. Pytest_ will show a line for every test source file.
On each such line a ``.`` will appear for every successfull test, and a ``F`` for a 
failing test.

.. code-block:: bash

   > pytest
   =============================== test session starts ===============================
   platform darwin -- Python 3.7.4, pytest-4.6.5, py-1.8.0, pluggy-0.13.0
   rootdir: /Users/etijskens/software/dev/workspace/ET-dot
   collected 1 item
   
   tests/test_et_dot.py .                                                      [100%]
   
   ============================ 1 passed in 0.08 seconds =============================
   >


Great! our test succeeded. Obviously, our test tests only one particular case. 
A clever way of testing is to focus on properties. From mathematics we now that 
the dot product is commutative. Let us add a test for that. 

.. code-block:: python

   def test_dot_commutative():
       # create two arrays of length 10 with random float numbers: 
       a = []
       b = []
       for _ in range(10):
           a.append(random.random())
           b.append(random.random())
       # do the test
       ab = dot(a,b)
       ba = dot(b,a)
       assert ab==ba

You can easily verify that this test works too. There is however a risk in using 
arrays of random numbers. Maybe we were just lucky and got random numbers that satisfy
the test by accident. Also the test is not reproducible anymore. The next time we run
pytest_ we will get other random numbers, and may be the test will fail. That would 
represent a serious problem: since we cannot reproduce the failing test, we have no way
finding out what went wrong. For random numbers we can fix the seed at the beginning of
the test. Random number generators are deterministic, so fixing the seed makes the code
reproducible. To increase coverage we put a loop around the test. 

.. code-block:: python

   def test_dot_commutative_2():
       # Fix the seed for the random number generator of module random.
       random.seed(0)
       # choose array size
       n = 10
       # create two arrays of length n with with zeros:
       a = n * [0]
       b = n * [0]
       # repetion loop:
       for r in range(1000): 
           # fill a and b with random float numbers: 
           for i in range(n):
               a[i] = random.random()
               b[i] = random.random()
           # do the test
           ab = dot(a,b)
           ba = dot(b,a)
           assert ab==ba
           
Again the test works. Another property of the dot product is that the dot product
with a zero vector is zero. 

.. code-block:: python

   def test_dot_zero():
       # Fix the seed for the random number generator of module random.
       random.seed(0)
       # choose array size
       n = 10
       # create two arrays of length n with with zeros:
       a = n * [0]
       zero = n * [0]
       # repetion loop (the underscore is a placeholder for a variable dat we do not use):
       for _ in range(1000): 
           # fill a with random float numbers: 
           for i in range(n):
               a[i] = random.random()
           # do the test
           azero = dot(a,zero)
           assert azero==0

This test works too. Furthermore, the dot product with a vector of ones is the sum of
the elements of the other vector:

.. code-block:: python

   def test_dot_one():
       # Fix the seed for the random number generator of module random.
       random.seed(0)
       # choose array size
       n = 10
       # create two arrays of length n with with zeros:
       a = n * [0]
       one = n * [1.0]
       # repetion loop (the underscore is a placeholder for a variable dat we do not use):
       for _ in range(1000): 
           # fill a with random float numbers: 
           for i in range(n):
               a[i] = random.random()
           # do the test
           aone = dot(a,one)
           expected = sum(a)
           assert aone==expected


Success again. We are getting quite confident in the correctness of our implementation. Here 
is another test: 
   
.. code-block:: python

   def test_dot_one_2():
       a1 = 1.0e16
       a   = [a1 ,1.0,-a1]
       one = [1.0,1.0,1.0]
       expected = 1.0
       result = dot(a,one)
       assert result==expected

Clearly, it is a special case of the test above the expected result is the sum of the elements
in ``a``, that is ``1.0``. Yet it - unexpectedly - fails. Fortunately *pytest* produces a readable
report about the failure:

.. code-block:: bash

   > pytest
   ================================= test session starts ==================================
   platform darwin -- Python 3.7.4, pytest-4.6.5, py-1.8.0, pluggy-0.13.0
   rootdir: /Users/etijskens/software/dev/workspace/ET-dot
   collected 6 items
   
   tests/test_et_dot.py .....F                                                      [100%]
   
   ======================================= FAILURES =======================================
   ____________________________________ test_dot_one_2 ____________________________________
   
       def test_dot_one_2():
           a1 = 1.0e16
           a   = [a1 , 1.0, -a1]
           one = [1.0, 1.0, 1.0]
           expected = 1.0
           result = dot(a,one)
   >       assert result==expected
   E       assert 0.0 == 1.0
   
   tests/test_et_dot.py:91: AssertionError
   ========================== 1 failed, 5 passed in 0.17 seconds ==========================
   >

Mathematically, our expectations about the outcome of the test are certainly correct. Yet,
*pytest* tells us it found that the result is ``0.0`` rather than ``1.0``. What could possibly
be wrong? Well our mathematical expectations are based on our - false - assumption that the 
elements of ``a`` are real numbers, most of which in decimal representation are characterised
by an infinite number of digits. Computer memory being finite, however, Python (and for that
matter all other programming languages) uses a finite number of bits to approximate real 
numbers. These numbers are called *floating point numbers* and their arithmetic is called 
*floating point arithmetic*.  *Floating point arithmetic* has quite different properties than
real number arithmetic. A floating point number in Python uses 64 bits which yields 
approximately 15 representable digits. Observe the consequences of this in the Python statements
below:
   
.. code-block:: python
   
   >>> 1.0 + 1e16
   1e+16
   >>> 1e16 + 1.0 == 1e16
   True
   >>> 1.0 + 1e16 == 1e16
   True
   >>> 1e16 + 1.0 - 1e16
   0.0

There are several lessons to be learned from this:

* The test does not fail because our code is wrong, but because our mind is used to reasoning 
  about real number arithmetic, rather than *floating point arithmetic* rules. As the latter 
  is subject to round-off errors, tests sometimes fail unexpectedly.  Note that for comparing 
  floating point numbers the the standard library provides a :py:meth:`math.isclose` method.
* Another silent assumption by which we can be mislead is in the random numbers. In fact,
  :py:meth:`random.random` generates pseudo-random numbers **in the interval ``[0,1[``**, which 
  is quite a bit smaller than ``]-inf,+inf[``. No matter how often we run the test the special 
  case above that fails will never be encountered, which may lead to unwarranted confidence in
  the code.
  
So, how do we cope with the failing test? Here is a way using :py:meth:`math.isclose`:

.. code-block:: python
   
   def test_dot_one_2():
       a1 = 1.0e16
       a   = [a1 , 1.0, -a1]
       one = [1.0, 1.0, 1.0]
       expected = 1.0
       result = dot(a,one)
       # assert result==expected
       assert math.isclose(result, expected, abs_tol=10.0)

This is a reasonable solution if we accept that when dealing with numbers as big as ``1e19``,
an absolute difference of ``10`` is negligible.

Another aspect that should be tested is the behavior of the code in exceptional circumstances.
Does it indeed raise :py:exc:`ArithmeticError` if the arguments are not of the same length?
Here is a test:

.. code-block:: python
   
   def test_dot_unequal_length():
       a = [1,2]
       b = [1,2,3]
       with pytest.raises(ArithmeticError):
           dot(a,b)

Here, :py:meth:`pytest.raises` is a *context manager* that will verify that :py:exc:`ArithmeticError`
is raise when its body is executed. 

.. note:: A detailed explanation about context managers see 
   https://jeffknupp.com/blog/2016/03/07/python-with-context-managers//

Note that you can easily make :meth:`et_dot.dot` raise other
exceptions, e.g. :exc:`TypeError` by passing in arrays of non-numeric types:

.. code-block:: python
   
   >>> dot([1,2],[1,'two'])
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/Users/etijskens/software/dev/workspace/ET-dot/et_dot.py", line 23, in dot
       d += a[i]*b[i]
   TypeError: unsupported operand type(s) for +=: 'int' and 'str'
   >>>

Note that it is not the product ``a[i]*b[i]`` for ``i=1`` that is wreaking havoc, but 
the addition of its result to ``d``.
 
At this point you might notice that even for a very simple and well defined function
as the dot product the amount of test code easily exceeds the amount of tested code 
by a factor of 5 or more. This is not at all uncommon. As the tested code here is an
isolated piece of code, you will probably leave it alone as soon as it passes the tests
and you are confident in the solution. If at some point, the :py:meth:`dot` would fail
you should write a test that reproduces the error and improve the solution so that it
passes the test.

When constructing software for more complex problems, there will very soon be many
interacting components and running the tests after modifying one of the components
will help you assure that all components still play well together, and spot problems
as soon as possible.
