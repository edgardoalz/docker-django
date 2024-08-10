from django.db import models
from django.utils.translation import gettext_lazy as _


class CompanyTypeCodes(models.TextChoices):
    customer = ("customer", _("Customer"))
    supplier = ("supplier", _("Supplier"))
    creditor = ("creditor", _("Creditor"))
    employee = ("employee", _("Employee"))
    debtor = ("debtor", _("Debtor"))
