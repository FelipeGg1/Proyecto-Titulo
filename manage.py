#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

# Cowboy
# # ---- COMANDOS ----#
# # ---- Crear Ambiente
# py -m venv NombreAmbiente
# # ------ Iniciar servidor
# py manage.py runserver 
# # ---- ---- Crear super Usuario
# python manage.py createsuperuser
# (estar dentro del Ambiente)
# # ---- ---- Crear archivo de migraciones
# python manage.py makemigrations core
# (Ojala dentro del ambiente)
# # ---- ---- Pasar Migraciones a Archivo SQL
# python manage.py migrate core
# (Ojala dentro del ambiente)