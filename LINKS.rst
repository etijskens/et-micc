This page is a compilation of links I found interesting while learning Python and while solving
everyday problems in project management and maintenance, and of course scientific computing.
As I keep on learning this list evolves continuously :-)

"the most dangerous thought you can have as a creative person, is that you know what you
are doing." `Bret Victor - The Future of Programming <https://vimeo.com/71278954>`_.

For Beginners
-------------
* `De Programmeursleerling - Pieter Spronck <http://www.spronck.net/pythonbook/dutchindex.xhtml>`_ (in Dutch)
* `Slither into Python <https://www.slitherintopython.com>`_
* `Learn Python by building 5 games <https://www.youtube.com/watch?v=XGf2GcyHPhc>`_
* `How do I start learning Python? <https://automationpanda.com/2020/02/18/how-do-i-start-learning-python/>`_
* `Learn Python Programming <https://www.programiz.com/python-programming>`_

Python as a language
--------------------
* `What makes Python a great language? <https://stevedower.id.au/blog/python-a-great-language/>`_
* Python is known for being a language that’s easy to read, quick to develop in, and applicable to
  `a wide range of scenarios <https://realpython.com/what-can-i-do-with-python/>`_
* `Writing your first Python program <https://able.bio/SamDev14/writing-your-first-python-program--31a3607>`_
* `How long did it take you to learn Python <https://nedbatchelder.com/blog/202003/how_long_did_it_take_you_to_learn_python.html>`_
  Wait, don’t answer that. It doesn’t matter. Ned Batchelder

Software engineering
--------------------
* `Cognitive Biases In Software Development <http://smyachenkov.com/posts/cognitive-biases-software-development/>`_
* `What scientists must know about hardware to write fast code <https://biojulia.net/post/hardware/>`_
  A simplified view - but not over-simplified - on how hardware affects performance. Written with
  Julia in mind rather than Python, but the principles remain valid.
* `Clean architecture  <https://github.com/preslavmihaylov/booknotes/tree/master/architecture/clean-architecture>`_
* `The Grand Unified Theory of Software Architecture <https://danuker.go.ro/the-grand-unified-theory-of-software-architecture.html>`_

Python internals
----------------
* `How to run a python script <https://realpython.com/run-python-scripts/>`_
* `Cpython source code guide <https://realpython.com/cpython-source-code-guide/>`_
* `Know thy self - Methods and method binding - PyCon 2017 <https://youtu.be/byff9LhYXOg>`_
* `Namespaces and Scope in Python <https://realpython.com/python-namespaces-scope/>`_
* `The many ways to pass code to Python from the terminal <https://snarky.ca/the-many-ways-to-pass-code-to-python-from-the-terminal/>`_
* `Unpacking in Python: Beyond Parallel Assignment <https://stackabuse.com/unpacking-in-python-beyond-parallel-assignment/>`_
* `Pragmatic Unicode - Ned Batchelder - PyCon 2012 <https://nedbatchelder.com/text/unipain.html>`_
* `Tracing the Python GIL <https://www.maartenbreddels.com/perf/jupyter/python/tracing/gil/2021/01/14/Tracing-the-Python-GIL.html>`_
* `Constant folding in Python (constant expressions) <https://arpitbhayani.me/blogs/constant-folding-python>`_
* `Python behind the scenes <https://tenthousandmeters.com>`_
* `Python behind the scenes #7: how Python attributes work <https://tenthousandmeters.com/blog/python-behind-the-scenes-7-how-python-attributes-work/>`_
* `Unravelling the import statement <https://snarky.ca/unravelling-the-import-statement/>`_
* `Episode 40: How Python Manages Memory and Creating Arrays With np.linspace <https://realpython.com/podcasts/rpp/40/>`_
* `RealPython podcasts <https://realpython.com/podcasts/rpp/>`_
* `Syntactic sugar <https://snarky.ca/tag/syntactic-sugar/>`_
* `Python Pitfalls - Expecting The Unexpected <https://towardsdatascience.com/python-pitfalls-expecting-the-unexpected-2e595dd1306c>`_


Python for HPC
--------------
Here's a list of approaches that rely on low-lever programming languages, as C, C++ and Fortran, for
speeding up Python (sequential) code. Some of these approaches, e.g. `Numba <http://numba.pydata.org>`_
rely on automatic code transformation from Python, so there is no need to write low-level code yourself.

* `Performance Python: Seven Strategies for Optimizing Your Numerical Code <https://www.youtube.com/watch?v=zQeYx87mfyw>`_
* `High performance Python 1 <http://www.admin-magazine.com/HPC/Articles/High-Performance-Python-1>`_
* `High performance Python 2 <http://www.admin-magazine.com/HPC/Articles/High-Performance-Python-2>`_
* `High performance Python 3 <http://www.admin-magazine.com/HPC/Articles/High-Performance-Python-3>`_
* `Python Bindings: Calling C or C++ From Python <https://realpython.com/python-bindings-overview/#strengths-and-weaknesses_2>`_
* `Implementing C++ Virtual Functions in Cython <https://monadical.com/posts/virtual-classes-in-cython.html>`_
* `Wrapping C++ with Cython: intro <https://azhpushkin.me/posts/cython-cpp-intro>`_

