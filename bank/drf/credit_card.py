from rest_framework import permissions, serializers

from account.drf.account import AccountSerializer
from account.models.account import Account
from multitenant.drf.fields import CurrentTenantDefault
from multitenant.drf.viewsets import TenantModelViewSet

from ..models import CreditCard
from ..models.bank import Bank
from .bank import BankSerializer


class CreditCardSerializer(serializers.ModelSerializer[CreditCard]):
    account = AccountSerializer()
    bank = BankSerializer()

    class Meta:
        model = CreditCard
        fields = [
            "uuid",
            "account_number",
            "name",
            "owner_name",
            "closing_day",
            "payment_due_day",
            "credit_limit",
            "bank",
            "account",
        ]
        read_only_fields = ["uuid", "account", "bank"]


class UpdateCreditCardSerializer(serializers.ModelSerializer[CreditCard]):
    bank = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Bank.objects.all(),
    )

    class Meta:
        model = CreditCard
        fields = [
            "account_number",
            "name",
            "owner_name",
            "closing_day",
            "payment_due_day",
            "credit_limit",
            "bank",
        ]

    def update(self, instance: CreditCard, validated_data) -> CreditCard:
        return super().update(instance, validated_data)

    def to_representation(self, instance: CreditCard) -> dict:
        return CreditCardSerializer(instance).data


class CreateCreditCardSerializer(serializers.ModelSerializer[CreditCard]):
    initial_balance = AccountSerializer().get_fields()["initial_balance"]
    bank = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Bank.objects.all(),
    )
    tenant = serializers.HiddenField(default=CurrentTenantDefault())

    class Meta:
        model = CreditCard
        fields = [
            "account_number",
            "name",
            "owner_name",
            "initial_balance",
            "closing_day",
            "payment_due_day",
            "credit_limit",
            "bank",
            "tenant",
        ]

    def create(self, validated_data) -> CreditCard:
        initial_balance = validated_data.pop("initial_balance")
        account = Account.objects.create(
            name=validated_data["name"],
            balance=initial_balance,
            tenant=validated_data["tenant"],
        )
        new_instance = CreditCard.objects.create(account=account, **validated_data)
        return new_instance

    def to_representation(self, instance: CreditCard) -> dict:
        return CreditCardSerializer(instance).data


class CreditCardViewSet(TenantModelViewSet[CreditCard]):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    lookup_field = "uuid"

    def get_queryset(self):
        return super().get_queryset().order_by("name")

    def get_serializer_class(self):
        if self.action == "create":
            return CreateCreditCardSerializer
        if self.action in ("update", "partial_update"):
            return UpdateCreditCardSerializer
        return CreditCardSerializer

    def perform_destroy(self, instance: CreditCard) -> None:
        instance.soft_delete()
