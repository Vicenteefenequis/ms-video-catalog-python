# pylint: disable=no-member

from typing import List
from core.__seedwork.domain.exceptions import NotFoundException
from core.__seedwork.domain.value_objects import UniqueEntityId
from django.core import exceptions as django_exceptions
from core.category.domain.entities import Category
from core.category.domain.repositories import CategoryRepository
from core.category.infra.django_app.mappers import CategoryModelMapper
from core.category.infra.django_app.models import CategoryModel


class CategoryDjangoRepository(CategoryRepository):

    def insert(self, entity: Category) -> None:
        model = CategoryModelMapper.to_model(entity)
        model.save()

    def find_by_id(self, entity_id: str | UniqueEntityId) -> Category:
        id_str = str(entity_id)
        model = self._get(id_str)
        return CategoryModelMapper.to_entity(model)

    def find_all(self) -> List[Category]:
        return [CategoryModelMapper.to_entity(model) for model in CategoryModel.objects.all()]

    def update(self, entity: Category) -> None:
        self._get(entity.id)
        model = CategoryModelMapper.to_model(entity)
        model.save()

    def delete(self, entity_id: str | UniqueEntityId) -> None:
        id_str = str(entity_id)
        model = self._get(id_str)
        model.delete()

    def search(self, input_params: CategoryRepository.SearchParams) -> CategoryRepository.SearchResult:
        raise NotImplementedError()

    def _get(self, entity_id: str) -> CategoryModel:
        try:
            return CategoryModel.objects.get(pk=entity_id)
        except (CategoryModel.DoesNotExist, django_exceptions.ValidationError) as exception:
            raise NotFoundException(
                f"Entity not found using ID '{entity_id}'"
            ) from exception