Approaches mimicking or wrapping OpenMP and MPI:

* `Pymp – OpenMP-like Python Programming <https://www.admin-magazine.com/HPC/Articles/Pymp-OpenMP-like-Python-Programming?utm_source=ADMIN+Newsletter&utm_campaign=HPC_Update_135_2020-04-16_Pymp_–_OpenMP-like_Python_Programming>`_
  A really interesting concept, not as efficient as OpenMP itself (which incurs quite a bit of overhead
  itself), and, of course, limited to a single node. As the number of cores per node keeps increasing,
  pymp may be a good solution for problems that can do with a single node.
* `High performance Python 4 <http://www.admin-magazine.com/HPC/Articles/High-Performance-Python-4>`_
  Mpi4py, doing mpi from Python.

Other parallel processing approaches:

* `Sequential Execution, Multiprocessing, and Multithreading IO-Bound Tasks in Python <https://zacs.site/blog/linear-python.html>`_
* `Common Issues Using Celery (And Other Task Queues) <https://adamj.eu/tech/2020/02/03/common-celery-issues-on-django-projects/>`_
* `The Parallelism Blues: when faster code is slower <https://pythonspeed.com/articles/parallelism-slower/>`_
* `Dask <https://dask.org>`_
* `Visualize multi-threaded Python programs with an open source tool <https://opensource.com/article/21/3/python-viztracer?utm_medium=Email&utm_campaign=weekly&sc_cid=7013a000002vuw2AAA>`_

GPU

* `Accelerating Python on GPUs with nvc++ and Cython <https://developer.nvidia.com/blog/accelerating-python-on-gpus-with-nvc-and-cython/>`_

Concepts and ideas:

* `Does it ever make sense to use more concurrent processes than processor cores? <https://softwareengineering.stackexchange.com/questions/415413/does-it-ever-make-sense-to-use-more-concurrent-processes-than-processor-cores?utm_source=Iterable&utm_medium=email&utm_campaign=the_overflow_newsletter>`_
  You can have as many threads as you want as long as they're doing nothing.

Code modernization
------------------
* `Improving performance with SIMD intrinsics in three use cases <https://stackoverflow.blog/2020/07/08/improving-performance-with-simd-intrinsics-in-three-use-cases/?utm_source=Iterable&utm_medium=email&utm_campaign=the_overflow_newsletter>`_

Profiling
---------
* `Profiling python <http://www.admin-magazine.com/HPC/Articles/Profiling-Python-Code>`_
* `Python profiling with blackfire <https://hello.blackfire.io/python?utm_source=pycoder_weekly&utm_medium=newsletter&utm_campaign=q4_2019>`_
* `Python 3.9 StatsProfile <https://medium.com/@olshansky/python-3-9-statsprofile-my-first-oss-contribution-to-cpython-9dd6847eb802>`_
* `Profiling Python Code <https://www.admin-magazine.com/HPC/Articles/Profiling-Python-Code?utm_source=ADMIN+Newsletter&utm_campaign=HPC_Update_134_2020-03-19_MPI_Apps_with_Singularity&utm_medium=email>`_
* `Disassemble Your Python Code <https://florian-dahlitz.de/blog/disassemble-your-python-code>`_
* `Counting FLOPS and other CPU counters in Python <http://www.bnikolic.co.uk/blog/python/flops/2019/09/27/python-counting-events.html>`_
* `A Comprehensive Guide to Profiling Python Programs <https://medium.com/better-programming/a-comprehensive-guide-to-profiling-python-programs-f8b7db772e6>`_
* `Yet Another Python Profiler, but this time thread&coroutine&greenlet aware <https://github.com/sumerc/yappi>`_

Resource monitoring
-------------------
* `Remora <https://www.admin-magazine.com/HPC/Articles/Remora-Resource-Monitoring-for-Users?utm_source=ADMIN+Newsletter&utm_campaign=HPC_Update_143_2020-12-10_Remora%3A_Resource_Monitoring+_or_Users&utm_medium=email>`_
* `REMORA: REsource MOnitoring for Remote Applications <https://github.com/TACC/remora>`_

