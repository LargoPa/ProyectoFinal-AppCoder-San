
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Crea grupos predeterminados'

    def handle(self, *args, **kwargs):
        # Lista de grupos predeterminados a crear
        grupos = ['admin', 'empleado']

        # Crear cada grupo si no existe
        for nombre_grupo in grupos:
            if not Group.objects.filter(name=nombre_grupo).exists():
                Group.objects.create(name=nombre_grupo)
                self.stdout.write(self.style.SUCCESS(f'Grupo "{nombre_grupo}" creado exitosamente.'))
            else:
                self.stdout.write(self.style.WARNING(f'Grupo "{nombre_grupo}" ya existe. No es necesario crearlo.'))


