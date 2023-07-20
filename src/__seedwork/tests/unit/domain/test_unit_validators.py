

import unittest
from __seedwork.domain.exceptions import ValidationException

from __seedwork.domain.validators import ValidatorRules


class TestValidatorRules(unittest.TestCase):
    def test_values_method(self):
        validator = ValidatorRules.values('some value', 'prop')
        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual(validator.value, 'some value')
        self.assertEqual(validator.prop, 'prop')

    def test_required_rule(self):

        invalid_data = [
            {'value': None, 'prop': 'prop'},
            {'value': "", 'prop': 'prop'},
        ]

        for i in invalid_data:
            msg = f'value: {i["value"]}, prop: {i["prop"]}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                # pylint: disable=expression-not-assigned
                ValidatorRules.values(i['value'], i['prop']).required()
            self.assertEqual(
                assert_error.exception.args[0],
                'The prop is required'
            )

        valid_data = [
            {'value': "test", 'prop': 'prop'},
            {'value': 5, 'prop': 'prop'},
            {'value': 0, 'prop': 'prop'},
            {'value': False, 'prop': 'prop'},
        ]

        for i in valid_data:
            self.assertIsInstance(
                ValidatorRules.values(i['value'], i['prop']).required(),
                ValidatorRules
            )

    def test_string_rule(self):

        invalid_data = [
            {'value': 5, 'prop': 'prop'},
            {'value': True, 'prop': 'prop'},
            {'value': {}, 'prop': 'prop'},
        ]

        for i in invalid_data:
            msg = f'value: {i["value"]}, prop: {i["prop"]}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                # pylint: disable=expression-not-assigned
                ValidatorRules.values(i['value'], i['prop']).string()
            self.assertEqual(
                assert_error.exception.args[0],
                'The prop must be a string'
            )

        valid_data = [
            {'value': None, 'prop': 'prop'},
            {'value': "", 'prop': 'prop'},
            {'value': "some value", 'prop': 'prop'},
        ]

        for i in valid_data:
            self.assertIsInstance(
                ValidatorRules.values(i['value'], i['prop']).string(),
                ValidatorRules
            )

    def test_max_length_rule(self):

        invalid_data = [
            {'value': "t" * 5, 'prop': 'prop'},
        ]

        for i in invalid_data:
            msg = f'value: {i["value"]}, prop: {i["prop"]}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                # pylint: disable=expression-not-assigned
                ValidatorRules.values(i['value'], i['prop']).max_length(4)
            self.assertEqual(
                assert_error.exception.args[0],
                'The prop must be less than 4 characters'
            )

        valid_data = [
            {'value': None, 'prop': 'prop'},
            {'value': "t" * 4, 'prop': 'prop'}
        ]

        for i in valid_data:
            self.assertIsInstance(
                ValidatorRules.values(i['value'], i['prop']).max_length(4),
                ValidatorRules
            )

    def test_boolean_rule(self):

        invalid_data = [
            {'value': "", 'prop': 'prop'},
            {'value': {}, 'prop': 'prop'},
            {'value': 5, 'prop': 'prop'}
        ]

        for i in invalid_data:
            msg = f'value: {i["value"]}, prop: {i["prop"]}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                # pylint: disable=expression-not-assigned
                ValidatorRules.values(i['value'], i['prop']).boolean()
            self.assertEqual(
                assert_error.exception.args[0],
                'The prop must be a boolean'
            )

        valid_data = [
            {'value': True, 'prop': 'prop'},
            {'value': False, 'prop': 'prop'}
        ]

        for i in valid_data:
            self.assertIsInstance(
                ValidatorRules.values(i['value'], i['prop']).boolean(),
                ValidatorRules
            )
