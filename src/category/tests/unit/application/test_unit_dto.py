

from datetime import datetime
from typing import Optional
import unittest

from category.application.dto import CategoryOutput, CategoryOutputMapper
from category.domain.entities import Category
from category.tests import unit


class TestCategoryOutput(unittest.TestCase):
    def test_fields(self):
        self.assertEqual(CategoryOutput.__annotations__, {
            'id': str,
            'name': str,
            'description': Optional[str],
            'is_active': bool,
            'created_at': datetime
        })


class TestCategoryOutputMapper(unittest.TestCase):
    def test_to_output(self):
        created_at = datetime.now()
        category = Category(
            name='test',
            description='test',
            is_active=True,
            created_at=created_at
        )
        output = CategoryOutputMapper.to_output(category)
        self.assertEqual(output, CategoryOutput(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,  # type: ignore
            created_at=category.created_at  # type: ignore
        ))
