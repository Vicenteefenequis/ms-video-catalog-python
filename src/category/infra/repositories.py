

from __seedwork.domain.repositories import InMemoryRepository
from category.domain.repositories import CategoryRepository


class CategoryInMemoryRepository(CategoryRepository, InMemoryRepository):
    pass
