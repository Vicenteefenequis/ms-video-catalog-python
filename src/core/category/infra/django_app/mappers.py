from core.__seedwork.domain.exceptions import EntityValidationException, LoadEntityException
from core.__seedwork.domain.value_objects import UniqueEntityId
from core.category.domain.entities import Category
from core.category.infra.django_app.models import CategoryModel


class CategoryModelMapper:

    @staticmethod
    def to_entity(category_model: CategoryModel) -> Category:
        try:
            return Category(
                unique_entity_id=UniqueEntityId(str(category_model.id)),
                name=category_model.name,
                description=category_model.description,
                is_active=category_model.is_active,
                created_at=category_model.created_at,
            )
        except EntityValidationException as exception:
            raise LoadEntityException(exception.error) from exception

    @staticmethod
    def to_model(category: Category) -> CategoryModel:
        return CategoryModel(**category.to_dict())
