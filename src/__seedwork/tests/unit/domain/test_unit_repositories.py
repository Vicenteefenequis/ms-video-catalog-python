

from dataclasses import dataclass
from typing import Optional
import unittest
from __seedwork.domain.entities import Entity
from __seedwork.domain.exceptions import NotFoundException

from __seedwork.domain.repositories import Filter, InMemoryRepository, RepositoryInterface, SearchParams, SearchableRepositoryInterface
from __seedwork.domain.value_objects import UniqueEntityId


class TestRepositoryInterface(unittest.TestCase):
    def test_throw_error_when_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            RepositoryInterface()  # type: ignore
        self.assertEqual(
            assert_error.exception.args[0],
            "Can't instantiate abstract class RepositoryInterface with abstract methods " +
            "delete, find_all, find_by_id, insert, update"
        )


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
            assert_error.exception.args[0],
            "Entity not found using ID '114e527b-d222-44f1-86c7-1cb621f44849'"
        )

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
            assert_error.exception.args[0],
            "Entity not found using ID '114e527b-d222-44f1-86c7-1cb621f44849'"
        )

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


class TestSearchableRepository(unittest.TestCase):
    def test_throw_error_when_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            SearchableRepositoryInterface()  # type: ignore
        self.assertEqual(
            "Can't instantiate abstract class SearchableRepositoryInterface with abstract" +
            " methods delete, find_all, find_by_id, insert, search, update",
            assert_error.exception.args[0]
        )


class TestSearchParams(unittest.TestCase):

    def test_props_annotations(self):
        self.assertEqual(SearchParams.__annotations__, {
            'page': Optional[int],
            'per_page': Optional[int],
            'sort': Optional[str],
            'sort_dir': Optional[str],
            'filter': Optional[Filter]
        })

    def test_page_prop(self):
        params = SearchParams()
        self.assertEqual(params.page, 1)

        arrange = [
            {'page': None, 'excepted': 1},
            {'page': "", 'excepted': 1},
            {'page': "fake", 'excepted': 1},
            {'page': 0, 'excepted': 1},
            {'page': -1, 'excepted': 1},
            {'page': "0", 'excepted': 1},
            {'page': "-1", 'excepted': 1},
            {'page': 5.5, 'excepted': 5},
            {'page': True, 'excepted': 1},
            {'page': False, 'excepted': 1},
            {'page': {}, 'excepted': 1},
            {'page': 1, 'excepted': 1},
            {'page': 2, 'excepted': 2},
        ]

        for i in arrange:
            params = SearchParams(page=i['page'])
            self.assertEqual(params.page, i['excepted'])

    def test_per_page_prop(self):
        params = SearchParams()
        self.assertEqual(params.per_page, 15)

        arrange = [
            {'per_page': None, 'expected': 15},
            {'per_page': "", 'expected': 15},
            {'per_page': "fake", 'expected': 15},
            {'per_page': 0, 'expected': 15},
            {'per_page': -1, 'expected': 15},
            {'per_page': "0", 'expected': 15},
            {'per_page': "-1", 'expected': 15},
            {'per_page': 5.5, 'expected': 5},
            {'per_page': True, 'expected': 1},
            {'per_page': False, 'expected': 15},
            {'per_page': {}, 'expected': 15},
            {'per_page': 1, 'expected': 1},
            {'per_page': 2, 'expected': 2},
        ]

        for i in arrange:
            params = SearchParams(per_page=i['per_page'])
            self.assertEqual(params.per_page, i['expected'])
