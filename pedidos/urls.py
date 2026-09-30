from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CambiarEstadoSolicitudView,
    ConfirmarSolicitudView,
    ItemCarroViewSet,
    MisSolicitudesView,
    SolicitudesGestorView,
)

router = DefaultRouter()
router.register("carro-insumos", ItemCarroViewSet, basename="carro-insumos")

urlpatterns = [
    path("", include(router.urls)),
    path("solicitudes/confirmar/", ConfirmarSolicitudView.as_view(), name="confirmar-solicitud"),
    path("mis-solicitudes/", MisSolicitudesView.as_view(), name="mis-solicitudes"),
    path("solicitudes/", SolicitudesGestorView.as_view(), name="solicitudes-gestor"),
    path(
        "solicitudes/<int:pk>/estado/",
        CambiarEstadoSolicitudView.as_view(),
        name="cambiar-estado-solicitud",
    ),
]
