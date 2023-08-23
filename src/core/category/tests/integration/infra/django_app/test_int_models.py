
# pylint: disable=no-member
import unittest
from django.db import connections
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.utils import timezone
import pytest

from core.category.infra.django_app.models import CategoryModel


@pytest.mark.django_db()
class TestCategoryModelInt(unittest.TestCase):

    def test_create(self):
        arrange = {
            'id': '114e527b-d222-44f1-86c7-1cb621f44849',
            'name': 'Category 1',
            'description': None,
            'is_active': True,
            'created_at': timezone.now()
        }
        category = CategoryModel.objects.create(**arrange)

        self.assertEqual(category.id, arrange['id'])
        self.assertEqual(category.name, arrange['name'])
        self.assertIsNone(category.description)
        self.assertEqual(category.is_active, arrange['is_active'])
        self.assertEqual(category.created_at, arrange['created_at'])
