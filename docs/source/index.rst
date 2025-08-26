.. role:: python(code)
   :language: python

.. role:: rst(code)
   :language: rst

SphinxRun documentation
=======================

SphinxRun registers a new :rst:dir:`.. run:: <run>` directive to execute python commands dynamically while building a sphinx documentation.
It can be used to generate documentation artifacts such as figures or to dynamic content.

Example
-------

.. literalinclude:: example.py

renders as:

.. autoclass:: example.Wrapper
   :members:

The environement persists across calls within the scope of a document.

Installation
------------

Install the package:

.. code:: shell

   pip install sphinxrun
   # or
   uv add --dev sphinxrun

Then add the extension to the sphinx configuration:

.. code:: python

   extensions = [
      ...
      "sphinxrun"
   ]

Usage
-----

.. rst:directive:: run

   Directive to execute code.

   The interpreter persists through the scope of a document, so imports and global variables can be reused across multiple directives.
   More specifically, the scope corresponds to a single `.rst` file (or it parent when included) or each entry of an autosummary.

   The code can generate content to insert at the position of the directive using :func:`sphinxrun.show`.
   Note: the ``sphinxrun`` module is automatically imported.

   .. rubric:: Options

   .. rst:directive:option:: group
      :type:

      Specify a command group name.
      The commands from each group are run in separate processes.


.. autofunction:: sphinxrun.show
