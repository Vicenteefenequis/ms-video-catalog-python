

from datetime import datetime, timedelta
from typing import Optional
import unittest
from unittest.mock import patch
from __seedwork.application.dto import SearchInput
from __seedwork.application.use_cases import UseCase
from __seedwork.domain.exceptions import NotFoundException
from category.application.dto import CategoryOutput, CategoryOutputMapper

from category.application.use_cases import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    GetCategoryUseCase,
    ListCategoriesUseCase,
    UpdateCategoryUseCase
)
from category.domain.entities import Category
from category.infra.repositories import CategoryInMemoryRepository


class TestCreateCategoryUseCaseUnit(unittest.TestCase):
    use_case: CreateCategoryUseCase
    category_repo: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = CreateCategoryUseCase(
            self.category_repo)  # type: ignore

    def test_if_is_instance_a_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

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
        with patch.object(
            self.category_repo,
            'insert',
            wraps=self.category_repo.insert
        ) as spy_insert:
            input_param = CreateCategoryUseCase.Input(name="Movie")
            output = self.use_case.execute(input_param)
            spy_insert.assert_called_once()
            self.assertEqual(output, CategoryOutput(
                id=self.category_repo.items[0].id,
                name='Movie',
                is_active=True,
                description=None,
                created_at=self.category_repo.items[0].created_at
            ))

        input_param = CreateCategoryUseCase.Input(
            name='test',
            description='some description',
            is_active=False
        )
        output = self.use_case.execute(input_param)
        self.assertEqual(output, CategoryOutput(
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
        self.assertEqual(output, CategoryOutput(
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

    def test_if_is_instance_a_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

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
        with patch.object(
            self.category_repo,
            'find_by_id',
            wraps=self.category_repo.find_by_id
        ) as spy_insert:
            input_param = GetCategoryUseCase.Input(id=category.id)
            output = self.use_case.execute(input_param)
            spy_insert.assert_called_once()
            self.assertEqual(output, CategoryOutput(
                id=self.category_repo.items[0].id,
                name='Movie',
                is_active=True,
                description=None,
                created_at=self.category_repo.items[0].created_at
            ))


class TestListCategoriesUseCase(unittest.TestCase):
    use_case: ListCategoriesUseCase
    category_repo: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = ListCategoriesUseCase(self.category_repo)

    def test_instance_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

    def test_input(self):
        self.assertTrue(issubclass(ListCategoriesUseCase.Input, SearchInput))

    def test_execute_using_empty_search_params(self):
        self.category_repo.items = [
            Category(name='test 1'),
            Category(
                name='test 2',
                created_at=datetime.now() + timedelta(seconds=200)
            ),
        ]

        with patch.object(
            self.category_repo,
            'search',
            wraps=self.category_repo.search
        ) as spy_search:
            input_param = ListCategoriesUseCase.Input()
            output = self.use_case.execute(input_param)
            spy_search.assert_called_once()
            self.assertEqual(output, ListCategoriesUseCase.Output(
                items=list(
                    map(
                        CategoryOutputMapper.without_child().to_output,
                        self.category_repo.items[::-1]
                    )
                ),
                total=2,
                current_page=1,
                per_page=15,
                last_page=1
            ))

    def test_execute_using_pagination_and_sort_and_filter(self):
        items = [
            Category(name='a'),
            Category(name='AAA'),
            Category(name='AaA'),
            Category(name='b'),
            Category(name='c'),
        ]
        self.category_repo.items = items

        input_param = ListCategoriesUseCase.Input(
            page=1, per_page=2, sort='name', sort_dir='asc', filter='a'
        )

        output = self.use_case.execute(input_param)
        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=list(
                map(
                    CategoryOutputMapper.without_child().to_output,
                    [items[1], items[2]]
                )
            ),
            total=3,
            current_page=1,
            per_page=2,
            last_page=2
        ))

        input_param = ListCategoriesUseCase.Input(
            page=2, per_page=2, sort='name', sort_dir='asc', filter='a'
        )

        output = self.use_case.execute(input_param)
        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=list(
                map(
                    CategoryOutputMapper.without_child().to_output,
                    [items[0]]
                )
            ),
            total=3,
            current_page=2,
            per_page=2,
            last_page=2
        ))

        input_param = ListCategoriesUseCase.Input(
            page=1, per_page=2, sort='name', sort_dir='desc', filter='a'
        )

        output = self.use_case.execute(input_param)

        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=list(
                map(
                    CategoryOutputMapper.without_child().to_output,
                    [items[0], items[2]]
                )
            ),
            total=3,
            current_page=1,
            per_page=2,
            last_page=2
        ))

        input_param = ListCategoriesUseCase.Input(
            page=2, per_page=2, sort='name', sort_dir='desc', filter='a'
        )

        output = self.use_case.execute(input_param)

        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=list(
                map(
                    CategoryOutputMapper.without_child().to_output,
                    [items[1]]
                )
            ),
            total=3,
            current_page=2,
            per_page=2,
            last_page=2
        ))


