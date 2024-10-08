# Generated by Django 5.0.4 on 2024-06-01 18:28

import uuid

import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tenant",
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
                (
                    "code",
                    models.CharField(max_length=255, unique=True, verbose_name="Code"),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
            ],
            options={
                "verbose_name": "Tenant",
                "verbose_name_plural": "Tenants",
            },
            managers=[
                ("global_objects", django.db.models.manager.Manager()),
            ],
        ),
    ]
