from unittest import TestCase
from unittest.mock import patch, call, MagicMock
from pathlib import Path
from pylspci.command import CommandBuilder, IDResolveOption
from pylspci.parsers import SimpleParser, VerboseParser


class TestCommandBuilder(TestCase):

    @patch('pylspci.command.lspci')
    def test_default(self, lspci_mock):
        lspci_mock.return_value = ['a', 'b']
        self.assertListEqual(list(CommandBuilder()), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call())

    @patch('pylspci.command.Path.is_file')
    @patch('pylspci.command.lspci')
    def test_use_pciids(self, lspci_mock, isfile_mock):
        lspci_mock.return_value = ['a', 'b']
        isfile_mock.return_value = True
        builder = CommandBuilder().use_pciids('somefile')
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(pciids=Path('somefile')))
        self.assertEqual(isfile_mock.call_count, 1)

    @patch('pylspci.command.Path.is_file')
    @patch('pylspci.command.lspci')
    def test_use_pciids_check(self, lspci_mock, isfile_mock):
        lspci_mock.return_value = ['a', 'b']
        isfile_mock.return_value = False
        with self.assertRaisesRegex(AssertionError, 'not found'):
            CommandBuilder().use_pciids('somefile')
        self.assertEqual(isfile_mock.call_count, 1)

    @patch('pylspci.command.Path.is_file')
    @patch('pylspci.command.lspci')
    def test_use_pciids_no_check(self, lspci_mock, isfile_mock):
        lspci_mock.return_value = ['a', 'b']
        isfile_mock.return_value = False
        builder = CommandBuilder().use_pciids('somefile', check=False)
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(pciids=Path('somefile')))
        self.assertFalse(isfile_mock.called)

    @patch('pylspci.command.Path.is_file')
    @patch('pylspci.command.lspci')
    def test_use_pcimap(self, lspci_mock, isfile_mock):
        lspci_mock.return_value = ['a', 'b']
        isfile_mock.return_value = True
        builder = CommandBuilder().use_pcimap('somefile')
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(pcimap=Path('somefile')))
        self.assertEqual(isfile_mock.call_count, 1)

    @patch('pylspci.command.Path.is_file')
    @patch('pylspci.command.lspci')
    def test_use_pcimap_check(self, lspci_mock, isfile_mock):
        lspci_mock.return_value = ['a', 'b']
        isfile_mock.return_value = False
        with self.assertRaisesRegex(AssertionError, 'not found'):
            CommandBuilder().use_pcimap('somefile')
        self.assertEqual(isfile_mock.call_count, 1)

    @patch('pylspci.command.Path.is_file')
    @patch('pylspci.command.lspci')
    def test_use_pcimap_no_check(self, lspci_mock, isfile_mock):
        lspci_mock.return_value = ['a', 'b']
        isfile_mock.return_value = False
        builder = CommandBuilder().use_pcimap('somefile', check=False)
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(pcimap=Path('somefile')))
        self.assertFalse(isfile_mock.called)

    @patch('pylspci.command.lspci')
    def test_use_access_method(self, lspci_mock):
        lspci_mock.return_value = ['a', 'b']
        builder = CommandBuilder() \
            .use_access_method('one') \
            .use_access_method('two')
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(access_method='two'))

    @patch('pylspci.command.list_access_methods')
    def test_list_access_methods(self, list_mock):
        list_mock.return_value = ['a', 'b']
        builder = CommandBuilder().list_pcilib_params().list_access_methods()
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(list_mock.call_count, 1)
        self.assertEqual(list_mock.call_args, call())

    @patch('pylspci.command.list_pcilib_params')
    def test_list_pcilib_params(self, list_mock):
        list_mock.return_value = ['a', 'b']
        builder = CommandBuilder().list_access_methods().list_pcilib_params()
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(list_mock.call_count, 1)
        self.assertEqual(list_mock.call_args, call())

    @patch('pylspci.command.list_pcilib_params_raw')
    def test_list_pcilib_params_raw(self, list_mock):
        list_mock.return_value = ['a', 'b']
        builder = CommandBuilder() \
            .list_access_methods() \
            .list_pcilib_params(raw=True)
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(list_mock.call_count, 1)
        self.assertEqual(list_mock.call_args, call())

    @patch('pylspci.command.lspci')
    def test_with_pcilib_params_dict(self, lspci_mock):
        with self.assertRaisesRegex(AssertionError, 'dict or keyword'):
            CommandBuilder().with_pcilib_params({'a': 'b'}, c='d')
        with self.assertRaisesRegex(AssertionError, 'Only one positional'):
            CommandBuilder().with_pcilib_params({'a': 'b'}, {'c': 'd'})

        lspci_mock.return_value = ['a', 'b']
        builder = CommandBuilder().with_pcilib_params({'a': 'b'})
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(pcilib_params={'a': 'b'}))

    @patch('pylspci.command.lspci')
    def test_with_pcilib_params_kwargs(self, lspci_mock):
        lspci_mock.return_value = ['a', 'b']
        builder = CommandBuilder() \
            .with_pcilib_params(a='1', b='2') \
            .with_pcilib_params(b='3', c='4')
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(pcilib_params={
            'a': '1', 'b': '3', 'c': '4',
        }))

    @patch('pylspci.command.Path.is_file')
    @patch('pylspci.command.lspci')
    def test_from_file(self, lspci_mock, isfile_mock):
        lspci_mock.return_value = ['a', 'b']
        isfile_mock.return_value = True
        builder = CommandBuilder().from_file('somefile')
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(file=Path('somefile')))
        self.assertEqual(isfile_mock.call_count, 1)

    @patch('pylspci.command.Path.is_file')
    @patch('pylspci.command.lspci')
    def test_from_file_check(self, lspci_mock, isfile_mock):
        lspci_mock.return_value = ['a', 'b']
        isfile_mock.return_value = False
        with self.assertRaisesRegex(AssertionError, 'not found'):
            CommandBuilder().from_file('somefile')
        self.assertEqual(isfile_mock.call_count, 1)

    @patch('pylspci.command.Path.is_file')
    @patch('pylspci.command.lspci')
    def test_from_file_no_check(self, lspci_mock, isfile_mock):
        lspci_mock.return_value = ['a', 'b']
        isfile_mock.return_value = False
        builder = CommandBuilder().from_file('somefile', check=False)
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(file=Path('somefile')))
        self.assertFalse(isfile_mock.called)

    @patch('pylspci.command.lspci')
    def test_verbose(self, lspci_mock):
        lspci_mock.return_value = ['a', 'b']
        builder = CommandBuilder().verbose()
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(verbose=True))

    @patch('pylspci.command.lspci')
    def test_include_kernel_drivers(self, lspci_mock):
        lspci_mock.return_value = ['a', 'b']
        builder = CommandBuilder() \
            .include_kernel_drivers(False) \
            .include_kernel_drivers()
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(
            verbose=True,
            kernel_drivers=True,
        ))

    @patch('pylspci.command.lspci')
    def test_include_bridge_paths(self, lspci_mock):
        lspci_mock.return_value = ['a', 'b']
        builder = CommandBuilder() \
            .include_bridge_paths(False) \
            .include_bridge_paths()
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(
            bridge_paths=True,
        ))

    @patch('pylspci.command.lspci')
    def test_hide_single_domain(self, lspci_mock):
        lspci_mock.return_value = ['a', 'b']
        builder = CommandBuilder().hide_single_domain()
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(hide_single_domain=True))

    @patch('pylspci.command.lspci')
    def test_with_ids(self, lspci_mock):
        lspci_mock.return_value = ['a', 'b']
        builder = CommandBuilder().with_ids(False)
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(
            id_resolve_option=IDResolveOption.NameOnly,
        ))

        lspci_mock.reset_mock()
        builder = builder.with_ids()
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(
            id_resolve_option=IDResolveOption.Both,
        ))

    @patch('pylspci.command.lspci')
    def test_with_names(self, lspci_mock):
        lspci_mock.return_value = ['a', 'b']
        builder = CommandBuilder().with_names(False)
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(
            id_resolve_option=IDResolveOption.IDOnly,
        ))

        lspci_mock.reset_mock()
        builder = builder.with_names()
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(
            id_resolve_option=IDResolveOption.Both,
        ))

    @patch('pylspci.command.SlotFilter')
    @patch('pylspci.command.lspci')
    def test_slot_filter_str(self, lspci_mock, filter_mock):
        with self.assertRaisesRegex(AssertionError, 'Only one positional'):
            CommandBuilder().slot_filter('something', 'something else')
        with self.assertRaisesRegex(AssertionError, 'Use either'):
            CommandBuilder().slot_filter('something', domain='a')

        filter_mock.parse.return_value = 'lefilter'
        lspci_mock.return_value = ['a', 'b']
        builder = CommandBuilder().slot_filter('something')
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(slot_filter='lefilter'))
        self.assertEqual(filter_mock.parse.call_count, 1)
        self.assertEqual(filter_mock.parse.call_args, call('something'))

    @patch('pylspci.command.SlotFilter')
    @patch('pylspci.command.lspci')
    def test_slot_filter_kwargs(self, lspci_mock, filter_mock):
        filter_mock.return_value = 'lefilter'
        lspci_mock.return_value = ['a', 'b']
        builder = CommandBuilder().slot_filter(
            domain='a',
            bus='b',
            device='c',
            function='d',
        )
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(slot_filter='lefilter'))
        self.assertEqual(filter_mock.call_count, 1)
        self.assertEqual(filter_mock.call_args, call(
            domain='a',
            bus='b',
            device='c',
            function='d',
        ))

    @patch('pylspci.command.DeviceFilter')
    @patch('pylspci.command.lspci')
    def test_device_filter_str(self, lspci_mock, filter_mock):
        with self.assertRaisesRegex(AssertionError, 'Only one positional'):
            CommandBuilder().device_filter('something', 'something else')
        with self.assertRaisesRegex(AssertionError, 'Use either'):
            CommandBuilder().device_filter('something', vendor='b')

        filter_mock.parse.return_value = 'lefilter'
        lspci_mock.return_value = ['a', 'b']
        builder = CommandBuilder().device_filter('something')
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(device_filter='lefilter'))
        self.assertEqual(filter_mock.parse.call_count, 1)
        self.assertEqual(filter_mock.parse.call_args, call('something'))

    @patch('pylspci.command.DeviceFilter')
    @patch('pylspci.command.lspci')
    def test_device_filter_kwargs(self, lspci_mock, filter_mock):
        filter_mock.return_value = 'lefilter'
        lspci_mock.return_value = ['a', 'b']
        builder = CommandBuilder().device_filter(
            cls='a',
            vendor='b',
            device='c',
        )
        self.assertListEqual(list(builder), ['a', 'b'])
        self.assertEqual(lspci_mock.call_count, 1)
        self.assertEqual(lspci_mock.call_args, call(device_filter='lefilter'))
        self.assertEqual(filter_mock.call_count, 1)
        self.assertEqual(filter_mock.call_args, call(
            cls='a',
            vendor='b',
            device='c',
        ))

    def test_with_default_parser(self):
        builder = CommandBuilder()
        self.assertIsNone(builder._parser)

        builder = CommandBuilder().with_default_parser()
        self.assertIsInstance(builder._parser, SimpleParser)

        builder = CommandBuilder().verbose().with_default_parser()
        self.assertIsInstance(builder._parser, VerboseParser)

    @patch('pylspci.command.lspci')
    def test_with_parser(self, lspci_mock):
        lspci_mock.return_value = ['a', 'b']
        parser_mock = MagicMock(spec=SimpleParser)
        parser_mock.parse.return_value = ('parsed_a', 'parsed_b')
        builder = CommandBuilder().with_parser(parser_mock)
        self.assertListEqual(list(builder), ['parsed_a', 'parsed_b'])
        self.assertEqual(parser_mock.parse.call_count, 1)
        self.assertEqual(parser_mock.parse.call_args, call(['a', 'b']))
