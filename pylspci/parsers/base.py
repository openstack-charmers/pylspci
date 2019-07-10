from abc import ABC, abstractmethod
from typing import Union, List, Mapping, Any
from pylspci.device import Device
from pylspci.command import lspci


class Parser(ABC):

    default_lspci_args: Mapping[str, Any] = {}

    @abstractmethod
    def parse(self, data: Union[str, List[str]]) -> List[Device]:
        """
        Parse a string or list of strings as a list of devices.
        """

    def run(self, **kwargs: Mapping[str, Any]) -> List[Device]:
        lspci_kwargs = self.default_lspci_args.copy()
        lspci_kwargs.update(kwargs)
        return self.parse(lspci(**lspci_kwargs))
