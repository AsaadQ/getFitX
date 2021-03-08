from django.db import models


# Create your models here.

class Days(models.Model):
    day_name = models.CharField(max_length=60)

    def __str__(self):
        return self.day_name


class Muscel(models.Model):
    Muscel_name = models.CharField(max_length=60)

    def __str__(self):
        return self.Muscel_name


class Exercise(models.Model):
    exercise_name = models.CharField(max_length=70)

    def __str__(self):
        return self.exercise_name


class Basic(models.Model):
    dagen_basic = models.ForeignKey(Days, related_name='days_basic', on_delete=models.CASCADE)
    muskel = models.ForeignKey(Muscel, related_name='muskel_basic', on_delete=models.CASCADE)
    exercise_name = models.ForeignKey(Exercise, related_name='exercise_name_basic', on_delete=models.CASCADE)
    reps = models.CharField(max_length=20)
    sets = models.IntegerField()


class Hard(models.Model):
    dagen_hard = models.ForeignKey(Days, related_name='days_hard', on_delete=models.CASCADE)
    muskel = models.ForeignKey(Muscel, related_name='muskel_hard', on_delete=models.CASCADE)
    exercise_name = models.ForeignKey(Exercise, related_name='exercise_name_hard', on_delete=models.CASCADE)
    reps = models.CharField(max_length=20)
    sets = models.IntegerField()


class Ultra(models.Model):
    dagen_ultra = models.ForeignKey(Days, related_name='days_ultra', on_delete=models.CASCADE)
    muskel = models.ForeignKey(Muscel, related_name='muskel_ultra', on_delete=models.CASCADE)
    exercise_name = models.ForeignKey(Exercise, related_name='exercise_name_ultra', on_delete=models.CASCADE)
    reps = models.CharField(max_length=20)
    sets = models.IntegerField()
