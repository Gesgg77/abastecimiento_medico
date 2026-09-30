from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoriaViewSet, InsumoViewSet

router = DefaultRouter()
router.register("categorias", CategoriaViewSet, basename="categoria")
router.register("insumos", InsumoViewSet, basename="insumo")

urlpatterns = [path("", include(router.urls))]
