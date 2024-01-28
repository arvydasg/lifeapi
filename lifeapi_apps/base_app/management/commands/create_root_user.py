from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create a Django superuser with username "root" and password "kk"'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username='root').exists():
            User.objects.create_superuser('root', 'admin@example.com', 'kk')
            self.stdout.write(self.style.SUCCESS('Superuser "root" created successfully.'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser "root" already exists.'))
