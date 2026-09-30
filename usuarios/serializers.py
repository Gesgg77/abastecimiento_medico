from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Usuario

class RegistroInstitucionSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Usuario
        fields = ("id", "username", "email", "password", "first_name", "last_name")

    def create(self, validated_data):
        return Usuario.objects.create_user(
            rol=Usuario.Rol.INSTITUCION,
            **validated_data,
        )

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ("id", "username", "email", "first_name", "last_name", "rol")
        read_only_fields = ("id", "rol")

class TokenConRolSerializer(TokenObtainPairSerializer):
    """Agrega el rol solicitado por la pauta dentro del payload JWT."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["rol"] = user.rol
        token["username"] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["rol"] = self.user.rol
        data["username"] = self.user.username
        return data
