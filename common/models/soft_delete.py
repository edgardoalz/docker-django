from typing import Generic, TypeVar

from django.db import models
from django.db.models.manager import BaseManager as DjangoBaseManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from .model_changed import ModelChangedMixin

T = TypeVar("T", bound=models.Model)


class SoftDeleteQuerySetMixin(models.QuerySet[T], Generic[T]):
    def soft_delete(self) -> int:
        return self.update(
            is_active=False,
            deleted_at=timezone.now(),
        )

    def restore(self) -> int:
        return self.update(
            is_active=True,
            deleted_at=None,
        )


class SoftDeleteManagerMixin(DjangoBaseManager[T], Generic[T]):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def deleted(self):
        return super().get_queryset().filter(is_active=False)


class SoftDeleteModelMixin(ModelChangedMixin, models.Model):
    is_active = models.BooleanField(_("Is active"), default=True)
    deleted_at = models.DateTimeField(_("Deletion date"), blank=True, null=True)

    def __init__(self, *args, **kwargs) -> None:
        self.__soft_delete_cleaned = False
        super().__init__(*args, **kwargs)

    class Meta(TypedModelMeta):
        abstract = True

    def get_fields_to_watch(self) -> tuple[str, ...]:
        return super().get_fields_to_watch() + ("is_active",)

    def soft_delete(self) -> None:
        self.is_active = False
        self.deleted_at = timezone.now()
        self.__soft_delete_cleaned = True
        self.save()

    def restore(self) -> None:
        self.is_active = True
        self.deleted_at = None
        self.__soft_delete_cleaned = True
        self.save()

    def _clean_soft_delete_values(self) -> None:
        """
        Derive deleted_at from is_active
        """
        if not self.__soft_delete_cleaned and self.has_changed("is_active"):
            self.deleted_at = None if self.is_active else timezone.now()

    def save(self, *args, **kargs) -> None:
        self._clean_soft_delete_values()
        super().save(*args, **kargs)
        self.__soft_delete_cleaned = False
