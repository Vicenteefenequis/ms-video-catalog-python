import pytest

from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from django_app import container

from core.category.tests.helpers import init_category_resource_all_none
from core.category.tests.fixture.categories_api_fixtures import CategoryApiFixture, HttpExpect
from core.category.domain.repositories import CategoryRepository
from core.category.infra.django_app.api import CategoryResource


@pytest.mark.django_db
class TestCategoryResourcePostMethodInt:

    resource: CategoryResource
    repo: CategoryRepository

    @classmethod
    def setup_class(cls):
        cls.repo = container.repository_category_django_orm()
        cls.resource = CategoryResource(**{
            **init_category_resource_all_none(),
            'create_use_case': container.use_case_category_create_category,
        })

    @pytest.mark.parametrize('http_expect', CategoryApiFixture.arrange_for_save())
    def test_post_method(self, http_expect: HttpExpect):
        request_factory = APIRequestFactory()
        _request = request_factory.get('/categories')
        request = Request(_request)
        request._full_data = http_expect.request.body  # pylint: disable=protected-access
        response = self.resource.post(request)
        assert response.status_code == 201
        assert CategoryApiFixture.keys_in_category_response() == list(
            response.data.keys()  # type: ignore
        )

        category = self.repo.find_by_id(response.data['id'])  # type: ignore
        serialized = CategoryResource.category_to_response(
            category)  # type: ignore
        assert response.data == serialized

        expected_data = {
            **http_expect.request.body,
            **http_expect.response.body
        }

        for key, value in expected_data.items():
            assert response.data[key] == value  # type: ignore
