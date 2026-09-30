from django.core.management.base import BaseCommand, CommandError

from usuarios.models import Usuario


class Command(BaseCommand):
    help = "Crea un Gestor de Bodega sin utilizar Django Admin."

    def add_arguments(self, parser):
        parser.add_argument("username")
        parser.add_argument("email")
        parser.add_argument("password")

    def handle(self, *args, **options):
        username = options["username"]

        if Usuario.objects.filter(username=username).exists():
            raise CommandError("Ese nombre de usuario ya existe.")

        Usuario.objects.create_user(
            username=username,
            email=options["email"],
            password=options["password"],
            rol=Usuario.Rol.GESTOR,
        )
        self.stdout.write(self.style.SUCCESS(f"Gestor '{username}' creado correctamente."))
