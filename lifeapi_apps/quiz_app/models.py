from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    description = models.TextField()

    # change the way question object is displayed in django admin panel
    def __str__(self):
        return self.description

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255, blank=False)
    date_added = models.DateTimeField(default=timezone.now)

    # change the way answer object is displayed in django admin panel
    def __str__(self):
        return f"{self.date_added} - {self.question} - {self.answer}"