Python idioms and readability
-----------------------------
* `The Elements of Python Stylez <https://github.com/amontalenti/elements-of-python-style>`_
* `Practical decorators <https://www.youtube.com/watch?v=MjHpMCIvwsY&t=1475s>`_ Reuven Lerner
* `Elegant Solutions For Everyday Python Problems - PyCon 2018 <https://youtu.be/WiQqqB9Mlk>`_
* `Yes, It's Time to Learn Regular Expressions - PyCon 2017 <https://youtu.be/abrcJ9MpF60>`_
* `Decorators, unwrapped How do they work - PyCon 2017 <https://youtu.be/UBSyD1RkOX0>`_
* `Decorators and descriptors decoded - PyCon 2017 <https://youtu.be/81S01c9zytE>`_
* `The Dictionary Even Mightier - PyCon 2017 <https://youtu.be/66P5FMkWoVU>`_
* `Looping Like a Pro in Python - PyCon 2017 <https://youtu.be/81S01c9zytE>`_
* `Readable Regular Expressions - PyCon 2017 <https://youtu.be/0sOfhhduqks>`_
* `Passing Exceptions 101 Paradigms in Error Handling - PyCon 2017 <https://youtu.be/BMtJbrvwlmo>`_
* `Readability Counts - PyCon 2017 <https://youtu.be/cbirFDKtT2w>`_
* `Modern Python Dictionaries: A confluence of a dozen great ideas - PyCon 2017 <https://youtu.be/npw4s1QTmPg>`_
* `Gang of 4 inspired decorators <https://www.nacnez.com/gof-inspired-decorators.html>`_
* `Python module of the week <https://pymotw.com/2/contents.html>`_
* `Type hints for busy programmers <https://inventwithpython.com/blog/2019/11/24/type-hints-for-busy-python-programmers/>`_
* `Exceptions <https://orbifold.xyz/raising-exceptions.html>`_
* `Python Tips and Tricks, You Haven't Already Seen - part 1 <https://martinheinz.dev/blog/1>`_
* `Python Tips and Tricks, You Haven't Already Seen - part 2 <https://martinheinz.dev/blog/4>`_
* `30 Python Best Practices, Tips, And Tricks <https://towardsdatascience.com/30-python-best-practices-tips-and-tricks-caefb9f8c5f5>`_
* `pythonic things <https://access.redhat.com/blogs/766093/posts/2802001>`_
* `71 Python Code Snippets for Everyday Problems <https://therenegadecoder.com/code/python-code-snippets-for-everyday-problems/>`_
* `Clean Code Concepts Adapted for Python <https://github.com/zedr/clean-code-python>`_
* `The place of the 'is' syntax in Python <https://utcc.utoronto.ca/~cks/space/blog/python/IsSyntaxPlace>`_
* `5 Things You're Doing Wrong When Programming in Python <https://www.youtube.com/watch?v=fMRzuwlqfzs>`_
* `10 Python Tips and Tricks For Writing Better Code <https://www.youtube.com/watch?v=C-gEQdGVXbk>`_
* `Tour of Python Itertools <https://towardsdatascience.com/tour-of-python-itertools-2af84db18a5e>`_
* `Getting the most out of Python collections <https://sourcery.ai/blog/effective-collection-handling/>`_
* `Unpacking in Python: Beyond Parallel Assignment <https://stackabuse.com/unpacking-in-python-beyond-parallel-assignment/>`_
* `When Python Practices Go Wrong <https://rhodesmill.org/brandon/slides/2019-11-codedive/>`_ About the
  use of exec() and eval(). A presentation, so, the logic isn`t always obvious, but definitely an
  interesting topic. Here's the corresponding video `When Python Practices Go Wrong - Brandon Rhodes - code::dive 2019 <https://www.youtube.com/watch?v=S0No2zSJmks>`_
* `The Curious Case of Python's Context Manager <https://rednafi.github.io/digressions/python/2020/03/26/python-contextmanager.html>`_
* `Demystifying Python’s Descriptor Protocol <https://deepsource.io/blog/demystifying-python-descriptor-protocol/>`_
* `Why You Should Use More Enums In Python <https://florian-dahlitz.de/blog/why-you-should-use-more-enums-in-python>`_
* `Regular Expressions: Regexes in Python (Part 1) <https://realpython.com/regex-python/>`_
* `Regular Expressions: Regexes in Python (Part 2) <https://realpython.com/regex-python-part-2/>`_
* `Novice to Advanced RegEx in Less-than 30 Minutes + Python <https://www.youtube.com/watch?v=GyJtxd14DTc>`_
* `10 Awesome Pythonic One-Liners Explained <https://dev.to/devmount/10-awesome-pythonic-one-liners-explained-3doc>`_
* `Stop writing classes <https://www.youtube.com/watch?v=o9pEzgHorH0>`_
* `Generators, Iterables, Iterators in Python: When and Where <https://www.pythonforthelab.com/blog/generators-iterables-iterators-python-when-and-where/>`_
* `New Features in Python 3.9 You Should Know About <https://medium.com/@martin.heinz/new-features-in-python-3-9-you-should-know-about-14f3c647c2b4>`_
* `The Curious Case of Python's Context Manager <https://rednafi.github.io/digressions/python/2020/03/26/python-contextmanager.html>`_
* `Python 101 – Working with Strings <https://www.blog.pythonlibrary.org/2020/04/07/python-101-working-with-strings/>`_
* `A Guide to Python Lambda Functions <https://adamj.eu/tech/2020/08/10/a-guide-to-python-lambda-functions/>`_
* `Pythonic code review <https://access.redhat.com/blogs/766093/posts/2802001>`_
* `Python args and kwargs: Demystified <https://realpython.com/courses/python-kwargs-and-args/>`_
* `Python Dictionary Iteration: Advanced Tips & Tricks <https://realpython.com/courses/python-dictionary-iteration/>`_
* `Python Code style and pythonic idioms <https://docs.python-guide.org/writing/style/>`_
* `Learn something new about Python every day in less than 1 minute <https://www.youtube.com/c/PythonIn1Minute/videos>`_
* `The pass Statement: How to Do Nothing in Python <https://realpython.com/python-pass/>`_
* `73 Examples to Help You Master Python's f-strings <https://miguendes.me/amp/73-examples-to-help-you-master-pythons-f-strings>`_

