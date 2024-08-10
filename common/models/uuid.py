import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta


class UUIDModelMixin(models.Model):
    uuid = models.UUIDField(_("UUID"), default=uuid.uuid4, unique=True)

    class Meta(TypedModelMeta):
        abstract = True
