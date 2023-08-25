
import unittest
import pytest
from django.utils import timezone
from model_bakery import baker

from core.__seedwork.domain.exceptions import NotFoundException
from core.category.infra.django_app.mappers import CategoryModelMapper
from core.category.infra.django_app.models import CategoryModel
from core.category.application.dto import CategoryOutput, CategoryOutputMapper
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    GetCategoryUseCase,
    ListCategoriesUseCase,
    UpdateCategoryUseCase,
)
from core.category.infra.django_app.repositories import CategoryDjangoRepository


@pytest.mark.django_db
class TestCreateCategoryUseCaseInt(unittest.TestCase):

    use_case: CreateCategoryUseCase
    repo: CategoryDjangoRepository

    def setUp(self) -> None:
        self.repo = CategoryDjangoRepository()
        self.use_case = CreateCategoryUseCase(self.repo)

    def test_execute(self):
        input_param = CreateCategoryUseCase.Input(name='Movie')
        output = self.use_case.execute(input_param)

        entity = self.repo.find_by_id(output.id)

        self.assertEqual(output, CategoryOutput(
            id=entity.id,
            name=entity.name,
            description=None,
            is_active=True,
            created_at=entity.created_at,  # type: ignore
        ))

        self.assertEqual(entity.name, 'Movie')
        self.assertIsNone(entity.description)
        self.assertTrue(entity.is_active)


@pytest.mark.django_db
class TestGetCategoryUseCaseUnit(unittest.TestCase):
    use_case: GetCategoryUseCase
    category_repo: CategoryDjangoRepository

    def setUp(self) -> None:
        self.category_repo = CategoryDjangoRepository()
        self.use_case = GetCategoryUseCase(self.category_repo)

    def test_throw_exception_when_category_not_found(self):
        input_param = GetCategoryUseCase.Input(id='fake_id')
        with self.assertRaises(NotFoundException) as assert_error:
            self.use_case.execute(input_param)
        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID 'fake_id'"
        )

    def test_execute(self):
        model = baker.make(CategoryModel)
        input_param = GetCategoryUseCase.Input(model.id)  # type: ignore
        output = self.use_case.execute(input_param)
        self.assertEqual(output, CategoryOutput(
            id=str(model.id),
            name=model.name,
            is_active=model.is_active,
            description=model.description,
            created_at=model.created_at
        ))


@pytest.mark.django_db
class TestListCategoriesUseCase(unittest.TestCase):
    use_case: ListCategoriesUseCase
    category_repo: CategoryDjangoRepository

    def setUp(self) -> None:
        self.category_repo = CategoryDjangoRepository()
        self.use_case = ListCategoriesUseCase(self.category_repo)

    def test_execute_using_empty_search_params(self):
        models = [
            baker.make(CategoryModel, created_at=timezone.now()),
            baker.make(CategoryModel, created_at=timezone.now()),
        ]

        input_param = ListCategoriesUseCase.Input()
        output = self.use_case.execute(input_param)
        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=[
                self.from_model_to_output(models[1]),
                self.from_model_to_output(models[0]),
            ],
            total=2,
            current_page=1,
            per_page=15,
            last_page=1
        ))

    def test_execute_using_pagination_and_sort_and_filter(self):
        models = [
            baker.make(CategoryModel, name='a'),
            baker.make(CategoryModel, name='AAA'),
            baker.make(CategoryModel, name='AaA'),
            baker.make(CategoryModel, name='b'),
            baker.make(CategoryModel, name='c'),
        ]

        input_param = ListCategoriesUseCase.Input(
            page=1, per_page=2, sort='name', sort_dir='asc', filter='a'
        )

        output = self.use_case.execute(input_param)
        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=[
                self.from_model_to_output(models[1]),
                self.from_model_to_output(models[2]),
            ],
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
            items=[self.from_model_to_output(models[0])],
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
            items=[self.from_model_to_output(
                models[0]), self.from_model_to_output(models[2])],
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
            items=[
                self.from_model_to_output(models[1])
            ],
            total=3,
            current_page=2,
            per_page=2,
            last_page=2
        ))

    def from_model_to_output(self, model: CategoryModel) -> CategoryOutput:
        entity = CategoryModelMapper.to_entity(model)
        return CategoryOutputMapper.without_child().to_output(entity)


@pytest.mark.django_db
class TestUpdateCategoryUseCase(unittest.TestCase):
    category_repo: CategoryDjangoRepository
    use_case: UpdateCategoryUseCase

    def setUp(self) -> None:
        self.category_repo = CategoryDjangoRepository()
        self.use_case = UpdateCategoryUseCase(self.category_repo)

    def test_execute(self):
        model = baker.make(CategoryModel, name='Movie')

        input_param = UpdateCategoryUseCase.Input(
            id=str(model.id),
            name='Movie 2',
            description='some description',
            is_active=False
        )
        output = self.use_case.execute(input_param)
        self.assertEqual(output, CategoryOutput(
            id=str(model.id),
            name='Movie 2',
            description='some description',
            is_active=False,
            created_at=model.created_at
        ))

        category = self.category_repo.find_by_id(str(model.id))
        self.assertEqual(category.name, 'Movie 2')
        self.assertEqual(category.description, 'some description')
        self.assertFalse(category.is_active)
        self.assertEqual(category.created_at, model.created_at)

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
