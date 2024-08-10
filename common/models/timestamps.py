from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta


class CreatedUpdatedModelMixin(models.Model):
    created_at = models.DateTimeField(_("Created date"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Update date"), auto_now=True)

    class Meta(TypedModelMeta):
        abstract = True
