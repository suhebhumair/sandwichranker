from django.db import models

# Create your models here.
from django.db import models

class Sandwich(models.Model):
    sandwich_id = models.CharField(max_length=255, unique=True)
    sandwich_name = models.CharField(default=0, max_length=255)
    average_rating = models.FloatField(default=0)
    percentage = models.FloatField(default=0)
    total_score = models.IntegerField(default=0)
    total_submissions = models.IntegerField(default=0)
    sandwich_image = models.CharField(default=0, max_length=255)
