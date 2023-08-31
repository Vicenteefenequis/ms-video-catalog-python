

from collections import namedtuple
from datetime import datetime
from typing import Any
import unittest
from unittest import mock
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from core.category.infra.serializers import CategorySerializer
from core.category.application.dto import CategoryOutput
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    ListCategoriesUseCase,
    GetCategoryUseCase,
    UpdateCategoryUseCase
)
from core.category.infra.django_app.api import CategoryResource


class StubCategorySerializer:
    validated_data = Any

    def is_valid(self, raise_exception: bool):
        pass


class TestCategoryResourceUnit(unittest.TestCase):
    @mock.patch.object(CategorySerializer, '__new__')
    def test_category_to_response_method(self, mock_serializer):
        mock_serializer.return_value = namedtuple(
            'Faker', ['data']
        )(data='test')
        data = CategoryResource.category_to_response('output')  # type: ignore
        mock_serializer.assert_called_with(
            CategorySerializer, instance='output'
        )
        self.assertEqual(data, 'test')

    @mock.patch.object(CategoryResource, 'category_to_response')
    def test_post_method(self, mock_category_to_response):
        stub_serializer = StubCategorySerializer()
        send_data = {'name': 'Movie'}
        expected_response = {
            'id': '114e527b-d222-44f1-86c7-1cb621f44849',
            'name': 'Movie',
            'description': None,
            'is_active': True,
            'created_at': datetime.now()
        }
        with mock.patch.object(
            CategorySerializer,
            '__new__',
            return_value=stub_serializer
        ) as mock_serializer:
            stub_serializer.validated_data = send_data
            stub_serializer.is_valid = mock.MagicMock()
            mock_create_use_case = mock.Mock(CreateCategoryUseCase)
            mock_create_use_case.execute.return_value = CreateCategoryUseCase.Output(
                **expected_response)
            mock_category_to_response.return_value = expected_response
            resource = CategoryResource(**{
                **self.__init_all_none(),
                'create_use_case': lambda: mock_create_use_case
            })
            _request = APIRequestFactory().post('/', send_data)
            request = Request(_request)
            request._full_data = send_data  # pylint: disable=protected-access
            response = resource.post(request)
            stub_serializer.is_valid.assert_called_with(raise_exception=True)
            mock_create_use_case.execute.assert_called_with(CreateCategoryUseCase.Input(
                name='Movie'
            ))
            mock_category_to_response.assert_called_with(
                mock_create_use_case.execute.return_value
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data, {
                'id': '114e527b-d222-44f1-86c7-1cb621f44849',
                'name': 'Movie',
                'description': None,
                'is_active': True,
                'created_at': expected_response['created_at']
            })
        mock_serializer.assert_called_with(CategorySerializer, data=send_data)

    def test_get_method(self):
        mock_list_use_case = mock.Mock(ListCategoriesUseCase)

        mock_list_use_case.execute.return_value = ListCategoriesUseCase.Output(
            items=[
                CategoryOutput(
                    id='114e527b-d222-44f1-86c7-1cb621f44849',
                    name='Movie',
                    description=None,
                    is_active=True,
                    created_at=datetime.now()
                )
            ],
            total=1,
            current_page=1,
            per_page=2,
            last_page=1
        )

        resource = CategoryResource(**{
            **self.__init_all_none(),
            'list_use_case': lambda: mock_list_use_case
        })
        _request = APIRequestFactory().get(
            '/?page=1&per_page=1&sort=name&sort_dir=asc&filter=test'
        )
        request = Request(_request)
        response = resource.get(request)
        mock_list_use_case.execute.assert_called_with(ListCategoriesUseCase.Input(
            page="1",  # type: ignore
            per_page="1",  # type: ignore
            sort='name',
            sort_dir='asc',
            filter='test'
        ))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data, {
            'items': [
                {
                    'id': '114e527b-d222-44f1-86c7-1cb621f44849',
                    'name': 'Movie',
                    'description': None,
                    'is_active': True,
                    'created_at': mock_list_use_case.execute.return_value.items[0].created_at
                }
            ],
            'total': 1,
            'current_page': 1,
            'per_page': 2,
            'last_page': 1
        })

    def test_if_get_invoke_get_object_method(self):
        mock_get_use_case = mock.Mock(GetCategoryUseCase)
        mock_list_use_case = mock.Mock(ListCategoriesUseCase)

        mock_get_use_case.execute.return_value = GetCategoryUseCase.Output(
            id='114e527b-d222-44f1-86c7-1cb621f44849',
            name='Movie',
            description=None,
            is_active=True,
            created_at=datetime.now()
        )

        resource = CategoryResource(**{
            **self.__init_all_none(),
            'list_use_case': lambda: mock_list_use_case,
            'get_use_case': lambda: mock_get_use_case
        })

        response = resource.get(
            None, '114e527b-d222-44f1-86c7-1cb621f44849'  # type: ignore
        )
        mock_get_use_case.execute.assert_called_with(GetCategoryUseCase.Input(
            id='114e527b-d222-44f1-86c7-1cb621f44849'
        ))

        mock_list_use_case.execute.assert_not_called()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id': '114e527b-d222-44f1-86c7-1cb621f44849',
            'name': 'Movie',
            'description': None,
            'is_active': True,
            'created_at': mock_get_use_case.execute.return_value.created_at
        })

    def test_get_object_method(self):
        mock_get_use_case = mock.Mock(GetCategoryUseCase)

        mock_get_use_case.execute.return_value = GetCategoryUseCase.Output(
            id='114e527b-d222-44f1-86c7-1cb621f44849',
            name='Movie',
            description=None,
            is_active=True,
            created_at=datetime.now()
        )

        resource = CategoryResource(**{
            **self.__init_all_none(),
            'get_use_case': lambda: mock_get_use_case
        })

        response = resource.get_object('114e527b-d222-44f1-86c7-1cb621f44849')
        mock_get_use_case.execute.assert_called_with(GetCategoryUseCase.Input(
            id='114e527b-d222-44f1-86c7-1cb621f44849'
        ))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id': '114e527b-d222-44f1-86c7-1cb621f44849',
            'name': 'Movie',
            'description': None,
            'is_active': True,
            'created_at': mock_get_use_case.execute.return_value.created_at
        })

    def test_put_method(self):
        send_data = {
            'id': '114e527b-d222-44f1-86c7-1cb621f44849',
            'name': 'Movie 2',
            'description': 'some description'
        }
        mock_update_use_case = mock.Mock(UpdateCategoryUseCase)

        mock_update_use_case.execute.return_value = UpdateCategoryUseCase.Output(
            id=send_data['id'],
            name=send_data['name'],
            description=send_data['description'],
            is_active=True,
            created_at=datetime.now()
        )

        resource = CategoryResource(**{
            **self.__init_all_none(),
            'update_use_case': lambda: mock_update_use_case
        })
        _request = APIRequestFactory().put('/', send_data)
        request = Request(_request)
        request._full_data = send_data  # pylint: disable=protected-access
        response = resource.put(
            request,
            send_data['id']
        )
        mock_update_use_case.execute.assert_called_with(UpdateCategoryUseCase.Input(
            id=send_data['id'],
            name=send_data['name'],
            description=send_data['description']
        ))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id': send_data['id'],
            'name': send_data['name'],
            'description': send_data['description'],
            'is_active': True,
            'created_at': mock_update_use_case.execute.return_value.created_at
        })

    def test_delete_method(self):
        send_data = {
            'id': '114e527b-d222-44f1-86c7-1cb621f44849',
        }
        mock_delete_use_case = mock.Mock(DeleteCategoryUseCase)

        resource = CategoryResource(**{
            **self.__init_all_none(),
            'delete_use_case': lambda: mock_delete_use_case
        })
        _request = APIRequestFactory().delete('/', send_data)
        request = Request(_request)
        request._full_data = send_data  # pylint: disable=protected-access
        response = resource.delete(
            request,
            send_data['id']
        )
        response = resource.delete(request, send_data['id'])
        mock_delete_use_case.execute.assert_called_with(DeleteCategoryUseCase.Input(
            id=send_data['id']
        ))

        self.assertEqual(response.status_code, 204)

    def __init_all_none(self):
        return {
            'list_use_case': None,
            'create_use_case': None,
            'get_use_case': None,
            'update_use_case': None,
            'delete_use_case': None
        }
