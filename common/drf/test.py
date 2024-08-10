from typing import ClassVar

from django.urls import reverse
from rest_framework.test import APITestCase


class CRUDAPITestCase(APITestCase):
    url_name: ClassVar[str]

    def list(self, version="v1"):
        url = self._list_url(version)
        return self.client.get(url)

    def detail(self, uuid: str, version="v1"):
        url = self._detail_url(uuid, version)
        return self.client.get(url)

    def create(self, data: dict, version="v1"):
        url = self._list_url(version)
        return self.client.post(url, data)

    def update(self, uuid: str, data: dict, version="v1"):
        url = self._detail_url(uuid, version)
        return self.client.put(url, data)

    def partial_update(self, uuid: str, data: dict, version="v1"):
        url = self._detail_url(uuid, version)
        return self.client.patch(url, data)

    def delete(self, uuid: str, version="v1"):
        url = self._detail_url(uuid, version)
        return self.client.delete(url)

    def _list_url(self, version="v1"):
        return reverse(f"{version}:{self.url_name}-list")

    def _detail_url(self, uuid: str, version="v1"):
        return reverse(f"{version}:{self.url_name}-detail", kwargs=dict(uuid=uuid))
