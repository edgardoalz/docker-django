from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class BankAccountType(TextChoices):
    checking_account = ("checking_account", _("Checking account"))
    savings_account = ("saving_account", _("Savings account"))
    investment_account = ("investment_account", _("Investment account"))
