

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TypeVar


from core.category.domain.entities import Category


@dataclass(frozen=True, slots=True)
class CategoryOutput:
    id: str  # pylint: disable=invalid-name
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime


Output = TypeVar('Output', bound=CategoryOutput)


class CategoryOutputMapper:

    output_child: Optional[Output] = CategoryOutput  # type: ignore

    @staticmethod
    def from_child(output_child: Output):
        return CategoryOutputMapper(output_child)  # type: ignore

    @staticmethod
    def without_child():
        return CategoryOutputMapper()

    def to_output(self, category: Category) -> Output:
        return CategoryOutput(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,  # type: ignore
            created_at=category.created_at  # type: ignore
        )
