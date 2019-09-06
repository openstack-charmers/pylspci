from unittest import TestCase
from unittest.mock import patch, call, MagicMock
from typing import List
from pylspci.device import Device
from pylspci.parsers import SimpleParser


class TestSimpleParser(TestCase):

    parser: SimpleParser

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.parser = SimpleParser()

    def _check_device(self, dev: Device) -> None:
        self.assertIsInstance(dev, Device)
        self.assertEqual(dev.slot.domain, 0x0000)
        self.assertEqual(dev.slot.bus, 0x00)
        self.assertEqual(dev.slot.device, 0x1c)
        self.assertEqual(dev.slot.function, 0x3)
        self.assertEqual(dev.cls.id, 0x0604)
        self.assertEqual(dev.cls.name, 'PCI bridge')
        self.assertEqual(dev.vendor.id, 0x8086)
        self.assertEqual(dev.vendor.name, 'Intel Corporation')
        self.assertEqual(dev.device.id, 0x244e)
        self.assertEqual(dev.device.name, '82801 PCI Bridge')
        assert dev.subsystem_vendor is not None
        self.assertEqual(dev.subsystem_vendor.id, 0x8086)
        self.assertEqual(dev.subsystem_vendor.name, 'Intel Corporation')
        assert dev.subsystem_device is not None
        self.assertEqual(dev.subsystem_device.id, 0x244e)
        self.assertEqual(dev.subsystem_device.name, '82801 PCI Bridge')
        self.assertEqual(dev.revision, 0xd5)
        self.assertEqual(dev.progif, 0x01)

    def test_parse_str(self) -> None:
        dev_list: List[Device] = self.parser.parse(
            '00:1c.3 "PCI bridge [0604]" "Intel Corporation [8086]" '
            '"82801 PCI Bridge [244e]" -rd5 -p01 "Intel Corporation [8086]" '
            '"82801 PCI Bridge [244e]"'
        )
        self.assertEqual(len(dev_list), 1)
        self._check_device(dev_list[0])

    def test_parse_list(self) -> None:
        dev_list: List[Device] = self.parser.parse([
            [
                '00:1c.3',
                'PCI bridge [0604]',
                'Intel Corporation [8086]',
                '82801 PCI Bridge [244e]',
                '-rd5',
                '-p01',
                'Intel Corporation [8086]',
                '82801 PCI Bridge [244e]',
            ]
        ])
        self.assertEqual(len(dev_list), 1)
        self._check_device(dev_list[0])

    def test_parse_nothing(self) -> None:
        dev_list: List[Device] = self.parser.parse('00:00.0 "" "" "" "" ""')
        self.assertEqual(len(dev_list), 1)
        dev: Device = dev_list[0]
        self.assertIsInstance(dev, Device)
        self.assertEqual(dev.slot.domain, 0x0000)
        self.assertEqual(dev.slot.bus, 0x00)
        self.assertEqual(dev.slot.device, 0x00)
        self.assertEqual(dev.slot.function, 0x0)
        self.assertIsNone(dev.cls.id)
        self.assertEqual(dev.cls.name, '')
        self.assertIsNone(dev.vendor.id)
        self.assertEqual(dev.vendor.name, '')
        self.assertIsNone(dev.device.id)
        self.assertEqual(dev.device.name, '')
        assert dev.subsystem_vendor is not None
        self.assertIsNone(dev.subsystem_vendor.id)
        self.assertEqual(dev.subsystem_vendor.name, '')
        assert dev.subsystem_device is not None
        self.assertIsNone(dev.subsystem_device.id)
        self.assertEqual(dev.subsystem_device.name, '')
        self.assertIsNone(dev.revision)
        self.assertIsNone(dev.progif)

    @patch('pylspci.command.lspci')
    def test_command(self, cmd_mock: MagicMock) -> None:
        cmd_mock.return_value = \
            '00:1c.3 "PCI bridge [0604]" "Intel Corporation [8086]" ' \
            '"82801 PCI Bridge [244e]" -rd5 -p01 "Intel Corporation [8086]" ' \
            '"82801 PCI Bridge [244e]"\n' * 2

        devices: List[Device] = self.parser.run()
        self.assertEqual(len(devices), 2)
        self._check_device(devices[0])
        self._check_device(devices[1])

        self.assertEqual(cmd_mock.call_count, 1)
        self.assertEqual(cmd_mock.call_args, call())
