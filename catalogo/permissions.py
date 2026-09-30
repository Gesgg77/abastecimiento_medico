from rest_framework.permissions import BasePermission, SAFE_METHODS

class EsGestorOSoloLectura(BasePermission):
    """Catálogo público para lectura; escritura solo para Gestor."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.rol == "GESTOR"
