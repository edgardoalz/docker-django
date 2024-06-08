from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CreditConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "credit"
    verbose_name = _("Credit")
