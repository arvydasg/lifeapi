from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from lifeapi_apps.quiz_app.models import Answer, Question
from lifeapi_apps.weather_app.models import Weather
from django.utils import timezone
import random
import datetime


class Command(BaseCommand):
    help = 'Generate fake answers for each weather date and each question'

    def handle(self, *args, **kwargs):
        # Retrieve all weather dates
        weather_dates = Weather.objects.all()

        # Retrieve all questions
        questions = Question.objects.all()

        # Check if weather dates and questions exist
        if not weather_dates.exists() or not questions.exists():
            self.stdout.write(self.style.ERROR(
                'No weather data or questions available.'
            ))
            return

        # Retrieve or create the user 'root'
        root_user = User.objects.get(username='root')

        for weather_date in weather_dates:
            for question in questions:
                # Randomly choose 'YES' or 'NO' for the answer
                answer_text = random.choice(['YES', 'NO'])

                # Convert weather_date.date to a timezone-aware datetime
                naive_date_added = datetime.datetime.combine(
                    weather_date.date, datetime.datetime.min.time()
                )
                date_added = timezone.make_aware(naive_date_added)

                # Create an answer
                Answer.objects.create(
                    question=question,
                    answer=answer_text,
                    created_by=root_user,
                    date_added=date_added
                )

                self.stdout.write(self.style.SUCCESS(f'Successfully created answer "{answer_text}" for question {question.id} on {weather_date.date}'))
