from dataclasses import FrozenInstanceError, is_dataclass
from datetime import datetime
import unittest
from category.domain.entities import Category


class TestCategory(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_constructor(self):
        category = Category(name='Movie')
        self.assertEqual(category.name, 'Movie')
        self.assertEqual(category.description, None)
        self.assertEqual(category.is_active, True)
        self.assertIsInstance(category.created_at, datetime)

        created_at = datetime.now()
        category = Category(
            name='Movie',
            description='some description',
            is_active=False,
            created_at=created_at
        )

        self.assertEqual(category.name, 'Movie')
        self.assertEqual(category.description, 'some description')
        self.assertEqual(category.is_active, False)
        self.assertEqual(category.created_at, created_at)

    def test_if_created_at_is_generated_in_constructor(self):
        category1 = Category(name='Movie 1')
        category2 = Category(name='Movie 2')

        self.assertNotEqual(category1.created_at, category2.created_at)

    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            category = Category(name='Movie 1')
            category.name = 'any_id'  # type: ignore

    def test_update(self):
        category = Category(name='Movie 1')

        self.assertEqual(category.name, 'Movie 1')
        self.assertIsNone(category.description)
        self.assertTrue(category.is_active)

        category.update('Movie updated', 'Movie description')

        self.assertEqual(category.name, 'Movie updated')
        self.assertEqual(category.description, 'Movie description')
        self.assertTrue(category.is_active)

    def test_deactivate(self):
        category = Category(name='Movie 1')

        self.assertEqual(category.name, 'Movie 1')
        self.assertIsNone(category.description)
        self.assertTrue(category.is_active)

        category.deactivate()

        self.assertEqual(category.name, 'Movie 1')
        self.assertIsNone(category.description)
        self.assertFalse(category.is_active)

    def test_activate(self):
        category = Category(
            name='Movie 1',
            description='Description 1',
            is_active=False
        )

        self.assertEqual(category.name, 'Movie 1')
        self.assertEqual(category.description, 'Description 1')
        self.assertFalse(category.is_active)

        category.activate()

        self.assertEqual(category.name, 'Movie 1')
        self.assertEqual(category.description, 'Description 1')
        self.assertTrue(category.is_active)
