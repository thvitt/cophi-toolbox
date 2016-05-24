Contributing to the Cophi Toolbox
=================================

Setup
-----

After cloning the project run `pip install -e .` to install the project with all dependencies.

Guidelines
----------

This is more a list of hints & suggestions

Code
""""

should be put into modules under cophi_toolbox. 

Documentation
"""""""""""""

Each module, class, function, and method should have a docstring. Docstrings should follow the `Google Style Guide`_, they are intended to be handled by the Napoleon_ Sphinx extension. Function docstrings should describe the arguments and their expected types, and also the return types.

Tests
"""""

Tests should either be doctests_ and thus directly included in the respective docstrings, or tests that can be run using the nose test framework, see the `nose introduction`_. It's really worthwhile to write tests, so please do.


Dependencies
""""""""""""
Dependencies should be listed in the setup.py file.




.. _`Google Style Guide`: http://google.github.io/styleguide/pyguide.html?showone=Comments#Comments
.. _Napoleon: http://www.sphinx-doc.org/en/stable/ext/napoleon.html
.. _doctests: https://docs.python.org/3.5/library/doctest.html#unittest-api
.. _`nose introduction`: http://pythontesting.net/framework/nose/nose-introduction/
