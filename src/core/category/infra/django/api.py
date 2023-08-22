
from dataclasses import asdict, dataclass
from typing import Callable
from rest_framework import status
from rest_framework.request import Request

from rest_framework.response import Response
from rest_framework.views import APIView
from core.category.application.use_cases import CreateCategoryUseCase, ListCategoriesUseCase


@dataclass(slots=True)
class CategoryResource(APIView):
    create_use_case: Callable[[],  CreateCategoryUseCase]
    list_use_case: Callable[[], ListCategoriesUseCase]

    def post(self, request: Request):
        input_param = CreateCategoryUseCase.Input(
            **request.data  # type: ignore
        )
        output = self.create_use_case().execute(input_param)
        return Response(asdict(output), status=status.HTTP_201_CREATED)

    def get(self, request: Request):
        input_param = ListCategoriesUseCase.Input(
            **request.query_params.dict()  # type: ignore
        )

        output = self.list_use_case().execute(input_param)
        return Response(asdict(output))
