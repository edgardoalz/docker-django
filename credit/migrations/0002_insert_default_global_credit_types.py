# Generated by Django 5.0.4 on 2024-06-08 17:46

from django.db import migrations

default_credit_types = (
    "Proveedores",
    "Préstamos bancarios",
    "Préstamos de terceros",
    "Automotríz",
    "Hipotecario",
    "Clientes",
)


def insert_default_credit_types(apps, schema_editor):
    CreditType = apps.get_model("credit", "CreditType")
    CreditType.global_objects.bulk_create(
        [CreditType(name=credit_type) for credit_type in default_credit_types]
    )


def delete_default_credit_types(apps, schema_editor):
    CreditType = apps.get_model("credit", "CreditType")
    CreditType.global_objects.filter(name__in=default_credit_types).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("credit", "0001_create_credittype_model"),
    ]

    operations = [
        migrations.RunPython(insert_default_credit_types, delete_default_credit_types),
    ]
