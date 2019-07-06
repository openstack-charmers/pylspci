from enum import Enum
from typing import Optional, Union, List, Mapping, Any
from pathlib import Path
import subprocess

OptionalPath = Optional[Union[str, Path]]


class IDResolveOption(Enum):
    NameOnly = ''
    IDOnly = '-n'
    Both = '-nn'


def lspci(
        pciids: OptionalPath = None,
        pcimap: OptionalPath = None,
        access_method: Optional[str] = None,
        pcilib_params: Mapping[str, Any] = {},
        file: OptionalPath = None,
        verbose: bool = False,
        kernel_drivers: bool = False,
        hide_single_domain: bool = True,
        id_resolve_option: IDResolveOption = IDResolveOption.Both,
        ) -> str:
    args: List[str] = ['lspci', '-mm']
    if verbose:
        args.append('-vvv')
    if kernel_drivers:
        args.append('-k')
    if not hide_single_domain:
        args.append('-D')
    if access_method:
        args.append('-A{}'.format(access_method))
    if id_resolve_option != IDResolveOption.NameOnly:
        args.append(id_resolve_option.value)

    if pciids:
        args.append('-i')
        if not isinstance(pciids, Path):
            pciids = Path(pciids)
        assert pciids.is_file(), 'ID database file not found'
        args.append(str(pciids.absolute()))

    if pcimap:
        args.append('-p')
        if not isinstance(pcimap, Path):
            pcimap = Path(pcimap)
        assert pcimap.is_file(), 'Kernel module mapping file not found'
        args.append(str(pcimap.absolute()))

    if file:
        args.append('-F')
        if not isinstance(file, Path):
            file = Path(file)
        assert file.is_file(), 'Hex dump file not found'
        args.append(str(file.absolute()))

    for key, value in pcilib_params.items():
        args.append('-O{}={}'.format(key, value))

    return subprocess.check_output(
        args,
        universal_newlines=True,
    )
