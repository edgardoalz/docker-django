from django.db import models
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from common.models.base import BaseModel
from common.models.clean_on_save import CleanOnSaveMixin

from ..constants import CompanyTypeCodes


class CompanyType(BaseModel, CleanOnSaveMixin, models.Model):
    code = models.CharField(
        _("Code"),
        max_length=255,
        choices=CompanyTypeCodes.choices,
        unique=True,
    )
    name = models.CharField(_("Name"), max_length=255)

    validation_exclusions = {"name"}

    class Meta(TypedModelMeta):
        verbose_name = _("Company type")
        verbose_name_plural = _("Company types")

    def full_clean(self, *args, **kwargs) -> None:
        super().full_clean(*args, **kwargs)

        self.name = CompanyTypeCodes(self.code).label

    def __str__(self) -> str:
        return gettext(self.name)
