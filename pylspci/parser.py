from functools import partial
import argparse
import re
import shlex
import subprocess

hexstring = partial(int, base=16)


class Slot(object):
    """
    Describes a PCI slot identifier.
    """

    def __init__(self, value):
        data = list(map(hexstring, re.split(r'[:\.]', value)))
        if len(data) == 3:
            data.insert(0, 0)
        self.domain, self.bus, self.device, self.function = data

    def __str__(self):
        return '{:04x}:{:02x}:{:02x}.{:01x}'.format(
            self.domain, self.bus, self.device, self.function,
        )

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, str(self))


class NameWithID(object):
    """
    Describes a name with an hexadecimal ID.
    """

    _NAME_ID_REGEX = re.compile(r'^(?P<name>.+)\s\[(?P<id>[0-9a-fA-F]+)\]$')

    def __init__(self, value):
        if value.endswith(']'):
            # Holds both an ID and a name
            gd = self._NAME_ID_REGEX.match(value).groupdict()
            self.id = gd['id']
            self.name = gd['name']

        try:
            self.id = int(value, base=16)
            self.name = None
        except ValueError:
            self.id = None
            self.name = value

    def __str__(self):
        if self.id and self.name:
            return '{} [{:x}]'.format(self.id, self.name)
        elif self.name:
            return self.name
        elif self.id:
            return '{:x}'.format(self.id)
        else:
            return ''

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, str(self))


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
            'class',
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
        return vars(self.parser.parse_args(args))

    def from_lspci(self):
        return list(map(
            self.parse,
            subprocess.check_output(
                ['lspci', '-nnmm'],
                universal_newlines=True,
            ).splitlines(),
        ))
