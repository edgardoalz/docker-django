from rest_framework.routers import DefaultRouter

from bank.drf.bank import BankViewSet
from bank.drf.bank_account import BankAccountViewSet
from bank.drf.credit_card import CreditCardViewSet

_router = DefaultRouter()
_router.register(r"bank", BankViewSet, basename="bank")
_router.register(r"bank-account", BankAccountViewSet, basename="bank_account")
_router.register(r"credit-card", CreditCardViewSet, basename="credit_card")

app_name = "v1"
urlpatterns = _router.urls
