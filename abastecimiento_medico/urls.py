from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import inicio

urlpatterns = [
    path("", inicio, name="inicio"),
    path("catalogo/", include("catalogo.web_urls")),
    path("api/", include("catalogo.urls")),
    path("api/", include("usuarios.urls")),
    path("api/", include("pedidos.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
