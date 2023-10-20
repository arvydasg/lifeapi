from django.db import models

# Create your models here.


class Rescuetime(models.Model):
    date = models.DateField()
    productive_hours = models.DecimalField(max_digits=5, decimal_places=2)
    distracting_hours = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.productive_hours} - {self.distracting_hours}"
