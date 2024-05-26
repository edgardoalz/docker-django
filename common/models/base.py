from typing import ClassVar, Generic, Self, TypeVar

from django.db import models
from django_stubs_ext.db.models import TypedModelMeta

from .soft_delete import (
    SoftDeleteManagerMixin,
    SoftDeleteModelMixin,
    SoftDeleteQuerySetMixin,
)
from .timestamps import CreatedUpdatedModelMixin
from .uuid import UUIDModelMixin

T = TypeVar("T", bound="BaseModel")


class BaseQuerySet(SoftDeleteQuerySetMixin[T], models.QuerySet[T], Generic[T]):
    pass


class BaseManager(
    SoftDeleteManagerMixin[T],
    models.Manager[T],
    Generic[T],
):
    pass


class BaseModel(
    UUIDModelMixin, CreatedUpdatedModelMixin, SoftDeleteModelMixin, models.Model
):
    global_objects: ClassVar[models.Manager[Self]] = models.Manager()  # type: ignore
    objects: ClassVar[BaseManager[Self]] = BaseManager.from_queryset(BaseQuerySet)()  # type: ignore

    class Meta(TypedModelMeta):
        abstract = True
