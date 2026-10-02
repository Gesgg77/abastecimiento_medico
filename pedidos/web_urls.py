from django.urls import path

from .views import pagina_carro, pagina_solicitudes

urlpatterns = [
    path("carro/", pagina_carro, name="pagina-carro"),
    path("solicitudes/", pagina_solicitudes, name="pagina-solicitudes"),
]
