from pylspci.fields import hexstring, Slot, NameWithID
from pylspci.device import Device
import argparse
import shlex
import subprocess


class SimpleFormatParser(object):

    _parser = None

    @property
    def parser(self):
        if self._parser is not None:
            return self._parser

        self._parser = argparse.ArgumentParser()
        self._parser.add_argument(
            'slot',
            type=Slot,
        )
        self._parser.add_argument(
            'cls',
            type=NameWithID,
        )
        self._parser.add_argument(
            'vendor',
            type=NameWithID,
        )
        self._parser.add_argument(
            'device',
            type=NameWithID,
        )
        self._parser.add_argument(
            'subsystem_vendor',
            type=NameWithID,
        )
        self._parser.add_argument(
            'subsystem_device',
            type=NameWithID,
        )
        self._parser.add_argument(
            '-r',
            type=hexstring,
            nargs='?',
            dest='revision',
        )
        self._parser.add_argument(
            '-p',
            type=hexstring,
            nargs='?',
            dest='progif',
        )
        return self._parser

    def parse(self, args):
        if isinstance(args, str):
            args = shlex.split(args)
        return Device(**vars(self.parser.parse_args(args)))

    def from_lspci(self):
        return list(map(
            self.parse,
            subprocess.check_output(
                ['lspci', '-nnmm'],
                universal_newlines=True,
            ).splitlines(),
        ))
