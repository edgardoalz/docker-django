from typing import Any

from django.db import models
from django_stubs_ext.db.models import TypedModelMeta


class ModelChangedMixin(models.Model):
    fields_to_watch: tuple[str, ...] = ()

    class Meta(TypedModelMeta):
        abstract = True

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._set_original()

    def get_fields_to_watch(self) -> tuple[str, ...]:
        return self.fields_to_watch

    def _set_original(self) -> None:
        for field in self.get_fields_to_watch():
            setattr(self, "__original_%s" % field, getattr(self, field))

    def get_original(self, field: str) -> Any:
        return getattr(self, "__original_%s" % field)

    def has_changed(self, field: str) -> bool:
        if field not in self.get_fields_to_watch():
            return False
        original = self.get_original(field)
        current = getattr(self, field)
        return original != current

    def save(self, *args, **kargs) -> None:
        super().save(*args, **kargs)
        self._set_original()
