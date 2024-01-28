from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker


class Command(BaseCommand):
    help = 'Create fake users'

    def handle(self, *args, **kwargs):
        fake = Faker()
        for _ in range(5):  # Adjust the number as needed
            username = fake.user_name()
            email = fake.email()
            password = fake.password()
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created user {username}'))
