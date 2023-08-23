
# pylint: disable=no-member
import unittest
from core.category.domain.entities import Category
from core.category.infra.django_app.models import CategoryModel
from core.category.infra.django_app.repositories import CategoryDjangoRepository

import pytest


@pytest.mark.django_db
class TestCategoryDjangoRepositoryInt(unittest.TestCase):

    repo: CategoryDjangoRepository

    def setUp(self) -> None:
        self.repo = CategoryDjangoRepository()

    def test_insert(self):
        category = Category(
            name='Movie',
        )
        self.repo.insert(category)
        model = CategoryModel.objects.get(pk=category.id)

        self.assertEqual(str(model.id), category.id)
        self.assertEqual(model.name, 'Movie')
        self.assertIsNone(model.description)
        self.assertTrue(model.is_active)
        self.assertEqual(model.created_at, category.created_at)

        category = Category(
            name='Movie 2',
            description='some description',
            is_active=False,
        )

        self.repo.insert(category)

        model = CategoryModel.objects.get(pk=category.id)

        self.assertEqual(str(model.id), category.id)
        self.assertEqual(model.name, 'Movie 2')
        self.assertEqual(model.description, 'some description')
        self.assertFalse(model.is_active)
        self.assertEqual(model.created_at, category.created_at)
