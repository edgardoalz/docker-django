from django.db.models import TextChoices


class GlobalCreditType(TextChoices):
    provider = ("Proveedores", "Proveedores")
    bank_loan = ("Préstamos bancarios", "Préstamos bancarios")
    third_party_loan = ("Préstamos de terceros", "Préstamos de terceros")
    automotive = ("Automotríz", "Automotríz")
    mortgage = ("Hipotecario", "Hipotecario")
    customer = ("Clientes", "Clientes")
