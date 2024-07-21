from rest_framework.routers import DefaultRouter

from bank.drf.bank import BankViewSet

_router = DefaultRouter()
_router.register(r"bank", BankViewSet, basename="bank")

app_name = "v1"
urlpatterns = _router.urls
