from django.db import models

from .tenant import Tenant


class TenantUser(models.Model):
    is_owner = models.BooleanField(default=False)
    tenants = models.ManyToManyField(
        Tenant,
        blank=True,
        related_name="users",
        related_query_name="user",
    )

    class Meta:
        abstract = True
