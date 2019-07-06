from functools import partial
import re


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
            return '{} [{:x}]'.format(self.name, self.id)
        elif self.name:
            return self.name
        elif self.id:
            return '{:x}'.format(self.id)
        else:
            return ''

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, str(self))
