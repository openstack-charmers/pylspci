from typing import NamedTuple
from pylspci.fields import Slot, NameWithID


class Device(NamedTuple):
    slot: Slot
    cls: NameWithID
    vendor: NameWithID
    device: NameWithID
    subsystem_vendor: NameWithID
    subsystem_device: NameWithID
    revision: int
    progif: int