Useful packages
---------------
* `safer: a safer file writer <https://medium.com/@TomSwirly/%EF%B8%8F-safer-a-safer-file-writer-%EF%B8%8F-5fe267dbe3f5>`_
* `sproc: subprocesses for subhumanses <https://medium.com/@TomSwirly/%EF%B8%8F-sproc-subprocesseses-for-subhumanses-dbee42f22af5>`_
* `The 22 Most-Used Python Packages in the World <https://medium.com/better-programming/the-22-most-used-python-packages-in-the-world-7020a904b2e>`_
* `Five Amazing Python Libraries you should be using! <https://youtu.be/eILeIEE3C8c>`_
* `The most underrated python packages <https://towardsdatascience.com/the-most-underrated-python-packages-e22bf6049b5e>`_
* `No Really, Python's Pathlib is Great <https://rednafi.github.io/digressions/python/2020/04/13/python-pathlib.html>`_
* `Python 101 – Creating Multiple Processes <https://www.blog.pythonlibrary.org/2020/07/15/python-101-creating-multiple-processes/>`_
* `Python Packages: Five Real Python Favorites <https://realpython.com/python-packages/>`_
* `Python and PDF: A Review of Existing Tools <https://johannesfilter.com/python-and-pdf-a-review-of-existing-tools/>`_
* `A cross-platform Python module for copy and paste clipboard functions <https://github.com/asweigart/pyperclip>`_
* `The Python pickle Module: How to Persist Objects in Python <https://realpython.com/python-pickle-module/>`_
* `Pickle’s nine flaws <https://nedbatchelder.com/blog/202006/pickles_nine_flaws.html>`_
* `Taichi:a programming language designed for high-performance computer graphics <https://github.com/taichi-dev/taichi>`_
* `rich: rich text and beautiful formatting in the terminal <https://github.com/willmcgugan/rich>`_
* `Awesome pattern matching (apm) for Python <https://github.com/scravy/awesome-pattern-matching>`_
* `Scheduling All Kinds of Recurring Jobs with Python <https://towardsdatascience.com/scheduling-all-kinds-of-recurring-jobs-with-python-b8784c74d5dc>`_

Exceptions
----------
* `Better Python tracebacks with Rich <https://www.willmcgugan.com/blog/tech/post/better-python-tracebacks-with-rich/>`_
* `Write Unbreakable Python <https://jessewarden.com/2020/03/write-unbreakable-python.html>`_
* `pretty-errors: Prettifies Python exception output to make it legible <https://github.com/onelivesleft/PrettyErrors/>`_
* `Python KeyError Exceptions and How to Handle Them <https://realpython.com/courses/python-keyerror/>`_

Type checking in Python
-----------------------
* `Type-checked Python in the real world - PyCon 2018 <https://www.youtube.com/watch?v=pMgmKJyWKn8>`_
  mypy
* `Applying mypy to real world projects <http://calpaterson.com/mypy-hints.html>`_
* `Types at the Edges in Python <https://blog.meadsteve.dev/programming/2020/02/10/types-at-the-edges-in-python/>`_
* `Exhaustiveness (enum) Checking with Mypy <https://hakibenita.com/python-mypy-exhaustive-checking>`_

Design patterns
---------------
* `Design Patterns in Python for the Untrained Eye - PyCon 2019 <http://34.212.143.74/s201911/pycon2019/docs/design_patterns.html>`_
* `Python patters <https://python-patterns.guide>`_
* `Refactoring and Design patterns <https://refactoring.guru>`_
* `Pyton anti-patterns <https://docs.quantifiedcode.com/python-anti-patterns/index.html>`_
* `Coding problems <https://github.com/MTrajK/coding-problems>`_

Testing
-------
* `Getting Started Testing: pytest edition <https://nedbatchelder.com/text/test3.html>`_
* `tox nox and invoke <https://www.youtube.com/watch?v=-BHverY7IwU>`_  Break the Cycle:
  Three excellent Python tools to automate repetitive tasks
