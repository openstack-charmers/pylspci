from unittest import TestCase
from pylspci.fields import Slot, NameWithID


class TestSlot(TestCase):

    def test_full_slot(self) -> None:
        s = Slot('cafe:13:37.2')
        self.assertEqual(s.domain, 0xcafe)
        self.assertEqual(s.bus, 0x13)
        self.assertEqual(s.device, 0x37)
        self.assertEqual(s.function, 0x2)

    def test_optional_domain(self) -> None:
        """
        lspci can hide the domain ID when there is only one domain
        on the system, numbered 0. Ensure Slot defaults the domain to 0.
        """
        s = Slot('13:37.2')
        self.assertEqual(s.domain, 0x0)
        self.assertEqual(s.bus, 0x13)
        self.assertEqual(s.device, 0x37)
        self.assertEqual(s.function, 0x2)

    def test_repr(self) -> None:
        self.assertEqual(
            repr(Slot('13:37:42.6')),
            "Slot('0013:37:42.6')",
        )

    def test_str(self) -> None:
        self.assertEqual(
            str(Slot('13:37:42.6')),
            '0013:37:42.6',
        )


class TestNameWithID(TestCase):

    def test_full(self) -> None:
        n = NameWithID('Something [caf3]')
        self.assertEqual(n.id, 0xcaf3)
        self.assertEqual(n.name, 'Something')
        self.assertEqual(str(n), 'Something [caf3]')
        self.assertEqual(repr(n), "NameWithID('Something [caf3]')")

    def test_only_id(self) -> None:
        """
        Depending on the lspci arguments, we might only have an hexadecimal ID
        """
        n = NameWithID('caf3')
        self.assertEqual(n.id, 0xcaf3)
        self.assertIsNone(n.name)
        self.assertEqual(str(n), 'caf3')
        self.assertEqual(repr(n), "NameWithID('caf3')")

    def test_only_name(self) -> None:
        """
        Depending on the lspci arguments, we might only have a name
        """
        n = NameWithID('Something')
        self.assertIsNone(n.id)
        self.assertEqual(n.name, 'Something')
        self.assertEqual(str(n), 'Something')
        self.assertEqual(repr(n), "NameWithID('Something')")

    def test_double_brackets(self) -> None:
        """
        Some device names have extra info in brackets
        """
        n = NameWithID('Something [with brackets] [caf3]')
        self.assertEqual(n.id, 0xcaf3)
        self.assertEqual(n.name, 'Something [with brackets]')
        self.assertEqual(str(n), 'Something [with brackets] [caf3]')
        self.assertEqual(
            repr(n),
            "NameWithID('Something [with brackets] [caf3]')",
        )

    def test_none(self) -> None:
        n = NameWithID(None)
        self.assertIsNone(n.id)
        self.assertIsNone(n.name)
        self.assertEqual(str(n), '')
        self.assertEqual(repr(n), "NameWithID('')")
