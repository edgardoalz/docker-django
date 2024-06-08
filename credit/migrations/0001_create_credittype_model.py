# Generated by Django 5.0.4 on 2024-06-08 17:36

import uuid

import django.db.models.deletion
import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("multitenant", "0001_create_tenant_model"),
    ]

    operations = [
        migrations.CreateModel(
            name="CreditType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is active"),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Deletion date"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Created date"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Update date"),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, unique=True, verbose_name="UUID"
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                (
                    "tenant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="multitenant.tenant",
                        to_field="code",
                        verbose_name="Tenant",
                    ),
                ),
            ],
            options={
                "verbose_name": "Credit type",
                "verbose_name_plural": "Credit types",
                "unique_together": {("tenant", "name")},
            },
            managers=[
                ("global_objects", django.db.models.manager.Manager()),
            ],
        ),
    ]