* `Hypothesis <https://hypothesis.readthedocs.io/>`_
* `Escape from auto-manual testing with Hypothesis! <https://youtu.be/SmBAl34RV4M?list=PLPbTDk1hBo3xof51R8pk3kP1BVBuMYP9c>`_
* `Beyond Unit Tests: Taking Your Testing to the Next Level - PyCon 2018 <https://www.youtube.com/watch?v=MYucYon2-lk>`_
* `How to mock in Python? – (almost) definitive guide <https://breadcrumbscollector.tech/how-to-mock-in-python-almost-definitive-guide/>`_
* `Why your mock doesn't work <https://nedbatchelder.com/blog/201908/why_your_mock_doesnt_work.html>`_
* `Visual Testing with PyCharm and pytest - PyCon 2018 <https://www.youtube.com/watch?v=FjojZxDZscQ>`_
* `"WHAT IS THIS MESS?" - Writing tests for pre-existing code bases - PyCon 2018 <https://www.youtube.com/watch?v=LDdUuoI_lIg>`_
* `Python Testing 201 with pytest <https://www.mattlayman.com/blog/2019/python-testing-201-with-pytest/>`_
* `8 great pytest plugins <https://opensource.com/article/18/6/pytest-plugins>`_
* `Pytest Features, That You Need in Your (Testing) Life <https://martinheinz.dev/blog/7>`_
* `An Introduction To Test Driven Development <https://able.bio/SamDev14/an-introduction-to-test-driven-development--69muplk>`_
* `How To Write Tests For Python <https://able.bio/SamDev14/how-to-write-tests-for-python--22m3q1n>`_
* `How I’m testing in 2020 <https://www.b-list.org/weblog/2020/feb/03/how-im-testing-2020/>`_
* `Building Good Tests <https://salmonmode.github.io/2019/03/29/building-good-tests.html>`_
* `Property-based tests for the Python standard library (and builtins) <https://github.com/Zac-HD/stdlib-property-tests>`_
* `a pytest plugin designed for analyzing resource usage <https://github.com/CFMTech/pytest-monitor>`_
* `ward - A modern Python test framework <https://github.com/darrenburns/ward>`_
* `The Clean Architecture in Python - How to write testable and flexible code <https://breadcrumbscollector.tech/the-clean-architecture-in-python-how-to-write-testable-and-flexible-code/>`_
* `Effective Python Testing With Pytest <https://realpython.com/pytest-python-testing>`_
* `Document your tests <https://hynek.me/articles/document-your-tests/>`_
* `15 amazing pytest plugins <https://testandcode.com/116>`_ and more (an episode on an interesting blog).
* `ARRANGE-ACT-ASSERT: A PATTERN FOR WRITING GOOD TESTS <https://automationpanda.com/2020/07/07/arrange-act-assert-a-pattern-for-writing-good-tests/>`_
* `There's no one right way to test your code <https://mattsegal.dev/alternate-test-styles.html>`_
* `Why you should document your tests <https://hynek.me/articles/document-your-tests/>`_
* `Property-Based Testing with hypothesis, and associated use cases <https://bytes.yingw787.com/posts/2021/02/02/property_based_testing/>`_
* `Testing Python Applications with Pytest [Guide] <https://stribny.name/blog/pytest/>`_
* `Learning Python Test Automation <https://automationpanda.com/2020/11/09/learning-python-test-automation/amp/>`_
  These days, there’s a wealth of great content on Python testing. Here’s a brief reference to help you get started.
* `How to write doctests in Python <https://www.digitalocean.com/community/tutorials/how-to-write-doctests-in-python>`_

Debugging
---------
* `pdb - The Python debugger <https://docs.python.org/3/library/pdb.html>`_
* `Python debugging with pdb <https://realpython.com/python-debugging-pdb/>`_
* `Python 101 – Debugging Your Code with pdb <https://www.blog.pythonlibrary.org/2020/07/07/python-101-debugging-your-code-with-pdb/>`_
* `tutorial on sys.settrace <https://pymotw.com/2/sys/tracing.html>`_
* `Liran Haimovitch - Understanding Python’s Debugging Internals - PyCon 2019 <https://www.youtube.com/watch?v=QU158nGABxI&t=765s&pbjreload=10>`_
* `bdb - debugger framework <https://docs.python.org/3.8/library/bdb.html>`_
* `pudb for Visual Debugging <https://realpython.com/python-packages/#pudb-for-visual-debugging>`_
* `Cyberbrain: Python debugging, redefined <https://github.com/laike9m/Cyberbrain>`_
* `Python Traceback (Error Message) Printing Variables <https://github.com/andy-landy/traceback_with_variables>`_
* `Introspection in Python <https://anvil.works/blog/introspection-in-python>`_
* `Learn to debug code with the GNU Debugger <https://opensource.com/article/21/3/debug-code-gdb?utm_medium=Email&utm_campaign=weekly&sc_cid=7013a000002vsCLAAY>`_
* `GDBGUI - A browser-based frontend to gdb <https://www.gdbgui.com>`_
* `Debugging Python and C(++) extensions with gdb and pdb <https://www.researchgate.net/figure/Debugging-both-C-extensions-and-Python-code-with-gdb-and-pdb_fig2_220307949>`_

Logging
-------
* `Python logging tutorial <http://www.patricksoftwareblog.com/python-logging-tutorial/>`_
* `Writing custom profilers for Python <https://pythonspeed.com/articles/custom-python-profiler/>`_
* `Do not log <https://sobolevn.me/2020/03/do-not-log>`_
* `Understanding Python's logging library <https://blog.urbanpiper.com/understanding-python-logging-library/>`_


Profiling
---------
* `Python timer functions <https://realpython.com/python-timer/>`_

Scientific Python
-----------------
* `Array Oriented Programming with Python NumPy <https://towardsdatascience.com/array-oriented-programming-with-python-numpy-e0190dd6ab65>`_
* `Numeric and Scientific Python Packages built on Numpy <https://wiki.python.org/moin/NumericAndScientific>`_
* `Symbolic Maths in Python <https://alexandrugris.github.io/maths/2017/04/30/symbolic-maths-python.html>`_
* `How to use HDF5 files in Python <https://www.pythonforthelab.com/blog/how-to-use-hdf5-files-in-python/>`_
* `A free course on Numpy <https://www.youtube.com/playlist?list=PL9oKUrtC4VP6gDp1Vq3BzfViO0TWgR0vR>`_
* `Generating Stl Models with Python (CAD) <https://micronote.tech/2020/12/Generating-STL-Models-with-Python/>`_

