from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegistroInstitucionSerializer, TokenConRolSerializer

class RegistroInstitucionView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegistroInstitucionSerializer

class TokenConRolView(TokenObtainPairView):
    serializer_class = TokenConRolSerializer
