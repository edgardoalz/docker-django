from rest_framework import serializers

from ..models.tenant import Tenant


class CurrentTenantDefault:
    requires_context = True

    def __call__(self, serializer_field: serializers.Field) -> Tenant:
        return serializer_field.context["tenant"]

    def __repr__(self):
        return "%s()" % self.__class__.__name__
