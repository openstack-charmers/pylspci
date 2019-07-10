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

.. image:: https://requires.io/github/Lucidiot/pylspci/requirements.svg?branch=master
   :target: https://requires.io/github/Lucidiot/pylspci/requirements/?branch=master

.. image:: https://img.shields.io/github/last-commit/Lucidiot/pylspci.svg
   :target: https://gitlab.com/Lucidiot/pylspci/commits

.. image:: https://img.shields.io/badge/badge%20count-9-brightgreen.svg
   :target: https://gitlab.com/Lucidiot/pylspci

A Python parser for the ``lspci`` command from the pciutils_ package.

.. _pciutils: http://mj.ucw.cz/sw/pciutils/

Basic usage
-----------

To parse ``lspci -nnmm``, use the
:class:`SimpleParser <pylspci.parsers.simple.SimpleParser>`.
To parse ``lspci -nnmmvvvk``, use the
:class:`VerboseParser <pylspci.parsers.verbose.VerboseParser>`.
A :class:`SimpleParser <pylspci.parsers.simple.SimpleParser>` instance is
available directly as ``pylspci.parser``.

.. code:: python

   >>> from pylspci import parser
   >>> parser.run()
   [Device(slot=Slot('0000:00:01.c'), name=NameWithID('Name A [2420]'), ...),
    Device(slot=Slot('0000:00:01.d'), name=NameWithID('Name B [0e54]'), ...)]

Custom arguments
^^^^^^^^^^^^^^^^

.. code:: python

   >>> from pylspci.command import IDResolveOption
   >>> from pylspci import parser
   >>> parser.run(
   ...     hide_single_domain=False,
   ...     id_resolve_option=IDResolveOption.NameOnly,
   ... )
   [Device(slot=Slot('0000:00:01.c'), name=NameWithID('Name A'), ...),
    Device(slot=Slot('0000:00:01.d'), name=NameWithID('Name B'), ...)]

Learn more
----------

.. toctree::
   data
   command
   low
   contributing
