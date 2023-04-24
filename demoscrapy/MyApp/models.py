from django.db import models

# Create your models here.

class PetrolPrice(models.Model):
    date = models.DateField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.date}: {self.price}"
