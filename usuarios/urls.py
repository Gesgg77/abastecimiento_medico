from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegistroInstitucionView, TokenConRolView

urlpatterns = [
    path("auth/registro/", RegistroInstitucionView.as_view(), name="registro"),
    path("auth/token/", TokenConRolView.as_view(), name="token"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
