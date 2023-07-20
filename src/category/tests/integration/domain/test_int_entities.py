

import unittest
from __seedwork.domain.exceptions import ValidationException

from category.domain.entities import Category


class TestCategoryIntegration(unittest.TestCase):

    def test_invalid_cases_for_name_prop(self):
        with self.assertRaises(ValidationException) as assert_error:
            Category(name=None)  # type: ignore
        self.assertEqual(
            assert_error.exception.args[0],
            "The name is required"
        )

        with self.assertRaises(ValidationException) as assert_error:
            Category(name='')
        self.assertEqual(
            assert_error.exception.args[0],
            "The name is required"
        )

        with self.assertRaises(ValidationException) as assert_error:
            Category(name=5)  # type: ignore
        self.assertEqual(
            assert_error.exception.args[0],
            "The name must be a string"
        )

        with self.assertRaises(ValidationException) as assert_error:
            Category(name="t" * 256)  # type: ignore
        self.assertEqual(
            assert_error.exception.args[0],
            "The name must be less than 255 characters"
        )

    def test_invalid_cases_for_description_prop(self):
        with self.assertRaises(ValidationException) as assert_error:
            Category(name='Movie', description=5)  # type: ignore
        self.assertEqual(
            assert_error.exception.args[0],
            "The description must be a string"
        )

    def test_invalid_cases_for_is_active_prop(self):
        with self.assertRaises(ValidationException) as assert_error:
            Category(name='Movie', is_active=5)  # type: ignore
        self.assertEqual(
            assert_error.exception.args[0],
            "The is_active must be a boolean"
        )
