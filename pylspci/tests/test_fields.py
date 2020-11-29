from unittest import TestCase

from pylspci.fields import NameWithID, PCIAccessParameter, Slot


class TestSlot(TestCase):

    def test_full_slot(self) -> None:
        s = Slot('cafe:13:07.2')
        self.assertEqual(s.domain, 0xcafe)
        self.assertEqual(s.bus, 0x13)
        self.assertEqual(s.device, 0x07)
        self.assertEqual(s.function, 0x2)

    def test_optional_domain(self) -> None:
        """
        lspci can hide the domain ID when there is only one domain
        on the system, numbered 0. Ensure Slot defaults the domain to 0.
        """
        s = Slot('13:07.2')
        self.assertEqual(s.domain, 0x0)
        self.assertEqual(s.bus, 0x13)
        self.assertEqual(s.device, 0x07)
        self.assertEqual(s.function, 0x2)

    def test_device_limit_32(self) -> None:
        """
        There cannot be more than 32 devices on each bus
        """
        with self.assertRaises(ValueError):
            Slot('0000:00:20.0')

    def test_function_limit_8(self) -> None:
        """
        Function numbers are from 0 to 7
        """
        with self.assertRaises(ValueError):
            Slot('0000:00:01.f')

    def test_repr(self) -> None:
        self.assertEqual(
            repr(Slot('13:37:04.2')),
            "Slot('0013:37:04.2')",
        )

    def test_str(self) -> None:
        self.assertEqual(
            str(Slot('13:37:04.2')),
            '0013:37:04.2',
        )

    def test_parent(self) -> None:
        s = Slot('abcd:13:07.2/cafe:c0:0f.3/66:06.6')
        self.assertEqual(str(s), 'abcd:13:07.2/cafe:c0:0f.3/cafe:66:06.6')
        self.assertEqual(
            repr(s),
            "Slot('abcd:13:07.2/cafe:c0:0f.3/cafe:66:06.6')",
        )
        self.assertEqual(s.domain, 0xcafe)
        self.assertEqual(s.bus, 0x66)
        self.assertEqual(s.device, 0x06)
        self.assertEqual(s.function, 0x6)
        self.assertIsInstance(s.parent, Slot)
        assert s.parent is not None  # Required for type checks
        self.assertEqual(s.parent.domain, 0xcafe)
        self.assertEqual(s.parent.bus, 0xc0)
        self.assertEqual(s.parent.device, 0x0f)
        self.assertEqual(s.parent.function, 0x3)
        self.assertIsInstance(s.parent.parent, Slot)
        assert s.parent.parent is not None  # Required for type checks
        self.assertEqual(s.parent.parent.domain, 0xabcd)
        self.assertEqual(s.parent.parent.bus, 0x13)
        self.assertEqual(s.parent.parent.device, 0x07)
        self.assertEqual(s.parent.parent.function, 0x2)


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

    def test_bad_format(self) -> None:
        n = NameWithID('Something [hexa]')
        self.assertIsNone(n.id)
        self.assertEqual(n.name, 'Something [hexa]')


class TestPCIAccessParameter(TestCase):

    def test_normal(self) -> None:
        p = PCIAccessParameter('param.name  Some description (default value)')
        self.assertEqual(p.name, 'param.name')
        self.assertEqual(p.description, 'Some description')
        self.assertEqual(p.default, 'default value')
        self.assertEqual(str(p),
                         'param.name\tSome description (default value)')
        self.assertEqual(repr(p),
                         "PCIAccessParameter('param.name\\tSome description"
                         " (default value)')")

    def test_no_default(self) -> None:
        p = PCIAccessParameter('param.name  Some description ()')
        self.assertEqual(p.name, 'param.name')
        self.assertEqual(p.description, 'Some description')
        self.assertIsNone(p.default)

    def test_bad_format(self) -> None:
        with self.assertRaises(ValueError):
            PCIAccessParameter('nope')
        with self.assertRaises(ValueError):
            PCIAccessParameter('nope (nope)')

    def test_equal(self) -> None:
        p1 = PCIAccessParameter('param.name  Some description (default value)')
        p2 = PCIAccessParameter('param.name  Some description ()')
        self.assertEqual(p1, p1)
        self.assertNotEqual(p1, p2)
