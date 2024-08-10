from rest_framework import permissions, serializers, viewsets

from ..models import Bank


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ["uuid", "name"]
        read_only_fields = ["uuid"]


class BankViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

    lookup_field = "uuid"
    permission_classes = [permissions.IsAuthenticated]
