from django.db import models

# Create your models here.

class Weather(models.Model):
    date = models.DateField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)