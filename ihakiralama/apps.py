from django.apps import AppConfig
from django.db import connection

class IhaKiralamaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ihakiralama'

    def ready(self):
        # Uygulama başlatıldığında veritabanı göçlerini uygula
        if connection.vendor == 'postgresql':  # Sadece PostgreSQL için çalıştır
            from django.core.management import call_command
            call_command('makemigrations', interactive=False)
            call_command('migrate', interactive=False)