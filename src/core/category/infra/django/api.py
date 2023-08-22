
from dataclasses import asdict, dataclass
from typing import Callable, Optional
from rest_framework import status
from rest_framework.request import Request

from rest_framework.response import Response
from rest_framework.views import APIView
from core.category.application.use_cases import CreateCategoryUseCase, GetCategoryUseCase, ListCategoriesUseCase


@dataclass(slots=True)
class CategoryResource(APIView):
    create_use_case: Callable[[],  CreateCategoryUseCase]
    list_use_case: Callable[[], ListCategoriesUseCase]
    get_use_case: Callable[[], GetCategoryUseCase]

    def post(self, request: Request):
        input_param = CreateCategoryUseCase.Input(
            **request.data  # type: ignore
        )
        output = self.create_use_case().execute(input_param)
        return Response(asdict(output), status=status.HTTP_201_CREATED)

    def get(self, request: Request, id: Optional[str] = None):  # pylint: disable=redefined-builtin, invalid-name

        if id:
            return self.get_object(id)

        input_param = ListCategoriesUseCase.Input(
            **request.query_params.dict()  # type: ignore
        )

        output = self.list_use_case().execute(input_param)
        return Response(asdict(output))

    def get_object(self, id: str):   # pylint: disable=redefined-builtin, invalid-name
        input_param = GetCategoryUseCase.Input(id)
        output = self.get_use_case().execute(input_param)
        return Response(asdict(output))
