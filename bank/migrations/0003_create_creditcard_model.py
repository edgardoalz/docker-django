# Generated by Django 5.0.4 on 2024-06-07 22:55

import uuid

import django.core.validators
import django.db.models.deletion
import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_create_account_and_account_move_models"),
        ("bank", "0002_create_bankaccount_model"),
        ("multitenant", "0001_create_tenant_model"),
    ]

    operations = [
        migrations.CreateModel(
            name="CreditCard",
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
                    "account_number",
                    models.CharField(max_length=4, verbose_name="Account number"),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                (
                    "owner_name",
                    models.CharField(max_length=255, verbose_name="Owner name"),
                ),
                (
                    "closing_day",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(28),
                        ],
                        verbose_name="Closing day",
                    ),
                ),
                (
                    "payment_due_day",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(28),
                        ],
                        verbose_name="Payment due day",
                    ),
                ),
                (
                    "credit_limit",
                    models.PositiveIntegerField(verbose_name="Credit limit"),
                ),
                (
                    "account",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="account.account",
                        verbose_name="Account",
                    ),
                ),
                (
                    "bank",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="bank.bank",
                        verbose_name="Bank",
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
                "abstract": False,
                "verbose_name": "Credit card",
                "verbose_name_plural": "Credit cards",
            },
            managers=[
                ("global_objects", django.db.models.manager.Manager()),
            ],
        ),
    ]