Machine learning and datascience
--------------------------------
* `Scikit-learn, wrapping your head around machine learning - PyCon 2019 <https://www.youtube.com/watch?v=kTdt0P0e3Qc>`_
* `Applied Deep Learning for NLP Using PyTorch <https://youtu.be/VBM1u-UIoI0>`_
* `Data Science Best Practices with pandas - PyCon 2019 <https://www.youtube.com/watch?v=ZjrUmNq41Eo>`_
* `Thinking like a Panda: Everything you need to know to use pandas the right way <https://www.youtube.com/watch?v=ObUcgEO4N8w>`_
* `Plotnine: Grammar of Graphics for Python <https://www.datascienceworkshops.com/blog/plotnine-grammar-of-graphics-for-python/>`_
* `Top 10 Python libraries of 2019 <https://tryolabs.com/blog/2019/12/10/top-10-python-libraries-of-2019/>`_
* `Top 10 Python Packages for Machine Learning <https://www.activestate.com/blog/top-10-python-machine-learning-packages/?utm_source=pycoders-weekly&utm_medium=email&utm_content=newsletter-2020-03-17-top-10-ML-packages&utm_campaign=as-blog>`_
* `streamz: Build Pipelines to Manage Continuous Streams of Data <https://github.com/python-streamz/streamz/blob/master/docs/source/index.rst>`_
* `nfstream - A flexible network data analysis framework <https://github.com/aouinizied/nfstream>`_
* `A series how to turn machine learning models into production-ready software solutions <https://www.youtube.com/playlist?list=PLx8omXiw3n9y26FKZLV5ScyS52D_c29QN>`_
* `A free course on Python Pandas <https://www.youtube.com/playlist?list=PL9oKUrtC4VP7ry0um1QOUUfJBXKnkf-dA>`_
* `Neural Networks Explained from Scratch using Python <https://youtu.be/9RN2Wr8xvro>`_
* `Machine learning made easy withe Python <https://opensource.com/article/21/1/machine-learning-python?utm_medium=Email&utm_campaign=weekly&sc_cid=7013a0000026SeIAAU>`_

CLIs and scripting
------------------
* `Building a CLI for Firmware Projects using Invoke <https://interrupt.memfault.com/blog/building-a-cli-for-firmware-projects>`_
* `Click <https://click.palletsprojects.com/en/7.x/>`_
* `QUICK: A real quick GUI generator for click <https://github.com/szsdk/quick>`_
* `When laziness is efficient: Make the most of your command line <https://stackoverflow.blog/2020/02/12/when-laziness-is-efficient-make-the-most-of-your-command-line/?utm_source=Iterable&utm_medium=email&utm_campaign=the_overflow_newsletter&utm_content=02-19-20>`_
* `Typer: build CLIs with Python type hints <https://typer.tiangolo.com/>`_
* `Messing with the python shell <https://www.kbairak.net/programming/python/2021/02/01/messing-with-the-python-shell.html>`_
* `Converting shell scripts to python scripts <https://github.com/jroose/shtk>`_
* `a Python shell environment that combines the expressiveness of shell pipelines with the power of python iterators <https://github.com/redhog/pieshell>`_
* `build a command line text editor with Python and curses <https://wasimlorgat.com/editor.html>`_
* `Show progress in your Python apps with tqdm <https://opensource.com/article/20/12/tqdm-python>`_
* `Questionary is a Python library for effortlessly building pretty command line interfaces <https://github.com/tmbo/questionary>`_
* `Command Line Interface Guidelines <https://clig.dev>`_
* `iterm2 plugins written in python <https://cgamesplay.com/post/2020/11/25/iterm-plugins/>`_

GUI
---
* `Use PyQt's QThread to Prevent Freezing GUIs <https://realpython.com/python-pyqt-qthread/>`_

Packaging
---------
* `Inside the Cheeseshop: How Python Packaging Works - PyCon 2018 <https://youtu.be/AQsZsgJ30AE>`_ historical overview with thorough explanation
* `Share Your Code! Python Packaging Without Complication - PyCon 2017 <https://youtu.be/qOH-h-EKKac>`_
* `A Python alternative to Docker <https://www.mattlayman.com/blog/2019/python-alternative-docker/>`_
* `The Python Packaging Ecosystem <http://www.curiousefficiency.org/posts/2016/09/python-packaging-ecosystem.html>`_
* `Python Packaging Is Good Now <https://glyph.twistedmatrix.com/2016/08/python-packaging.html>`_
* `Conda: Myths and Misconceptions <https://jakevdp.github.io/blog/2016/08/25/conda-myths-and-misconceptions/>`_
* `The private PyPI server powered by flexible backends <https://github.com/pywharf/pywharf>`_
* `Packaging without setup.py <https://pgjones.dev/blog/packaging-without-setup-py-2020/>`_
* `PDM - Python Development Master <https://github.com/frostming/pdm>`_
* `Python Packaging Made Better: An Intro to Python Wheels <https://realpython.com/python-wheels/>`_
* `Options for packaging your Python code: Wheels, Conda, Docker, and more <https://pythonspeed.com/articles/distributing-software/>`_
* `What the heck is pyproject.toml? <https://snarky.ca/what-the-heck-is-pyproject-toml/>`_

