from typing import Iterable

from django.db import models
from django_stubs_ext.db.models import TypedModelMeta


class CleanOnSaveMixin(models.Model):
    validation_exclusions: set[str] = set()

    def __init__(self, *args, **kwargs) -> None:
        self.__clean_on_save_cleaned = False
        super().__init__(*args, **kwargs)

    class Meta(TypedModelMeta):
        abstract = True

    def get_validation_exclusions(self) -> set[str]:
        return self.validation_exclusions

    def full_clean(self, exclude: Iterable[str] | None = None, *args, **kwargs) -> None:
        if self.__clean_on_save_cleaned:
            return
        try:
            if not exclude:
                kwargs["exclude"] = self.get_validation_exclusions()
            else:
                kwargs["exclude"] = self.get_validation_exclusions().union(exclude)
            super().full_clean(*args, **kwargs)
            self.__clean_on_save_cleaned = True
        except Exception as e:
            self.__clean_on_save_cleaned = True
            raise e

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.__clean_on_save_cleaned = False
