
import unittest

from category.domain.validators import CategoryValidator, CategoryValidatorFactory


class TestCategoryValidationUnit(unittest.TestCase):

    validator: CategoryValidator

    def setUp(self):
        self.validator = CategoryValidatorFactory.create()
        return super().setUp()

    def test_invalidation_cases_for_name_field(self):

        invalid_data = [
            {'data': None, 'expected': 'This field is required.'},
            {'data': {}, 'expected': 'This field is required.'},
            {'data': {'name': None}, 'expected': 'This field may not be null.'},
            {'data': {'name': ''}, 'expected': 'This field may not be blank.'},
            {'data': {'name': 5}, 'expected': 'Not a valid string.'},
            {'data': {'name': 'a' * 256},
                'expected': 'Ensure this field has no more than 255 characters.'},
        ]

        for i in invalid_data:
            is_valid = self.validator.validate(i['data'])  # type: ignore
            self.assertFalse(is_valid)
            self.assertListEqual(
                self.validator.errors['name'],
                [i['expected']],
                f'Expected: {i["expected"]}, Actual: {self.validator.errors["name"]}'
            )

    def test_invalidation_cases_for_description_field(self):
        is_valid = self.validator.validate({'description': 5})  # type: ignore
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['description'],
                             ['Not a valid string.'])

    def test_invalidation_cases_for_is_active_field(self):
        is_valid = self.validator.validate({'is_active': None})  # type: ignore
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['is_active'],
                             ['This field may not be null.'])

        is_valid = self.validator.validate({'is_active': 0})  # type: ignore
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['is_active'],
                             ['Must be a valid boolean.'])

    def test_invalidation_cases_for_created_at_field(self):
        is_valid = self.validator.validate(
            {'created_at': None})  # type: ignore
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['created_at'],
                             ['This field may not be null.'])

        is_valid = self.validator.validate(
            {'created_at': 5})  # type: ignore
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['created_at'],
                             ['Datetime has wrong format. Use one of these formats instead: ' +
                              'YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'])

    def test_validate_cases(self):
        valid_data = [
            {'name': 'Movie'},
            {'name': 'Movie', 'description': None},
            {'name': 'Movie', 'description': ''},
            {'name': 'Movie', 'is_active': True},
            {'name': 'Movie', 'is_active': False},
            {'name': 'Movie', 'description': 'some description', 'is_active': False},
        ]

        for i in valid_data:
            is_valid = self.validator.validate(i)
            self.assertTrue(is_valid)
