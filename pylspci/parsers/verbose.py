from typing import Union, List, NamedTuple, Callable, Any
from pylspci.parsers.base import Parser
from pylspci.device import Device
from pylspci.fields import hexstring, Slot, NameWithID


class FieldMapping(NamedTuple):
    field_name: str
    field_type: Callable[[str], Any]
    many: bool = False


class VerboseParser(Parser):
    """
    A parser for lspci -vvvmm
    """

    default_lspci_args = {
        'verbose': True,
        'kernel_drivers': True,
    }

    # Maps lspci output fields to Device fields with a type
    _field_mapping = {
        'Slot': FieldMapping(field_name='slot', field_type=Slot),
        'Class': FieldMapping(field_name='cls', field_type=NameWithID),
        'Vendor': FieldMapping(field_name='vendor', field_type=NameWithID),
        'Device': FieldMapping(field_name='device', field_type=NameWithID),
        'SVendor': FieldMapping(
            field_name='subsystem_vendor',
            field_type=NameWithID,
        ),
        'SDevice': FieldMapping(
            field_name='subsystem_device',
            field_type=NameWithID,
        ),
        'Rev': FieldMapping(field_name='revision', field_type=hexstring),
        'ProgIf': FieldMapping(field_name='progif', field_type=hexstring),
        'Driver': FieldMapping(field_name='driver', field_type=str),
        'Module': FieldMapping(
            field_name='kernel_modules',
            field_type=str,
            many=True,
        ),
    }

    def _parse_device(self, device_data: Union[str, List[str]]) -> Device:
        devdict = {}
        if isinstance(device_data, str):
            device_data = device_data.splitlines()

        for line in device_data:
            key, _, value = map(str.strip, line.partition(':'))
            assert key in self._field_mapping, \
                'Unsupported key {!r}'.format(key)
            field = self._field_mapping[key]
            if field.many:
                devdict.setdefault(field.field_name, []) \
                       .append(field.field_type(value))
            else:
                devdict[field.field_name] = field.field_type(value)

        return Device(**devdict)

    def parse(self, data: Union[str, List[str]]) -> List[Device]:
        if isinstance(data, str):
            data = data.split('\n\n')
        return list(map(
            self._parse_device,
            filter(bool, map(str.strip, data)),  # Ignore empty strings
        ))
