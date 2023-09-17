from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    sequence = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.description}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField(blank=False)
    date_added = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.date_added} - {self.question} - {self.answer}"