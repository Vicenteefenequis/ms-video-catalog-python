

from abc import ABC
from dataclasses import FrozenInstanceError, dataclass, is_dataclass
import unittest
from unittest.mock import patch
from __seedwork.domain.exceptions import InvalidUuidException
from __seedwork.domain.value_objects import UniqueEntityId, ValueObject
import uuid


@dataclass(frozen=True)
class StubOneProp(ValueObject):
    prop: str


@dataclass(frozen=True)
class StubTwoProp(ValueObject):
    prop1: str
    prop2: str


class TestValueObjectUnit(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(ValueObject))

    def test_if_is_a_abstract_class(self):
        self.assertIsInstance(ValueObject(), ABC)

    def test_init_prop(self):
        vo1 = StubOneProp(prop='value')
        self.assertEqual(vo1.prop, 'value')

        vo2 = StubTwoProp(prop1='value1', prop2='value2')
        self.assertEqual(vo2.prop1, 'value1')
        self.assertEqual(vo2.prop2, 'value2')

    def test_convert_to_string(self):
        vo1 = StubOneProp(prop='value')
        self.assertEqual(vo1.prop,  str(vo1))

        vo2 = StubTwoProp(prop1='value1', prop2='value2')
        self.assertEqual('{"prop1": "value1", "prop2": "value2"}', str(vo2))

    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = StubOneProp(prop='1')
            value_object.prop = 'any_id'  # type: ignore


class TestUniqueEntityIdUnit(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_throw_exception_when_uuid_is_invalid(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate  # type: ignore
        ) as mock_validate:
            with self.assertRaises(InvalidUuidException) as assert_error:
                UniqueEntityId('fake_id')
            mock_validate.assert_called_once()
            self.assertEqual(
                assert_error.exception.args[0], "ID must be a valid UUID")

    def test_accept_uuid_passed_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate  # type: ignore
        ) as mock_validate:
            value_object = UniqueEntityId(
                '114e527b-d222-44f1-86c7-1cb621f44849')
            mock_validate.assert_called_once()
            self.assertEqual(
                value_object.id, '114e527b-d222-44f1-86c7-1cb621f44849')

        uuid_value = uuid.uuid4()
        value_object = UniqueEntityId(uuid_value)  # type: ignore
        self.assertEqual(value_object.id, str(uuid_value))

    def test_generate_id_when_no_passed_id_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate  # type: ignore
        ) as mock_validate:
            value_object = UniqueEntityId()
            uuid.UUID(value_object.id)
            mock_validate.assert_called_once()

    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = UniqueEntityId()
            value_object.id = 'any_id'  # type: ignore
