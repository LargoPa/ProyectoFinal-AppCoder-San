
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Admin, Empleado
from django.db.models.signals import post_migrate


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if kwargs['app_config'].name == 'AppCoder':
        if not Group.objects.filter(name='admin').exists():
            group, created = Group.objects.get_or_create(name='admin')
            if created:
                print("Grupo 'admin' creado")
        if not Group.objects.filter(name='empleado').exists():
            group, created = Group.objects.get_or_create(name='empleado')
            if created:
                print("Grupo 'empleado' creado")

