from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FinanceAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "finance_auth"
    verbose_name = _("Finance Auth")
