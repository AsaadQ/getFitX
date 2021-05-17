from django.db import models
from decimal import *
from django.contrib.auth.models import User
import re


# Create your models here.

class WorkoutManager(models.Manager):

    def new(self, **kwargs):
        """
        Registrere Og Validere Ny Trenings Økt
        """

        errors = []

        # Hvis Navn er Mindre enn to bokstaver
        if len(kwargs["name"]) < 2:
            errors.append('Navn er Obligatorisk og må innholde mer enn to Bokstaver')

        # Ser Om Navnet Innholder Bokstaver eller Tall.

        WORKOUT_REGEX = re.compile(
            r'^\s*[A-Za-z0-9!@#$%^&*\"\':;\/?,<.>()-_=+\]\[~`]+(?:\s+[A-Za-z0-9!@#$%^&*\"\':;\/?,<.>()-_=+\]\[~`]+)*\s*$')

        if not WORKOUT_REGEX.match(kwargs["name"]):
            errors.append('Navn Må Innholde Bokstaver eller Tall.')

        # Notater
        if len(kwargs["description"]) < 2:
            errors.append('Notater må innholde mer enn to bokstaver')

        if not WORKOUT_REGEX.match(kwargs["description"]):
            errors.append('Notater Må Innholde Bokstaver eller Tall.')

        # Sjekk for Evt Feil
        if len(errors) == 0:
            # Create new validated workout:
            validated_workout = {
                "workout": Workout(name=kwargs["name"], description=kwargs["description"], user=kwargs["user"]),
            }
            # lagre ny Workout
            validated_workout["workout"].save()
            return validated_workout
        else:
            # Om Evt Feil
            for error in errors:
                print("Validation Error: ", error)
            errors = {
                "errors": errors,
            }
            return errors

    def update(self, **kwargs):
        """
        Validere og Oppdatere Eksisterende Trennings Økt
        """

        errors = []

        # Hvis Navn er Mindre enn to bokstaver
        if len(kwargs["name"]) < 2:
            errors.append('Navn er Obligatorisk og må innholde mer enn to Bokstaver')

        # Ser Om Navnet Innholder Bokstaver eller Tall.

        WORKOUT_REGEX = re.compile(
            r'^\s*[A-Za-z0-9!@#$%^&*\"\':;\/?,<.>()-_=+\]\[~`]+(?:\s+[A-Za-z0-9!@#$%^&*\"\':;\/?,<.>()-_=+\]\[~`]+)*\s*$')

        if not WORKOUT_REGEX.match(kwargs["name"]):
            errors.append('Navn Må Innholde Bokstaver eller Tall.')

        # Notater

        if len(kwargs["description"]) < 2:
            errors.append('Notater må innholde mer enn to bokstaver')

        if not WORKOUT_REGEX.match(kwargs["description"]):
            errors.append('Notater Må Innholde Bokstaver eller Tall.')

        # Sjekk for Evt Feil
        if len(errors) == 0:

            # Update workout:
            workout = Workout.objects.filter(id=kwargs['workout_id']).update(name=kwargs['name'],
                                                                             description=kwargs["description"])

            # Return updated Workout:
            updated_workout = {
                "updated_workout": workout
            }
            return updated_workout
        else:
            # Else, if validation fails, print errors to console and return errors object:
            for error in errors:
                print("Validation Error: ", error)
            # Prepare data for controller:
            errors = {
                "errors": errors,
            }
            return errors


class ExerciseManager(models.Manager):

    def new(self, **kwargs):
        """
        Validere Og Registrere Ny Økt
        """

        errors = []

        # Alle Felt Må Være Fylt
        if not kwargs['name'] or not kwargs['weight'] or not kwargs['repetitions']:
            errors.append('Alle Felt Må Være Fylt!!')

        if len(kwargs["name"]) < 2:
            errors.append('Name is required and must be at least 2 characters long.')

        EXERCISE_REGEX = re.compile(
            r'^\s*[A-Za-z0-9!@#$%^&*\"\':;\/?,<.>()-_=+\]\[~`]+(?:\s+[A-Za-z0-9!@#$%^&*\"\':;\/?,<.>()-_=+\]\[~`]+)*\s*$')

        if not EXERCISE_REGEX.match(kwargs["name"]):
            errors.append('Name must contain letters, numbers and basic characters only.')

        # Konvertering av Tall i Vekt og Repitasjon Feltene
        try:
            kwargs["weight"] = round(float(kwargs["weight"]), 1)
            kwargs["repetitions"] = round(float(kwargs["repetitions"]), 1)

            # De bør være Positvit Tall
            if (kwargs["weight"] < 0) or (kwargs["repetitions"] < 0):
                errors.append('Vekt eller Reptisjon Felt må være Postivt tall.')

        except ValueError:
            # Evt Feil
            errors.append(
                'Vekt eller Reptisjon Felt må være  KUN Postivt tall.')

        # Om Evt Validering Feil
        if len(errors) == 0:
            validated_exercise = {
                "exercise": Exercise(name=kwargs["name"], weight=kwargs["weight"], repetitions=kwargs["repetitions"],
                                     workout=kwargs["workout"]),
            }
            validated_exercise["exercise"].save()
            return validated_exercise
        else:
            for error in errors:
                print("Validering: ", error)
            errors = {
                "errors": errors,
            }
            return errors


class Workout(models.Model):
    """Creates instances of `Workout`."""

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WorkoutManager()


class Exercise(models.Model):
    """Creates instances of `Exercise`."""

    name = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=999, decimal_places=1)
    repetitions = models.DecimalField(max_digits=999, decimal_places=1)
    category = models.CharField(max_length=50,
                                default="Strength Training")
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ExerciseManager()
