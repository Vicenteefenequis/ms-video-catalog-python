

from datetime import datetime
import unittest
from unittest import mock
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from core.category.application.dto import CategoryOutput
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    ListCategoriesUseCase,
    GetCategoryUseCase
)
from core.category.infra.django.api import CategoryResource


class TestCategoryResourceUnit(unittest.TestCase):

    def test_post_method(self):
        send_data = {'name': 'Movie'}
        mock_create_use_case = mock.Mock(CreateCategoryUseCase)

        mock_create_use_case.execute.return_value = CreateCategoryUseCase.Output(
            id='114e527b-d222-44f1-86c7-1cb621f44849',
            name='Movie',
            description=None,
            is_active=True,
            created_at=datetime.now()
        )

        resource = CategoryResource(**{
            **self.__init_all_none(),
            'create_use_case': lambda: mock_create_use_case
        })
        _request = APIRequestFactory().post('/', send_data)
        request = Request(_request)
        request._full_data = send_data  # pylint: disable=protected-access
        response = resource.post(request)
        mock_create_use_case.execute.assert_called_with(CreateCategoryUseCase.Input(
            name='Movie'
        ))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {
            'id': '114e527b-d222-44f1-86c7-1cb621f44849',
            'name': 'Movie',
            'description': None,
            'is_active': True,
            'created_at': mock_create_use_case.execute.return_value.created_at
        })

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

    def __init_all_none(self):
        return {
            'list_use_case': None,
            'create_use_case': None,
            'get_use_case': None
        }
