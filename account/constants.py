from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class AccountMoveType(TextChoices):
    income = ("income", _("Income"))
    outcome = ("outcome", _("Outcome"))
