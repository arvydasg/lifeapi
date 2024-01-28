from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from lifeapi_apps.rescuetime_app.models import Rescuetime
from lifeapi_apps.weather_app.models import Weather
from faker import Faker


class Command(BaseCommand):
    help = 'Generate fake Rescuetime data for each weather day'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Retrieve all weather dates
        weather_dates = Weather.objects.all()

        # Retrieve the 'root' user
        user = User.objects.filter(username='root').first()

        if not weather_dates.exists() or not user:
            self.stdout.write(self.style.ERROR(
                'No weather data or user "root" available.'
            ))
            return

        for weather_date in weather_dates:
            # Generate fake Rescuetime data
            date = weather_date.date
            productive_hours = fake.pydecimal(
                left_digits=3,
                right_digits=2,
                positive=True
            )
            distracting_hours = fake.pydecimal(
                left_digits=3,
                right_digits=2,
                positive=True
            )

            # Create Rescuetime entry
            Rescuetime.objects.create(
                date=date,
                productive_hours=productive_hours,
                distracting_hours=distracting_hours,
                user=user
            )

            self.stdout.write(self.style.SUCCESS(f'Successfully created Rescuetime data for {date}'))
