

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
