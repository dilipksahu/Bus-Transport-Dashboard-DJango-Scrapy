from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=300, blank=True)
    code = models.CharField(max_length=100, blank=True)

    