Graphics
--------
* `matplotlib <https://matplotlib.org>`_
* `"Cyberpunk style" for matplotlib plots <https://github.com/dhaitz/mplcyberpunk>`_
* `Effectively using matplotlib <https://pbpython.com/effective-matplotlib.html>`_
* `ModernGL : a python wrapper over OpenGL 3.3+ <https://github.com/moderngl/moderngl>`_
* `Magnum: Lightweight and modular C++11/C++14 graphics middleware for games and data visualization <https://doc.magnum.graphics/python/examples/>`_
* `Grammar of graphics for Pyhon (using plotnine and pandas) <https://www.datascienceworkshops.com/blog/plotnine-grammar-of-graphics-for-python/>`_
* `plotly Express <https://pbpython.com/plotly-look.html>`_
* `widgets in matplotlib <https://kapernikov.com/ipywidgets-with-matplotlib/>`_
* `How to build beautiful plots with Python and Seaborn <https://livecodestream.dev/post/how-to-build-beautiful-plots-with-python-and-seaborn/>`_
* `HiPlot is a lightweight interactive visualization tool to help  discover correlations and patterns in high-dimensional data <https://github.com/facebookresearch/hiplot>`_

Installing packages
-------------------
* `A quick-and-dirty guide on how to install packages for Python <https://snarky.ca/a-quick-and-dirty-guide-on-how-to-install-packages-for-python/>`_

Tools
-----
* `Software Development Checklist for Python Applications <http://www.patricksoftwareblog.com/software-development-checklist-for-python-applications/>`_
* `IPython and Jupyter in Depth: High productivity, interactive Python <https://www.youtube.com/watch?v=hgiNlxUN2V0>`_ Matthias Bussonier
* `Faster Python Programs - Measure, don't Guess - PyCon 2019 <https://youtu.be/EcGWDNlGTNg>`_
* `Python Tooling Makes a Project Tick <https://medium.com/georgian-impact-blog/python-tooling-makes-a-project-tick-181d567eea44>`_
* `Life Is Better Painted Black, or: How to Stop Worrying and Embrace Auto-Formatting <https://youtu.be/esZLCuWs_2Y>`_
* `Using GitHub, Travis CI, and Python to Introduce Collaborative Software Development - PyCon 2018 <https://www.youtube.com/watch?v=cxTXJ3N91s0>`_
* `What's in your pip toolbox - PyCon 2017 <https://youtu.be/HOZxSmsbk4M>`_
* `How can I get tox and poetry to work together to support testing multiple versions of a Python dependency? <https://stackoverflow.com/questions/59377071/how-can-i-get-tox-and-poetry-to-work-together-to-support-testing-multiple-versio>`_
* `Understanding Best Practice Python Tooling by Comparing Popular Project Templates <https://medium.com/better-programming/understanding-best-practice-python-tooling-by-comparing-popular-project-templates-6eba49229106>`_
* `My unpopular meaning about Black code formatter <https://luminousmen.com/post/my-unpopular-opinion-about-black-code-formatter>`_
* `Python static analysis tools <https://luminousmen.com/post/python-static-analysis-tools>`_
* `Leverage Sublime project folders to ease your work <https://storiesinmypocket.com/articles/leverage-sublime-project-folders-ease-your-work/>`_
* `Deep dive into how pyenv actually works by leveraging the shim design pattern <https://mungingdata.com/python/how-pyenv-works-shims/>`_
* `Explore binaries using this full-featured Linux tool <https://opensource.com/article/21/1/linux-radare2?utm_medium=Email&utm_campaign=weekly&sc_cid=7013a0000026SeIAAU>`_
* `How to write a configuration file in python <https://towardsdatascience.com/from-novice-to-expert-how-to-write-a-configuration-file-in-python-273e171a8eb3>`_
* `How to automatically set up a development machine with Ansible <https://stribny.name/blog/ansible-dev/>`_

git and other VCS

* `Introduction to Git In 16 Minutes <https://vickyikechukwu.hashnode.dev/introduction-to-git-in-16-minutes?utm_source=tldrnewsletter>`_
* `9 useful tricks of git branch <https://gitbetter.substack.com/p/9-useful-tricks-of-git-branch-you>`_
* `gitutor <https://github.com/artemisa-mx/gitutor>`_
* `Git Commands to Live By - The cheat sheet that goes beyond Git basics <https://medium.com/better-programming/git-commands-to-live-by-349ab1fe3139>`_
* `Things You Want to Do in Git and How to Do Them <https://stu2b50.dev/posts/things-you-wante9665>`_
* `Helpful git commands for beginners <https://dev.to/s2engineers/helpful-git-commands-for-beginners-40bm>`_
* `understanding git: commits are snapshots not diffs <https://github.blog/2020-12-17-commits-are-snapshots-not-diffs/>`_
* `Pijul, a sound and fast distributed version control system based on a mathematical theory of asynchronous work. <https://nest.pijul.com/pijul/pijul>`_
* `Getting The Most Out Of Git <https://www.smashingmagazine.com/2021/02/getting-the-most-out-of-git/?utm_source=tldrnewsletter>`_
* `Git is my buddy: Effective Git as a solo developer <https://mikkel.ca/blog/git-is-my-buddy-effective-solo-developer/?utm_source=tldrnewsletter>`_

