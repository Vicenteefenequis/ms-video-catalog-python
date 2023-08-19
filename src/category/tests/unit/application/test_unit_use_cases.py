

import unittest
from unittest.mock import patch

from category.application.use_cases import CreateCategoryUseCase
from category.infra.repositories import CategoryInMemoryRepository


class TestCreateCategoryUseCaseUnit(unittest.TestCase):
    use_case: CreateCategoryUseCase
    category_repo: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = CreateCategoryUseCase(self.category_repo)

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