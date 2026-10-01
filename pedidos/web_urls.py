from django.urls import path

from .views import pagina_solicitudes

urlpatterns = [
    path("solicitudes/", pagina_solicitudes, name="pagina-solicitudes"),
]
