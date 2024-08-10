from typing import ClassVar, Generic, Self, TypeVar

from django.db import models
from django.db.models.manager import BaseManager as DjangoBaseManager
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
    DjangoBaseManager[T].from_queryset(BaseQuerySet[T]),  # type: ignore[misc]
    Generic[T],
):
    pass


class BaseModel(
    UUIDModelMixin, CreatedUpdatedModelMixin, SoftDeleteModelMixin, models.Model
):
    global_objects: ClassVar[models.Manager[Self]] = models.Manager()  # type: ignore[assignment]
    objects: ClassVar[BaseManager[Self]] = BaseManager()

    class Meta(TypedModelMeta):
        abstract = True
