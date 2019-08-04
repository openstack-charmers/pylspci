Command-line interface
======================

Once the package is installed, an executable called ``pylspci`` should be
created by setuptools. You may also use ``python3 -m pylspci`` to call the same
script. The CLI mimicks some of lspci's arguments, but due to pylspci's own
behavior and due to some features being not implemented, some arguments have
been omitted or modified.

.. code::

   pylspci [-h] [-i PCIIDS] [-p PCIMAP]
           [-s [[domain:]bus:][device][.function]]
           [-d [vendor]:[device][:class]]
           [-v] [-k] [-P] [--name-only | -n | -nn]
           [-A METHOD | -F FILE | -H1 | -H2] [-O KEY=VALUE]
           [--json | --raw]

Options
-------

``-h, --help``
  Show a help message and exit.
``-i, --pci-ids <path>``
  Path to an alternate file to use as the PCI ID list.

  Maps to ``pciids`` in :func:`lspci() <pylspci.command.lspci>`.
``-p, --pci-map <path>``
  Path to an alternate file to use as the kernel module mapping file.

  Maps to ``pcimap`` in :func:`lspci() <pylspci.command.lspci>`.

Filters
^^^^^^^

``-s [[domain:]bus:][device][.function]``
  Filter devices by their slots.
  Any value can be omitted or set to ``*`` to disable filtering.

  Maps to ``slot_filter`` in :func:`lspci() <pylspci.command.lspci>`.
  See :class:`SlotFilter <pylspci.filters.SlotFilter>` for more details.
``-d [vendor]:[device][:class]``
  Filter devices by their type.
  Any value can be omitted or set to ``*`` to disable filtering.

  Maps to ``device_filter`` in :func:`lspci() <pylspci.command.lspci>`.
  See :class:`DeviceFilter <pylspci.filters.DeviceFilter>` for more details.

Device data
^^^^^^^^^^^

``-v, --verbose``
  Display more details about devices.

  Maps to ``verbose`` in :func:`lspci() <pylspci.command.lspci>`.
``-k, --kernel-modules``
  On Linux kernels above 2.6, include kernel drivers handling each device and
  kernel modules able to handle them. Implies ``-v``.

  Maps to ``include_kernel_drivers``
  in :func:`lspci() <pylspci.command.lspci>`.
``-P, -PP, --bridge-paths``
  Include PCI bridge paths along with device IDs.

  Maps to ``include_bridge_paths`` in :func:`lspci() <pylspci.command.lspci>`.
``--name-only``
  Only include device names. This is the default.

  Maps to :attr:`NameOnly <pylspci.command.IDResolveOption.NameOnly>` as
  the ``id_resolve_option`` in :func:`lspci() <pylspci.command.lspci>`.
``-n, --id-only``
  Only include device IDs, without looking for names in the PCI ID file.

  Maps to :attr:`IDOnly <pylspci.command.IDResolveOption.IDOnly>` as
  the ``id_resolve_option`` in :func:`lspci() <pylspci.command.lspci>`.
``-nn, --name-with-id``
  Include both device IDs and names.

  Maps to :attr:`Both <pylspci.command.IDResolveOption.Both>` as
  the ``id_resolve_option`` in :func:`lspci() <pylspci.command.lspci>`.

Output modes
^^^^^^^^^^^^

``--json``
  Parse the lspci output and return a JSON list. This is the default.

  Will automatically select the best parser depending on the chosen settings:

  * In verbose mode, uses an instance of
    :class:`VerboseParser <pylspci.parsers.VerboseParser>` and returns a list
    of objects corresponding to :class:`Device <pylspci.device.Device>`
    instances.
  * In non-verbose mode, uses an instance of
    :class:`SimpleParser <pylspci.parsers.SimpleParser>` and returns a list of
    objects corresponding to :class:`Device <pylspci.device.Device>` instances.
  * ``-Ahelp`` will always return a list of strings.
  * ``-Ohelp`` returns a list of objects for each parameter,
    with its name, description and default values.
    See :class:`PCIAccessParameter <pylspci.fields.PCIAccessParameter>`.
``--raw``
  Return lspci's output directly, without parsing; the CLI then just becomes a
  thin layer of argument parsing before lspci.

PCI access
^^^^^^^^^^

``-O, --option <key>=<value>``
  Set PCI library access parameters.

  Maps to ``pcilib_params`` in :func:`lspci() <pylspci.command.lspci>`.

  Use ``-O help`` to get a list of available parameters, via
  :func:`list_pcilib_params() <pylspci.command.list_pcilib_params>`.
``-A, --access-method <method>``
  PCI library access method to use.

  Maps to ``access_method`` in :func:`lspci() <pylspci.command.lspci>`.

  Use ``-A help`` to list available access methods, via
  :func:`list_access_methods() <pylspci.command.list_access_methods>`.
``-F, --file <path>``
  Use a hex dump file from a previous run of lspci instead of accessing
  real hardware. Implies ``-Adump``.

  Maps to ``file`` in :func:`lspci() <pylspci.command.lspci>`.
``-H1``
  Access hardware using Intel configuration mechanism 1.
  Alias to ``-A intel-conf1``.
``-H2``
  Access hardware using Intel configuration mechanism 2.
  Alias to ``-A intel-conf2``.

