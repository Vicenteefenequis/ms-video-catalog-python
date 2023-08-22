

from datetime import datetime
import unittest
from unittest import mock
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request

from core.category.application.use_cases import (
    CreateCategoryUseCase
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

        resource = CategoryResource(
            list_use_case=None,  # type: ignore
            create_use_case=lambda: mock_create_use_case
        )
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
