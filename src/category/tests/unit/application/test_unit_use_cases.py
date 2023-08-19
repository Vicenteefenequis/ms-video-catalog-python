

from typing import Optional
import unittest
from unittest.mock import patch
from __seedwork.domain.exceptions import NotFoundException
from category.application.dto import CategoryOutput

from category.application.use_cases import CreateCategoryUseCase, GetCategoryUseCase
from category.domain.entities import Category
from category.infra.repositories import CategoryInMemoryRepository


class TestCreateCategoryUseCaseUnit(unittest.TestCase):
    use_case: CreateCategoryUseCase
    category_repo: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = CreateCategoryUseCase(self.category_repo)

    def test_input(self):
        self.assertEqual(CreateCategoryUseCase.Input.__annotations__, {
            'name': str,
            'description': Optional[str],
            'is_active': Optional[bool]
        })
        # pylint: disable=no-member
        description_field = CreateCategoryUseCase.Input.__dataclass_fields__[
            'description']
        self.assertEqual(description_field.default,
                         Category.get_field('description').default)

        # pylint: disable=no-member
        description_field = CreateCategoryUseCase.Input.__dataclass_fields__[
            'is_active']
        self.assertEqual(description_field.default,
                         Category.get_field('is_active').default)

    def test_output(self):
        self.assertTrue(
            issubclass(CreateCategoryUseCase.Output, CategoryOutput)
        )

    def test_execute(self):
        with patch.object(self.category_repo, 'insert', wraps=self.category_repo.insert) as spy_insert:
            input_param = CreateCategoryUseCase.Input(name="Movie")
            output = self.use_case.execute(input_param)
            spy_insert.assert_called_once()
            self.assertEqual(output, CreateCategoryUseCase.Output(
                id=self.category_repo.items[0].id,
                name='Movie',
                is_active=True,
                description=None,
                created_at=self.category_repo.items[0].created_at
            ))

        input_param = CreateCategoryUseCase.Input(
            name='test', description='some description', is_active=False
        )
        output = self.use_case.execute(input_param)
        self.assertEqual(output, CreateCategoryUseCase.Output(
            id=self.category_repo.items[1].id,
            name='test',
            description='some description',
            is_active=False,
            created_at=self.category_repo.items[1].created_at
        ))

        input_param = CreateCategoryUseCase.Input(
            name='test', description='some description', is_active=True
        )

        output = self.use_case.execute(input_param)
        self.assertEqual(output, CreateCategoryUseCase.Output(
            id=self.category_repo.items[2].id,
            name='test',
            description='some description',
            is_active=True,
            created_at=self.category_repo.items[2].created_at
        ))


class TestGetCategoryUseCaseUnit(unittest.TestCase):
    use_case: GetCategoryUseCase
    category_repo: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = GetCategoryUseCase(self.category_repo)

    def test_input(self):
        self.assertEqual(GetCategoryUseCase.Input.__annotations__, {
            'id': str,
        })

    def test_throw_exception_when_category_not_found(self):
        input_param = GetCategoryUseCase.Input(id='fake_id')
        with self.assertRaises(NotFoundException) as assert_error:
            self.use_case.execute(input_param)
        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID 'fake_id'"
        )

    def test_output(self):
        self.assertTrue(
            issubclass(GetCategoryUseCase.Output, CategoryOutput)
        )

    def test_execute(self):
        category = Category(name='Movie')
        self.category_repo.items = [category]
        with patch.object(self.category_repo, 'find_by_id', wraps=self.category_repo.find_by_id) as spy_insert:
            input_param = GetCategoryUseCase.Input(id=category.id)
            output = self.use_case.execute(input_param)
            spy_insert.assert_called_once()
            self.assertEqual(output, GetCategoryUseCase.Output(
                id=self.category_repo.items[0].id,
                name='Movie',
                is_active=True,
                description=None,
                created_at=self.category_repo.items[0].created_at
            ))
