from django.db import models
from decimal import * # for decimal number purposes
from django.contrib.auth.models import User
import re # regex for email validation


# Create your models here.


class Workout(models.Model):
    """Creates instances of `Workout`."""

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Exercise(models.Model):
    """Creates instances of `Exercise`."""

    name = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=999, decimal_places=1)
    repetitions = models.DecimalField(max_digits=999, decimal_places=1)
    category = models.CharField(max_length=50, default="Strength Training") # Add more categories in the future: ['Strength Training', 'Endurance Training', 'Balance', 'Flexibility']
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
