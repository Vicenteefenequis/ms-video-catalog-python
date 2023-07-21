import unittest
from rest_framework import serializers
from __seedwork.domain.validators import DRFValidator

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
