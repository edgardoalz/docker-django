# Generated by Django 5.0.4 on 2024-06-02 19:36

import uuid
from decimal import Decimal

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
            name="Account",
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
                ("name", models.CharField(max_length=255)),
                (
                    "initial_balance",
                    models.DecimalField(
                        blank=True,
                        decimal_places=4,
                        max_digits=19,
                    ),
                ),
                ("balance", models.DecimalField(decimal_places=4, max_digits=19)),
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
                "verbose_name": "Account",
                "verbose_name_plural": "Accounts",
            },
            managers=[
                ("global_objects", django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name="AccountMove",
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
                ("date", models.DateField(verbose_name="Date")),
                (
                    "type",
                    models.CharField(
                        choices=[("income", "Income"), ("outcome", "Outcome")],
                        max_length=10,
                        verbose_name="Type",
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="Notes")),
                (
                    "initial_balance",
                    models.DecimalField(
                        decimal_places=4, max_digits=19, verbose_name="Initial balance"
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=4, max_digits=19, verbose_name="Amount"
                    ),
                ),
                (
                    "balance",
                    models.DecimalField(
                        decimal_places=4, max_digits=19, verbose_name="Balance"
                    ),
                ),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="moves",
                        to="account.account",
                        verbose_name="Account",
                    ),
                ),
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
                "verbose_name": "Account move",
                "verbose_name_plural": "Account moves",
            },
            managers=[
                ("global_objects", django.db.models.manager.Manager()),
            ],
        ),
    ]
