
# pylint: disable=no-member
import unittest
from core.__seedwork.domain.exceptions import NotFoundException
from core.__seedwork.domain.value_objects import UniqueEntityId
from core.category.domain.entities import Category
from core.category.infra.django_app.mappers import CategoryModelMapper
from core.category.infra.django_app.models import CategoryModel
from core.category.infra.django_app.repositories import CategoryDjangoRepository
from model_bakery import baker

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

    def test_throw_not_found_exception_in_find_by_id(self):
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id('not-found')
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'not-found'")

        unique_entity_id = UniqueEntityId(
            '114e527b-d222-44f1-86c7-1cb621f44849')
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID '114e527b-d222-44f1-86c7-1cb621f44849'"
        )

    def test_find_by_id(self):
        category = Category(
            name='Movie',
        )
        self.repo.insert(category)

        category_found = self.repo.find_by_id(category.id)

        self.assertEqual(category_found, category)

        category_found = self.repo.find_by_id(category.unique_entity_id)
        self.assertEqual(category_found, category)

    def test_find_all(self):
        models = baker.make(CategoryModel, _quantity=2)

        categories = self.repo.find_all()

        self.assertEqual(len(categories), 2)
        self.assertEqual(
            categories[0], CategoryModelMapper.to_entity(models[0])
        )
        self.assertEqual(
            categories[1], CategoryModelMapper.to_entity(models[1])
        )

    def test_throw_not_found_exception_in_update(self):
        entity = Category(
            name='Movie',
        )
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.update(entity)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not found using ID '{entity.id}'"
        )

    def test_update(self):
        category = Category(
            name='Movie',
        )
        self.repo.insert(category)

        category.update('Movie 2', 'some description')

        self.repo.update(category)

        model = CategoryModel.objects.get(pk=category.id)

        self.assertEqual(str(model.id), category.id)
        self.assertEqual(model.name, 'Movie 2')
        self.assertEqual(model.description, 'some description')
        self.assertTrue(model.is_active)
        self.assertEqual(model.created_at, category.created_at)

    def test_throw_not_found_exception_in_delete(self):
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete('not-found')
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'not-found'")

        unique_entity_id = UniqueEntityId(
            '114e527b-d222-44f1-86c7-1cb621f44849')
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete(unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID '114e527b-d222-44f1-86c7-1cb621f44849'"
        )

    def test_delete(self):
        category = Category(
            name='Movie',
        )
        self.repo.insert(category)

        self.repo.delete(category.id)

        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(category.id)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not found using ID '{category.id}'"
        )
