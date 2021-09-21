from unittest import TestCase

from pylspci.device import Device
from pylspci.fields import NameWithID, Slot


class TestDevice(TestCase):

    def test_as_dict(self) -> None:
        d = Device(
            slot=Slot('cafe:13:07.2'),
            cls=NameWithID('Something [caf3]'),
            vendor=NameWithID('Something [caf3]'),
            device=NameWithID('Something [caf3]'),
            subsystem_vendor=NameWithID('Something [caf3]'),
            subsystem_device=NameWithID('Something [caf3]'),
            revision=20,
            progif=1,
            driver='self_driving',
            kernel_modules=['snd-pcsp'],
            numa_node=0,
            iommu_group=1,
            physical_slot='4-2',
        )
        self.assertDictEqual(d.as_dict(), {
            'slot': {
                'bus': 0x13,
                'device': 0x07,
                'domain': 0xcafe,
                'function': 0x2,
                'parent': None
            },
            'cls': {
                'id': 0xcaf3,
                'name': 'Something'
            },
            'vendor': {
                'id': 0xcaf3,
                'name': 'Something'
            },
            'device': {
                'id': 0xcaf3,
                'name': 'Something'
            },
            'subsystem_vendor': {
                'id': 0xcaf3,
                'name': 'Something'
            },
            'subsystem_device': {
                'id': 0xcaf3,
                'name': 'Something'
            },
            'revision': 20,
            'progif': 1,
            'driver': 'self_driving',
            'kernel_modules': ['snd-pcsp'],
            'numa_node': 0,
            'iommu_group': 1,
            'physical_slot': '4-2',
        })
