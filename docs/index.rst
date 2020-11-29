Python lspci parser
===================

:ref:`genindex` - :ref:`modindex` - :ref:`search`

.. image:: https://img.shields.io/pypi/v/pylspci.svg
   :target: https://pypi.org/project/pylspci

.. image:: https://img.shields.io/pypi/l/pylspci.svg
   :target: https://pypi.org/project/pylspci

.. image:: https://img.shields.io/pypi/format/pylspci.svg
   :target: https://pypi.org/project/pylspci

.. image:: https://img.shields.io/pypi/pyversions/pylspci.svg
   :target: https://pypi.org/project/pylspci

.. image:: https://img.shields.io/pypi/status/pylspci.svg
   :target: https://pypi.org/project/pylspci

.. image:: https://gitlab.com/Lucidiot/pylspci/badges/master/pipeline.svg
   :target: https://gitlab.com/Lucidiot/pylspci/pipelines

.. image:: https://codecov.io/gl/Lucidiot/pylspci/branch/master/graph/badge.svg
   :target: https://codecov.io/gl/Lucidiot/pylspci

.. image:: https://img.shields.io/badge/badge%20count-10-brightgreen.svg
   :target: https://gitlab.com/Lucidiot/pylspci

A Python parser for the ``lspci`` command from the pciutils_ package.

.. _pciutils: http://mj.ucw.cz/sw/pciutils/

Command-line interface
----------------------

An executable script named ``pylspci`` is available, and acts as a wrapper
around ``lspci`` that can produce JSON output. ::

   $ pylspci -nn
   [{
     "slot": {"domain": 0, "bus": 0, "device": 1, "function": 3},
     "device": {"id": 9248, "name": "Name A"},
     ...
   }]

See ``pylspci --help`` and the `CLI docs <cli>`_ to learn more.

Parsing in Python
-----------------

To parse ``lspci -nnmm``, use the
:class:`SimpleParser <pylspci.parsers.simple.SimpleParser>`.
To parse ``lspci -nnmmvvvk``, use the
:class:`VerboseParser <pylspci.parsers.verbose.VerboseParser>`.

.. code:: python

   >>> from pylspci.parsers import SimpleParser
   >>> SimpleParser.run()
   [Device(slot=Slot('0000:00:01.3'), name=NameWithID('Name A [2420]'), ...),
    Device(slot=Slot('0000:00:01.4'), name=NameWithID('Name B [0e54]'), ...)]

Custom arguments
^^^^^^^^^^^^^^^^

.. code:: python

   >>> from pylspci.command import IDResolveOption
   >>> from pylspci import parser
   >>> parser.run(
   ...     hide_single_domain=False,
   ...     id_resolve_option=IDResolveOption.NameOnly,
   ... )
   [Device(slot=Slot('0000:00:01.3'), name=NameWithID('Name A'), ...),
    Device(slot=Slot('0000:00:01.4'), name=NameWithID('Name B'), ...)]

Learn more
----------

.. toctree::
   cli
   data
   command
   low
   contributing
