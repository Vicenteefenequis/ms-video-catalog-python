

import unittest

from model_bakery import baker
import pytest

from core.__seedwork.domain.exceptions import NotFoundException

from core.category.infra.django_app.models import CategoryModel
from core.category.application.dto import CategoryOutput
from core.category.application.use_cases import CreateCategoryUseCase, GetCategoryUseCase
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
