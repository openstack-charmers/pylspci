from typing import NamedTuple, Optional, List
from pylspci.fields import Slot, NameWithID


class Device(NamedTuple):
    slot: Slot
    cls: NameWithID
    vendor: NameWithID
    device: NameWithID
    subsystem_vendor: Optional[NameWithID] = None
    subsystem_device: Optional[NameWithID] = None
    revision: Optional[int] = None
    progif: Optional[int] = None
    driver: Optional[str] = None
    kernel_modules: List[str] = []
