from django.db import models

# Create your models here.

class Weather(models.Model):
    date = models.DateField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)

    # change the way weather object is displayed in django admin panel
    def __str__(self):
        return f"{self.date} - {self.temperature}"