class TestUpdateCategoryUseCase(unittest.TestCase):
    category_repo: CategoryInMemoryRepository
    use_case: UpdateCategoryUseCase

    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = UpdateCategoryUseCase(self.category_repo)

    def test_if_is_instance_a_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

    def test_input(self):
        self.assertEqual(UpdateCategoryUseCase.Input.__annotations__, {
            'id': str,
            'name': str,
            'description': Optional[str],
            'is_active': Optional[bool]
        })

    def test_output(self):
        self.assertTrue(
            issubclass(UpdateCategoryUseCase.Output, CategoryOutput)
        )

    def test_execute(self):
        category = Category(name='Movie')
        self.category_repo.items = [category]

        with patch.object(
            self.category_repo,
            'find_by_id',
            wraps=self.category_repo.find_by_id
        ) as spy_find_by_id, \
                patch.object(
            self.category_repo,
            'update',
            wraps=self.category_repo.update
        ) as spy_update:
            input_param = UpdateCategoryUseCase.Input(
                id=category.id,
                name='Movie 2',
                description='some description',
                is_active=False
            )
            output = self.use_case.execute(input_param)
            spy_find_by_id.assert_called_once()
            spy_update.assert_called_once()
            self.assertEqual(output, CategoryOutput(
                id=self.category_repo.items[0].id,
                name='Movie 2',
                description='some description',
                is_active=False,
                created_at=self.category_repo.items[0].created_at
            ))

        input_param = UpdateCategoryUseCase.Input(
            id=category.id,
            name='Movie 2',
            description='some description',
            is_active=True
        )

        output = self.use_case.execute(input_param)

        self.assertEqual(output, CategoryOutput(
            id=self.category_repo.items[0].id,
            name='Movie 2',
            description='some description',
            is_active=True,
            created_at=self.category_repo.items[0].created_at
        ))

    def test_throw_exception_when_category_not_found(self):
        input_param = UpdateCategoryUseCase.Input(
            id='fake_id',
            name='Movie 2',
            description='some description',
            is_active=True
        )
        with self.assertRaises(NotFoundException) as assert_error:
            self.use_case.execute(input_param)
        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID 'fake_id'"
        )


class TestDeleteCategoryUseCase(unittest.TestCase):
    category_repo: CategoryInMemoryRepository
    use_case: DeleteCategoryUseCase

    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = DeleteCategoryUseCase(self.category_repo)

    def test_if_is_instance_a_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

    def test_input(self):
        self.assertEqual(
            DeleteCategoryUseCase.Input.__annotations__, {
                'id': str,
            }
        )

    def test_execute(self):
        category = Category(name='Movie')
        self.category_repo.items = [category]

        with patch.object(
            self.category_repo,
            'delete',
            wraps=self.category_repo.delete
        ) as spy_delete:
            input_param = DeleteCategoryUseCase.Input(id=category.id)
            self.use_case.execute(input_param)
            spy_delete.assert_called_once()

    def test_throw_exception_when_category_not_found(self):
        input_param = DeleteCategoryUseCase.Input(id='fake_id')
        with self.assertRaises(NotFoundException) as assert_error:
            self.use_case.execute(input_param)
        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID 'fake_id'"
        )
