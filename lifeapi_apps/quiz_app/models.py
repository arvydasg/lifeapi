from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    TYPE_CHOICES = [
        ('YN', 'Yes/No'),
        ('Scale', 'Scale 1-5'),
        ('Text', 'Text'),
    ]

    description = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Text')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # change the way question object is displayed in django admin panel
    def __str__(self):
        return f"{self.description} - {self.type}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField(blank=False)
    date_added = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # change the way answer object is displayed in django admin panel
    def __str__(self):
        return f"{self.date_added} - {self.question} - {self.answer}"