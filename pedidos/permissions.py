from rest_framework.permissions import BasePermission


class EsInstitucion(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.rol == "INSTITUCION"
        )


class EsGestor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.rol == "GESTOR"
        )
