from typing import ClassVar, Generic, Self, TypeVar

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from common.models.base import BaseManager, BaseModel

from .tenant import Tenant

T = TypeVar("T", bound="TenantModel")


class PublicDataMutationError(ValidationError):
    def __init__(self):
        msg = gettext("Mutation of public objects is not allowed")
        super().__init__(msg)


class MissingTenantError(ValidationError):
    def __init__(self):
        msg = gettext("Tenant is required")
        super().__init__(msg)


class TenantManager(BaseManager[T], Generic[T]):
    public_filter = Q(tenant__isnull=True)

    def get_queryset(self):
        return super().get_queryset().filter(self.public_filter)

    def with_tenant(self, tenant_id: int, include_public=True):
        filter = Q(tenant__pk=tenant_id)
        if include_public:
            filter |= self.public_filter
        return super().get_queryset().filter(filter)


class TenantModel(BaseModel, models.Model):
    tenant_id: int | None
    tenant = models.ForeignKey(
        Tenant,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        to_field="code",
        verbose_name=_("Tenant"),
    )

    global_objects: ClassVar[models.Manager[Self]] = models.Manager()  # type: ignore[assignment]
    objects: ClassVar[BaseManager[Self]] = BaseManager()
    tenant_set: ClassVar[TenantManager[Self]] = TenantManager()

    contains_public_data = False

    class Meta:
        abstract = True

    @property
    def is_public(self):
        return not self.tenant_id

    def save(self, *args, **kargs) -> None:
        if self.pk:
            if self.__class__.contains_public_data:
                current_tenant_id = self.__class__.objects.get(pk=self.pk).tenant_id
                if not current_tenant_id:
                    raise PublicDataMutationError
        else:
            if not self.__class__.contains_public_data and not self.tenant_id:
                raise MissingTenantError
        super().save(*args, **kargs)
