from typing import TypeVar, Generic, Optional, Sequence

from fastapi import Query
from fastapi_paginate import Params

from fastapi_paginate.bases import BasePage, AbstractParams
from pydantic import conint
from starlette.requests import Request

T = TypeVar("T")


class CustomParams(Params):
    size: int = Query(10, ge=1, le=1_000, description="Page size")


class CustomPage(BasePage[T], Generic[T]):
    current_page: conint(ge=1)
    total_pages: int
    size: conint(ge=1)
    total: Optional[int] = 0
    items: Sequence[T]

    __params_type__ = CustomParams

    @classmethod
    def create(cls, items: Sequence[T], total: int, params: AbstractParams, request: Request):
        if not isinstance(params, Params):
            raise ValueError("Page should be used with Params")

        total_pages = total // params.size if total % params.size == 0 else total // params.size + 1
        return cls(
            current_page=params.page,
            total_pages=total_pages,
            total=total,
            size=params.size,
            items=items,
        )

