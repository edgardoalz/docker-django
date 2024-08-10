from django.db import models

from common.models.base import BaseModel


class SatPaymentMethod(BaseModel, models.Model):
    code = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name}[{self.code}]"
