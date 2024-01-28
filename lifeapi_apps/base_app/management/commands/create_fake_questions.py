from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from lifeapi_apps.quiz_app.models import Question
from faker import Faker


class Command(BaseCommand):
    help = 'Generate fake questions'

    def add_arguments(self, parser):
        parser.add_argument(
            'n',
            type=int,
            help='The number of fake questions to create'
        )

    def handle(self, *args, **kwargs):
        n = kwargs['n']
        fake = Faker()

        def generate_seven_letter_word():
            word = fake.word()
            while len(word) != 7:
                word = fake.word()
            return word

        for _ in range(n):
            description = generate_seven_letter_word()
            created_by = User.objects.filter(username='root').first()
            Question.objects.create(description=description, created_by=created_by)

            self.stdout.write(self.style.SUCCESS(f'Successfully created question with description "{description}"'))
