from rest_framework import serializers

from ..models.account import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "uuid",
            "name",
            "balance",
            "initial_balance",
        ]
        read_only_fields = ["uuid"]
