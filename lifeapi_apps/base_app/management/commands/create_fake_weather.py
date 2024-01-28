from django.core.management.base import BaseCommand
from lifeapi_apps.weather_app.models import Weather
from faker import Faker
import datetime


class Command(BaseCommand):
    help = 'Generate fake weather data'

    def add_arguments(self, parser):
        parser.add_argument(
            'n',
            type=int,
            help='The number of fake weather data to create'
        )

    def handle(self, *args, **kwargs):
        n = kwargs['n']
        fake = Faker()

        # Get today's date
        today = datetime.date.today()

        for i in range(n):
            # Generate a date that is 'i' days before today
            date = today - datetime.timedelta(days=i)
            temperature = fake.pydecimal(
                left_digits=2,
                right_digits=2,
                positive=True
            )
            Weather.objects.create(date=date, temperature=temperature)

            self.stdout.write(self.style.SUCCESS(f'Successfully created weather data for {date}'))
