import uuid

from django.db import models
from django_stubs_ext.db.models import TypedModelMeta


class UUIDModelMixin(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    class Meta(TypedModelMeta):
        abstract = True
