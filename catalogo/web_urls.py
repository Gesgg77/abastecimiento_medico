from django.urls import path

from .views import pagina_categorias, pagina_insumos

urlpatterns = [
    path("insumos/", pagina_insumos, name="pagina-insumos"),
    path("categorias/", pagina_categorias, name="pagina-categorias"),
]
