from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from common.models.base import BaseModel


class Bank(BaseModel, models.Model):
    code = models.CharField(
        _("Code"),
        max_length=255,
        unique=True,
    )
    name = models.CharField(_("Name"), max_length=255)

    validation_exclusions = {"name"}

    class Meta(TypedModelMeta):
        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")

    def __str__(self) -> str:
        return self.name
