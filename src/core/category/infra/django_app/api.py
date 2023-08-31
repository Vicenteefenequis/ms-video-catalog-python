
from dataclasses import asdict, dataclass
from typing import Callable, Optional

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


from core.__seedwork.infra.serializers import UUIDSerializer
from core.category.application.dto import CategoryOutput
from core.category.infra.serializers import CategorySerializer
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    GetCategoryUseCase,
    ListCategoriesUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase
)


@dataclass(slots=True)
class CategoryResource(APIView):
    create_use_case: Callable[[],  CreateCategoryUseCase]
    list_use_case: Callable[[], ListCategoriesUseCase]
    get_use_case: Callable[[], GetCategoryUseCase]
    update_use_case: Callable[[], UpdateCategoryUseCase]
    delete_use_case: Callable[[], DeleteCategoryUseCase]

    def post(self, request: Request):
        serializer = CategorySerializer(data=request.data)  # type: ignore
        serializer.is_valid(raise_exception=True)

        input_param = CreateCategoryUseCase.Input(
            **serializer.validated_data)  # type: ignore
        output = self.create_use_case().execute(input_param)
        body = CategoryResource.category_to_response(output)
        return Response(body, status=status.HTTP_201_CREATED)

    def get(self, request: Request, id: Optional[str] = None):  # pylint: disable=redefined-builtin, invalid-name

        if id:
            return self.get_object(id)

        input_param = ListCategoriesUseCase.Input(
            **request.query_params.dict()  # type: ignore
        )

        output = self.list_use_case().execute(input_param)
        return Response(asdict(output))

    def get_object(self, id: str):   # pylint: disable=redefined-builtin, invalid-name
        CategoryResource.validate_id(id)
        input_param = GetCategoryUseCase.Input(id)
        output = self.get_use_case().execute(input_param)
        body = CategoryResource.category_to_response(output)
        return Response(body)

    def put(self, request: Request, id: str):  # pylint: disable=redefined-builtin, invalid-name
        CategoryResource.validate_id(id)
        serializer = CategorySerializer(data=request.data)  # type: ignore
        serializer.is_valid(raise_exception=True)

        input_param = UpdateCategoryUseCase.Input(
            **{'id': id, **serializer.validated_data}  # type: ignore
        )
        output = self.update_use_case().execute(input_param)
        body = CategoryResource.category_to_response(output)
        return Response(body)

    def delete(self, _request: Request, id: str):  # pylint: disable=redefined-builtin, invalid-name
        CategoryResource.validate_id(id)
        input_param = DeleteCategoryUseCase.Input(id=id)
        self.delete_use_case().execute(input_param)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def category_to_response(output: CategoryOutput):
        serializer = CategorySerializer(instance=output)
        return serializer.data

    @staticmethod
    def validate_id(id: str):  # pylint: disable=invalid-name,redefined-builtin
        serializer = UUIDSerializer(data={'id': id})  # type: ignore
        serializer.is_valid(raise_exception=True)
