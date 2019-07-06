from unittest import TestCase
from unittest.mock import patch, call, MagicMock
from pylspci.command import lspci, IDResolveOption


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
