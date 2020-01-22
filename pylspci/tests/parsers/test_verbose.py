from unittest import TestCase
from unittest.mock import patch, call, MagicMock
from typing import List
from pylspci.device import Device
from pylspci.parsers import VerboseParser

SAMPLE_DEVICE: str = """
Slot:	00:1c.3
Class:	PCI bridge [0604]
Vendor:	Intel Corporation [8086]
Device:	82801 PCI Bridge [244e]
SVendor:	Intel Corporation [8086]
SDevice:	82801 PCI Bridge [244e]
Rev:	d5
ProgIf:	01
Driver:	pcieport
Module:	nouveau
Module:	nvidia
NUMANode:	0
"""


class TestVerboseParser(TestCase):

    parser: VerboseParser

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.parser = VerboseParser()

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
        self.assertEqual(dev.driver, 'pcieport')
        self.assertListEqual(dev.kernel_modules, ['nouveau', 'nvidia'])
        self.assertEqual(dev.numa_node, 0)

    def test_parse_str(self) -> None:
        devices: List[Device] = self.parser.parse(SAMPLE_DEVICE)
        self.assertEqual(len(devices), 1)
        self._check_device(devices[0])

    def test_parse_list(self) -> None:
        devices: List[Device] = self.parser.parse([SAMPLE_DEVICE, ])
        self.assertEqual(len(devices), 1)
        self._check_device(devices[0])

    @patch('pylspci.command.lspci')
    def test_command(self, cmd_mock: MagicMock) -> None:
        cmd_mock.return_value = '{0}\n\n{0}'.format(SAMPLE_DEVICE)

        devices: List[Device] = self.parser.run()
        self.assertEqual(len(devices), 2)
        self._check_device(devices[0])
        self._check_device(devices[1])

        self.assertEqual(cmd_mock.call_count, 1)
        self.assertEqual(cmd_mock.call_args,
                         call(verbose=True, kernel_drivers=True))

    def test_unknown_field(self) -> None:
        with self.assertWarns(
            UserWarning,
            msg="Unsupported device field 'NewField' with value 'Value'\n"
                "Please report this, along with the output of"
                "`lspci -mmnnvvvk`, at "
                "https://gitlab.com/Lucidiot/pylspci/issues"):
            devices: List[Device] = \
                self.parser.parse(SAMPLE_DEVICE + 'NewField\tValue')

        self.assertEqual(len(devices), 1)
        self._check_device(devices[0])
