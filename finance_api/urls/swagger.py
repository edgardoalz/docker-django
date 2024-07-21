import os
from pathlib import Path

from django.shortcuts import redirect
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

api_folder_path = Path(__file__).resolve().parent / "api"
versions = [
    file.replace(".py", "")
    for file in os.listdir(api_folder_path)
    if file.startswith("v")
]


def _build_swagger_urls(version="v1"):
    return [
        path(
            f"{version}/",
            SpectacularSwaggerView.as_view(url_name=f"{version}_schema"),
            name=f"{version}_swagger-ui",
        ),
        path(
            f"{version}/schema/",
            SpectacularAPIView.as_view(api_version=version),
            name=f"{version}_schema",
        ),
    ]


urlpatterns = []
for version in versions:
    urlpatterns += _build_swagger_urls(version)

urlpatterns.append(path("", lambda _: redirect("v1/")))
