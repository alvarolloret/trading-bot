from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(max_length=254,unique=True)
    def __str__(self):
        return self.date


class CandleStick(models.Model):
    date = models.IntegerField(default=170)
    high = models.FloatField(default=0)
    low = models.FloatField(default=0)
    open = models.FloatField(default=0)
    close = models.FloatField(default=0)

    def __str__(self):
        return self.date
