from rest_framework import permissions, serializers

from account.drf.account import AccountSerializer
from account.models.account import Account
from multitenant.drf.fields import CurrentTenantDefault
from multitenant.drf.viewsets import TenantModelViewSet

from ..models import BankAccount
from ..models.bank import Bank
from .bank import BankSerializer


class BankAccountSerializer(serializers.ModelSerializer[BankAccount]):
    account = AccountSerializer()
    bank = BankSerializer()

    class Meta:
        model = BankAccount
        fields = [
            "uuid",
            "account_number",
            "name",
            "owner_name",
            "type",
            "bank",
            "account",
        ]
        read_only_fields = ["uuid", "account", "bank"]


class UpdateBankAccountSerializer(serializers.ModelSerializer[BankAccount]):
    bank = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Bank.objects.all(),
    )

    class Meta:
        model = BankAccount
        fields = [
            "account_number",
            "name",
            "owner_name",
            "type",
            "bank",
        ]

    def to_representation(self, instance: BankAccount) -> dict:
        return BankAccountSerializer(instance).data


class CreateBankAccountSerializer(serializers.ModelSerializer[BankAccount]):
    initial_balance = AccountSerializer().get_fields()["initial_balance"]
    bank = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Bank.objects.all(),
    )
    tenant = serializers.HiddenField(default=CurrentTenantDefault())

    class Meta:
        model = BankAccount
        fields = [
            "account_number",
            "name",
            "owner_name",
            "type",
            "initial_balance",
            "bank",
            "tenant",
        ]

    def create(self, validated_data) -> BankAccount:
        initial_balance = validated_data.pop("initial_balance")
        account = Account.objects.create(
            name=validated_data["name"],
            balance=initial_balance,
            tenant=validated_data["tenant"],
        )
        new_instance = BankAccount.objects.create(account=account, **validated_data)
        return new_instance

    def to_representation(self, instance: BankAccount) -> dict:
        return BankAccountSerializer(instance).data


class BankAccountViewSet(TenantModelViewSet[BankAccount]):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    lookup_field = "uuid"

    def get_queryset(self):
        return super().get_queryset().order_by("name")

    def get_serializer_class(self):
        if self.action == "create":
            return CreateBankAccountSerializer
        if self.action in ("update", "partial_update"):
            return UpdateBankAccountSerializer
        return BankAccountSerializer

    def perform_destroy(self, instance: BankAccount) -> None:
        instance.soft_delete()