Development environment, developement workflow
----------------------------------------------
* `pyenv+poetry+pipx <https://jacobian.org/2019/nov/11/python-environment-2020/>`
* https://sourcery.ai/blog/python-best-practices/
* https://pypi.org/project/create-python-package/ a micc 'light'
* `Managing Python Environments <https://www.pluralsight.com/tech-blog/managing-python-environments/>`_
* `Using Sublime Text for python <https://storiesinmypocket.com/articles/using-sublime-text-python/>`_
* `How to Set Up a Python Project For Automation and Collaboration <https://eugeneyan.com/writing/setting-up-python-project-for-automation-and-collaboration/>`_
* `Hypermodern Python <https://cjolowicz.github.io/posts/hypermodern-python-01-setup/>`_
* `Thoughts on where tools fit into a workflow <https://snarky.ca/thoughts-on-a-tooling-workflow/>`_
* `poetry <https://github.com/python-poetry/poetry>`_
* `Blazing fast CI with GitHub Actions, Poetry, Black and Pytest <https://medium.com/@vanflymen/blazing-fast-ci-with-github-actions-poetry-black-and-pytest-9e74299dd4a5>`_
* `Rewriting your git history, removing files permanently - cheatsheet & guide <https://blog.gitguardian.com/rewriting-git-history-cheatsheet/>`_
* `pipupgrade <https://github.com/achillesrasquinha/pipupgrade>`_
* `How to Set Environment Variables in Linux and Mac: The Missing Manual <https://doppler.com/blog/how-to-set-environment-variables-in-linux-and-mac>`_

Problem solving
---------------
* `The mental game of Python - Raymond Hettinger - pybay 2019 <https://www.youtube.com/watch?v=UANN2Eu6ZnM>`_

Documentation
-------------
* `Practical Sphinx - PyCon 2018 <https://youtu.be/0ROZRNZkPS8>`_
* `Write the Docs is a global community of people who care about documentation <https://www.writethedocs.org>`_
* `How documentation works, and how to make it work for your project - PyCon 2017 <https://youtu.be/azf6yzuJt54>`_
* `How to document Python code with Sphinx <https://opensource.com/article/19/11/document-python-sphinx>`_
    interesting section about tox
* `Scott Meyers' advise on writing <https://scottmeyers.blogspot.com/2013/01/effective-effective-books.html>`_

Django
------
* `Understanding django <https://www.mattlayman.com/understand-django/browser-to-django/>`_

Fortran/C/C++ Syntax
--------------------
* `<https://www.fortran90.org>`_
* `<http://www.cplusplus.com>`_
* `<http://cppreference.com>`_

C++
---
* `A friendly guide to the syntax of C++ method pointers <https://opensource.com/article/21/2/ccc-method-pointers?utm_medium=Email&utm_campaign=weekly&sc_cid=7013a000002vqnQAAQ>`_
* `How Many Strings Does C++ Have? <https://blogs.msmvps.com/gdicanio/2018/05/28/how-many-strings-does-c-have/>`_

Compilers
---------

* `CppCon 2017: Matt Godbolt “What Has My Compiler Done for Me Lately? Unbolting the Compiler's Lid” <https://youtu.be/bSkpMdDe4g4>`_
* `A Complete Guide to LLVM for Programming Language Creators <https://mukulrathi.co.uk/create-your-own-programming-language/llvm-ir-cpp-api-tutorial/>`_

Notebooks
---------
* `Jupyter Notebooks in the IDE <https://towardsdatascience.com/jupyter-notebooks-in-the-ide-visual-studio-code-versus-pycharm-5e72218eb3e8>`_

Containers
----------
* `Building Python Data Science Container using Docker <https://faizanbashir.me/building-python-data-science-container-using-docker-c8e346295669>`_

Windows
-------
* `Using WSL to Build a Python Development Environment on Windows <https://pbpython.com/wsl-python.html>`_
  This is promising: maybe we finally have a an environment on Windows with a minimal difference from
  Linux an MacOSX.

Linux
-----
* `2020: The Year of the Linux Desktop - Moving from Macbook to Linux <https://monadical.com/posts/moving-to-linux-desktop.html>`_

Programming blogs
-----------------
* `julien danjou <https://julien.danjou.info>`_
* `Patrick's software blog <http://www.patricksoftwareblog.com/>`_
* `Ruslan Spivak <https://ruslanspivak.com/>`_
* `<https://rhodesmill.org/brandon/>`_
* `testandcode <https://testandcode.com>`_

QUOTES
------
* "The code you write makes you a programmer. The code you delete makes you a good one.
  The code you don't have to write makes you a great one." - Mario Fusco
* “It's hard enough to find an error in your code when you're looking for it;
  it's even harder when you've assumed your code is error-free.” - Steve McConnell