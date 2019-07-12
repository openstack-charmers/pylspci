from unittest import TestCase
from unittest.mock import patch, call, MagicMock
from pylspci.fields import PCIAccessParameter
from pylspci.command import \
    lspci, list_access_methods, list_pcilib_params, IDResolveOption


class TestCommand(TestCase):

    @patch('pylspci.command.subprocess.check_output')
    def test_default(self, cmd_mock: MagicMock) -> None:
        cmd_mock.return_value = 'something'
        self.assertEqual(lspci(), 'something')
        self.assertEqual(cmd_mock.call_count, 1)
        self.assertEqual(cmd_mock.call_args, call(
            ['lspci', '-mm', '-nn'], universal_newlines=True,
        ))

    @patch('pylspci.command.Path.is_file')
    @patch('pylspci.command.subprocess.check_output')
    def test_pciids(self, cmd_mock: MagicMock, is_file_mock: MagicMock):
        cmd_mock.return_value = 'something'
        is_file_mock.return_value = True
        self.assertEqual(lspci(pciids='/somewhere'), 'something')
        self.assertEqual(cmd_mock.call_count, 1)
        self.assertEqual(cmd_mock.call_args, call(
            ['lspci', '-mm', '-nn', '-i', '/somewhere'],
            universal_newlines=True,
        ))
        self.assertEqual(is_file_mock.call_count, 1)

    @patch('pylspci.command.Path.is_file')
    def test_pciids_missing(self, is_file_mock: MagicMock):
        is_file_mock.return_value = False
        with self.assertRaises(AssertionError):
            lspci(pciids='/nowhere')
        self.assertEqual(is_file_mock.call_count, 1)

    @patch('pylspci.command.Path.is_file')
    @patch('pylspci.command.subprocess.check_output')
    def test_pcimap(self, cmd_mock: MagicMock, is_file_mock: MagicMock):
        cmd_mock.return_value = 'something'
        is_file_mock.return_value = True
        self.assertEqual(lspci(pcimap='/somewhere'), 'something')
        self.assertEqual(cmd_mock.call_count, 1)
        self.assertEqual(cmd_mock.call_args, call(
            ['lspci', '-mm', '-nn', '-p', '/somewhere'],
            universal_newlines=True,
        ))
        self.assertEqual(is_file_mock.call_count, 1)

    @patch('pylspci.command.Path.is_file')
    def test_pcimap_missing(self, is_file_mock: MagicMock):
        is_file_mock.return_value = False
        with self.assertRaises(AssertionError):
            lspci(pcimap='/nowhere')
        self.assertEqual(is_file_mock.call_count, 1)

    @patch('pylspci.command.subprocess.check_output')
    def test_access_method(self, cmd_mock: MagicMock) -> None:
        cmd_mock.return_value = 'something'
        self.assertEqual(lspci(access_method='somemethod'), 'something')
        self.assertEqual(cmd_mock.call_count, 1)
        self.assertEqual(cmd_mock.call_args, call(
            ['lspci', '-mm', '-Asomemethod', '-nn'], universal_newlines=True,
        ))

    @patch('pylspci.command.subprocess.check_output')
    def test_pcilib_params(self, cmd_mock: MagicMock) -> None:
        cmd_mock.return_value = 'something'
        self.assertEqual(lspci(pcilib_params={'a': 'b', 'c': 2}), 'something')
        self.assertEqual(cmd_mock.call_count, 1)
        self.assertEqual(cmd_mock.call_args, call(
            ['lspci', '-mm', '-nn', '-Oa=b', '-Oc=2'],
            universal_newlines=True,
        ))

    @patch('pylspci.command.Path.is_file')
    @patch('pylspci.command.subprocess.check_output')
    def test_file(self, cmd_mock: MagicMock, is_file_mock: MagicMock):
        cmd_mock.return_value = 'something'
        is_file_mock.return_value = True
        self.assertEqual(lspci(file='/somewhere'), 'something')
        self.assertEqual(cmd_mock.call_count, 1)
        self.assertEqual(cmd_mock.call_args, call(
            ['lspci', '-mm', '-nn', '-F', '/somewhere'],
            universal_newlines=True,
        ))
        self.assertEqual(is_file_mock.call_count, 1)

    @patch('pylspci.command.Path.is_file')
    def test_file_missing(self, is_file_mock: MagicMock):
        is_file_mock.return_value = False
        with self.assertRaises(AssertionError):
            lspci(file='/nowhere')
        self.assertEqual(is_file_mock.call_count, 1)

    @patch('pylspci.command.subprocess.check_output')
    def test_verbose(self, cmd_mock: MagicMock) -> None:
        cmd_mock.return_value = 'something'
        self.assertEqual(lspci(verbose=True), 'something')
        self.assertEqual(cmd_mock.call_count, 1)
        self.assertEqual(cmd_mock.call_args, call(
            ['lspci', '-mm', '-vvv', '-nn'],
            universal_newlines=True,
        ))

    @patch('pylspci.command.subprocess.check_output')
    def test_kernel_drivers(self, cmd_mock: MagicMock) -> None:
        cmd_mock.return_value = 'something'
        self.assertEqual(lspci(kernel_drivers=True), 'something')
        self.assertEqual(cmd_mock.call_count, 1)
        self.assertEqual(cmd_mock.call_args, call(
            ['lspci', '-mm', '-k', '-nn'],
            universal_newlines=True,
        ))

    @patch('pylspci.command.subprocess.check_output')
    def test_hide_single_domain(self, cmd_mock: MagicMock) -> None:
        cmd_mock.return_value = 'something'
        self.assertEqual(lspci(hide_single_domain=False), 'something')
        self.assertEqual(cmd_mock.call_count, 1)
        self.assertEqual(cmd_mock.call_args, call(
            ['lspci', '-mm', '-D', '-nn'],
            universal_newlines=True,
        ))

    @patch('pylspci.command.subprocess.check_output')
    def test_id_resolve_option_id_only(self, cmd_mock: MagicMock) -> None:
        cmd_mock.return_value = 'something'
        self.assertEqual(
            lspci(id_resolve_option=IDResolveOption.IDOnly),
            'something',
        )
        self.assertEqual(cmd_mock.call_count, 1)
        self.assertEqual(cmd_mock.call_args, call(
            ['lspci', '-mm', '-n'],
            universal_newlines=True,
        ))

    @patch('pylspci.command.subprocess.check_output')
    def test_id_resolve_option_name_only(self, cmd_mock: MagicMock) -> None:
        cmd_mock.return_value = 'something'
        self.assertEqual(
            lspci(id_resolve_option=IDResolveOption.NameOnly),
            'something',
        )
        self.assertEqual(cmd_mock.call_count, 1)
        self.assertEqual(cmd_mock.call_args, call(
            ['lspci', '-mm'],
            universal_newlines=True,
        ))

    @patch('pylspci.command.Path.is_file')
    @patch('pylspci.command.subprocess.check_output')
    def test_everything(self, cmd_mock: MagicMock, is_file_mock: MagicMock):
        cmd_mock.return_value = 'something'
        is_file_mock.return_value = True

        self.assertEqual(lspci(
            pciids='/pciids',
            pcimap='/pcimap',
            access_method='somemethod',
            pcilib_params={'a': 'b', 'c': 42},
            file='/file',
            verbose=True,
            kernel_drivers=True,
            hide_single_domain=False,
            id_resolve_option=IDResolveOption.IDOnly,
        ), 'something')

        self.assertEqual(cmd_mock.call_count, 1)
        self.assertEqual(cmd_mock.call_args, call(
            ['lspci',
             '-mm',
             '-vvv',
             '-k',
             '-D',
             '-Asomemethod',
             '-n',
             '-i', '/pciids',
             '-p', '/pcimap',
             '-F', '/file',
             '-Oa=b',
             '-Oc=42'],
            universal_newlines=True,
        ))
        self.assertEqual(is_file_mock.call_count, 3)

    @patch('pylspci.command.subprocess.check_output')
    def test_list_access_methods(self, cmd_mock: MagicMock) -> None:
        cmd_mock.return_value = """
        Known PCI access methods:

        linux-sysfs
        linux-proc
        intel-conf1
        intel-conf2
        dump
        """
        self.assertListEqual(
            list_access_methods(),
            ['linux-sysfs', 'linux-proc', 'intel-conf1', 'intel-conf2', 'dump']
        )
        self.assertEqual(cmd_mock.call_count, 1)
        self.assertEqual(cmd_mock.call_args, call(
            ['lspci', '-mm', '-Ahelp', '-nn'],
            universal_newlines=True,
        ))

    @patch('pylspci.command.subprocess.check_output')
    def test_list_pcilib_params(self, cmd_mock: MagicMock) -> None:
        cmd_mock.return_value = """
        Known PCI access parameters:

        dump.name        Name of the bus dump file to read from ()
        proc.path        Path to the procfs bus tree (/proc/bus/pci)
        sysfs.path       Path to the sysfs device tree (/sys/bus/pci)
        hwdb.disable     Do not look up names in UDEV's HWDB if non-zero (0)
        net.cache_name   Name of the ID cache file (~/.pciids-cache)
        net.domain       DNS domain used for resolving of ID's (pci.id.ucw.cz)
        """
        self.assertListEqual(
            list_pcilib_params(),
            list(map(PCIAccessParameter, [
                "dump.name   Name of the bus dump file to read from ()",
                "proc.path   Path to the procfs bus tree (/proc/bus/pci)",
                "sysfs.path   Path to the sysfs device tree (/sys/bus/pci)",
                "hwdb.disable   Do not look up names "
                "in UDEV's HWDB if non-zero (0)",
                "net.cache_name   Name of the ID cache file (~/.pciids-cache)",
                "net.domain    DNS domain used for "
                "resolving of ID's (pci.id.ucw.cz)",
            ]))
        )
        self.assertEqual(cmd_mock.call_count, 1)
        self.assertEqual(cmd_mock.call_args, call(
            ['lspci', '-Ohelp'],
            universal_newlines=True,
        ))
