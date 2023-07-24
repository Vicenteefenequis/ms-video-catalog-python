

from dataclasses import dataclass
import unittest
from __seedwork.domain.entities import Entity
from __seedwork.domain.exceptions import NotFoundException

from __seedwork.domain.repositories import InMemoryRepository, RepositoryInterface
from __seedwork.domain.value_objects import UniqueEntityId


class TestRepositoryInterface(unittest.TestCase):

    def test_throw_error_when_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            RepositoryInterface()  # type: ignore
        self.assertEqual(
            assert_error.exception.args[0], "Can't instantiate abstract class RepositoryInterface with abstract methods " +
            "delete, find_all, find_by_id, insert, update")


@dataclass(frozen=True, kw_only=True, slots=True)
class StubEntity(Entity):
    name: str
    price: float


class StubInMemoryRepository(InMemoryRepository[StubEntity]):
    pass


class TestInMemoryRepository(unittest.TestCase):
    repo: StubInMemoryRepository

    def setUp(self) -> None:
        self.repo = StubInMemoryRepository()
        return super().setUp()

    def test_items_prop_is_empty_on_init(self):
        self.assertEqual(self.repo.items, [])

    def test_insert(self):
        entity = StubEntity(name='test', price=10.0)
        self.repo.insert(entity)
        self.assertEqual(self.repo.items, [entity])

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
            assert_error.exception.args[0], "Entity not found using ID '114e527b-d222-44f1-86c7-1cb621f44849'")

    def test_find_by_id(self):
        entity = StubEntity(name='test', price=10.0)
        self.repo.insert(entity)
        self.assertEqual(self.repo.find_by_id(entity.id), entity)

    def test_find_all(self):
        entity = StubEntity(name='test', price=10.0)
        self.repo.insert(entity)
        self.assertEqual(self.repo.find_all(), [entity])

    def test_throw_not_found_exception_in_update(self):

        entity = StubEntity(name='test', price=10.0)
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.update(entity)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not found using ID '{entity.id}'")

        unique_entity_id = UniqueEntityId(
            '114e527b-d222-44f1-86c7-1cb621f44849')
        entity = StubEntity(unique_entity_id=unique_entity_id,
                            name='test', price=10.0)
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID '114e527b-d222-44f1-86c7-1cb621f44849'")

    def test_update(self):
        entity = StubEntity(name='test', price=10.0)
        self.repo.insert(entity)
        entity._set('name', 'test2')
        self.repo.update(entity)
        self.assertEqual(self.repo.find_by_id(entity.id), entity)

    def test_throw_not_found_exception_in_delete(self):
        entity = StubEntity(name='test', price=10.0)
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete(entity.id)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not found using ID '{entity.id}'")

        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete(entity.unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not found using ID '{entity.id}'")

    def test_delete(self):
        entity = StubEntity(name='test', price=10.0)
        self.repo.insert(entity)

        self.repo.delete(entity.id)
        self.assertListEqual(self.repo.items, [])

        entity = StubEntity(name='test', price=10.0)
        self.repo.insert(entity)

        self.repo.delete(entity.unique_entity_id)
        self.assertListEqual(self.repo.items, [])
