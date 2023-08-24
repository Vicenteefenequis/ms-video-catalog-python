

import unittest
import pytest
from django.utils import timezone
from core.category.domain.entities import Category
from core.category.infra.django_app.mappers import CategoryModelMapper
from core.category.infra.django_app.models import CategoryModel


@pytest.mark.django_db
class TestCategoryModelMapper(unittest.TestCase):
    def test_to_entity(self):
        created_at = timezone.now()
        model = CategoryModel(
            id='114e527b-d222-44f1-86c7-1cb621f44849',
            name='Movie',
            description='some description',
            is_active=False,
            created_at=created_at,
        )
        category = CategoryModelMapper.to_entity(model)

        self.assertEqual(str(model.id), category.id)
        self.assertEqual(model.name, 'Movie')
        self.assertEqual(model.description, 'some description')
        self.assertFalse(model.is_active)
        self.assertEqual(created_at, category.created_at)

    def test_to_model(self):
        category = Category(
            name='Movie',
        )
        model = CategoryModelMapper.to_model(category)

        self.assertEqual(model.name, 'Movie')
        self.assertIsNone(model.description)
        self.assertTrue(model.is_active)
        self.assertEqual(model.created_at, category.created_at)

        category = Category(
            name='Movie 2',
            description='some description',
            is_active=False,
        )

        model = CategoryModelMapper.to_model(category)

        self.assertEqual(model.name, 'Movie 2')
        self.assertEqual(model.description, 'some description')
        self.assertFalse(model.is_active)
        self.assertEqual(model.created_at, category.created_at)
