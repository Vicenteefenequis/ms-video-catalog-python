import unittest
from rest_framework import serializers
from core.__seedwork.domain.validators import DRFValidator, StrictBooleanField, StrictCharField
# pylint: disable=abstract-method


class StubSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.IntegerField()


class TestDRFValidatorIntegration(unittest.TestCase):

    def test_validation_with_error(self):
        validator = DRFValidator()
        serializer = StubSerializer(data={})  # type: ignore
        serializer.is_valid()
        is_valid = validator.validate(serializer)
        self.assertFalse(is_valid)
        self.assertEqual(validator.errors, {
            'name': ['This field is required.'],
            'price': ['This field is required.']
        })

    def test_validate_without_error(self):
        validator = DRFValidator()
        serializer = StubSerializer(
            data={'name': 'some value', 'price': 2}  # type: ignore
        )
        serializer.is_valid()
        is_valid = validator.validate(serializer)
        self.assertTrue(is_valid)
        self.assertEqual(validator.validated_data, {
            'name': 'some value',
            'price': 2
        })


class TestStrictCharFieldUnit(unittest.TestCase):
    def test_if_is_invalid_when_not_str_values(self):

        class StubStrictCharFieldSerializer(serializers.Serializer):
            field = StrictCharField()

        serializer = StubStrictCharFieldSerializer(
            data={'field': 1}  # type: ignore
        )
        serializer.is_valid()
        self.assertEqual(serializer.errors, {
            'field':
            [serializers.ErrorDetail(
                string='Not a valid string.',
                code='invalid'
            )]
        })

        serializer = StubStrictCharFieldSerializer(
            data={'field': True})  # type: ignore
        serializer.is_valid()
        self.assertEqual(serializer.errors, {
            'field':
            [serializers.ErrorDetail(
                string='Not a valid string.',
                code='invalid'
            )]
        })

    def test_none_value_is_valid(self):
        class StubStrictCharFieldSerializer(serializers.Serializer):
            field = StrictCharField(required=False, allow_null=True)

        serializer = StubStrictCharFieldSerializer(
            data={'field': None}  # type: ignore
        )
        self.assertTrue(serializer.is_valid())

    def test_value_is_valid(self):
        class StubStrictCharFieldSerializer(serializers.Serializer):
            field = StrictCharField(required=False, allow_null=True)

        serializer = StubStrictCharFieldSerializer(
            data={'field': 'some value'}  # type: ignore
        )
        self.assertTrue(serializer.is_valid())


class TestStrictBooleanFieldInt(unittest.TestCase):
    def test_if_is_invalid_when_not_bool_values(self):

        class StubStrictBooleanFieldSerializer(serializers.Serializer):
            active = StrictBooleanField()

        message_error = 'Must be a valid boolean.'

        serializer = StubStrictBooleanFieldSerializer(
            data={'active': 0}  # type: ignore
        )
        serializer.is_valid()
        self.assertEqual(serializer.errors, {
            'active':
            [serializers.ErrorDetail(
                string=message_error,
                code='invalid'
            )]
        })

        serializer = StubStrictBooleanFieldSerializer(
            data={'active': 1}  # type: ignore
        )
        serializer.is_valid()
        self.assertEqual(serializer.errors, {
            'active':
            [serializers.ErrorDetail(
                string=message_error,
                code='invalid'
            )]
        })

        serializer = StubStrictBooleanFieldSerializer(
            data={'active': 'True'}  # type: ignore
        )
        serializer.is_valid()
        self.assertEqual(serializer.errors, {
            'active':
            [serializers.ErrorDetail(
                string=message_error,
                code='invalid'
            )]
        })

        serializer = StubStrictBooleanFieldSerializer(
            data={'active': 'False'}  # type: ignore
        )
        serializer.is_valid()
        self.assertEqual(serializer.errors, {
            'active':
            [serializers.ErrorDetail(
                string=message_error,
                code='invalid'
            )]
        })

    def test_value_is_valid(self):
        class StubStrictBooleanFieldSerializer(serializers.Serializer):
            active = StrictBooleanField(allow_null=True)

        serializer = StubStrictBooleanFieldSerializer(
            data={'active': None}  # type: ignore
        )
        self.assertTrue(serializer.is_valid())

        serializer = StubStrictBooleanFieldSerializer(
            data={'active': True}  # type: ignore
        )
        self.assertTrue(serializer.is_valid())

        serializer = StubStrictBooleanFieldSerializer(
            data={'active': False}  # type: ignore
        )
        self.assertTrue(serializer.is_valid())
