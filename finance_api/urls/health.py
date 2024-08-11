# myapp/views.py

from django.http import JsonResponse
from django.urls import path

def healthcheck(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("", healthcheck)
]