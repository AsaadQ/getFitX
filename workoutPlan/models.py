from django.db import models
from decimal import *  # for decimal number purposes
from django.contrib.auth.models import User
import re  # regex for email validation


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
        Validates and updates a workout.
        Parameters:
        - `self` - Instance to whom this method belongs.
        - `**kwargs` - Dictionary object of workout values from controller to be validated.
        Validations:
        - Name - Required; No fewer than 2 characters; letters, basic characters, numbers only
        - Description - Required; letters, basic characters, numbers only
        Developer Note:
        - This section utilizes essentially the exact same validations as the `new()` method above (in this same WorkoutManager class). However, in this particular case, we're updating a record rather than creating one. At a later point, it might be good to refactor this section/these validations.
        """

        # Create empty errors list, which we'll return to generate django messages back in our controller:
        errors = []

        # -----------#
        # -- NAME: --#
        # -----------#
        # Check if name is less than 2 characters:
        if len(kwargs["name"]) < 2:
            errors.append('Name is required and must be at least 2 characters long.')

        # Check if name contains letters, numbers and basic characters only:
        '''
        Note: The following regex pattern matches for strings which start or do not start with spaces, whom contain letters, numbers and some basic character sequences, followed by either more spaces or more characters. This prevents empty string submissions.
        '''
        WORKOUT_REGEX = re.compile(
            r'^\s*[A-Za-z0-9!@#$%^&*\"\':;\/?,<.>()-_=+\]\[~`]+(?:\s+[A-Za-z0-9!@#$%^&*\"\':;\/?,<.>()-_=+\]\[~`]+)*\s*$')

        # Test name against regex object:
        if not WORKOUT_REGEX.match(kwargs["name"]):
            errors.append('Name must contain letters, numbers and basic characters only.')

        # ------------------#
        # -- DESCRIPTION: --#
        # ------------------#
        # Check if description is less than 2 characters:
        if len(kwargs["description"]) < 2:
            errors.append('Description is required and must be at least 2 characters long.')

        # Check if description contains letters, numbers and basic characters only:
        # Test description against regex object (we'll just use WORKOUT_REGEX again since the pattern has not changed):
        if not WORKOUT_REGEX.match(kwargs["description"]):
            errors.append('Description must contain letters, numbers and basic characters only.')

        # Check for validation errors:
        # If none, create workout and return new workout:
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
    """Additional instance method functions for `Exercise`"""

    def new(self, **kwargs):
        """
        Validates and registers a new exercise.
        Parameters:
        - `self` - Instance to whom this method belongs.
        - `**kwargs` - Dictionary object of exercise values from controller to be validated.
        Validations:
        - Name - Required; No fewer than 2 characters; letters, basic characters, numbers only
        - Weight (lbs) - Required; Numbers only, Decimals allowed.
        - Repetitions - Required; Numbers only, no Decimals.
        """

        # Create empty errors list, which we'll return to generate django messages back in our controller:
        errors = []

        # ---------------#
        # -- REQUIRED: --#
        # ---------------#
        # Check if all fields are present:
        if not kwargs['name'] or not kwargs['weight'] or not kwargs['repetitions']:
            errors.append('All fields are required.')

        # -----------#
        # -- NAME: --#
        # -----------#
        # Check if name is less than 2 characters:
        if len(kwargs["name"]) < 2:
            errors.append('Name is required and must be at least 2 characters long.')

        # Check if name contains letters, numbers and basic characters only:
        '''
        Note: The following regex pattern matches for strings which start or do not start with spaces, whom contain letters, numbers and some basic character sequences, followed by either more spaces or more characters. This prevents empty string submissions.
        '''
        EXERCISE_REGEX = re.compile(
            r'^\s*[A-Za-z0-9!@#$%^&*\"\':;\/?,<.>()-_=+\]\[~`]+(?:\s+[A-Za-z0-9!@#$%^&*\"\':;\/?,<.>()-_=+\]\[~`]+)*\s*$')

        # Test name against regex object:
        if not EXERCISE_REGEX.match(kwargs["name"]):
            errors.append('Name must contain letters, numbers and basic characters only.')

        # ---------------------------#
        # -- WEIGHT & REPETITIONS: --#
        # ---------------------------#
        # Try converting weight and repetitions to floating numbers, rounded to tenth place:
        try:
            kwargs["weight"] = round(float(kwargs["weight"]), 1)
            kwargs["repetitions"] = round(float(kwargs["repetitions"]), 1)

            # Ensure weight and repetitions is a positive number:
            if (kwargs["weight"] < 0) or (kwargs["repetitions"] < 0):
                errors.append('Weight and repetitions must be a positive number.')

            # Ensure repetitions is a positive number:
            # if (kwargs["repetitions"] < 0):
            #     errors.append('Weight cannot be a negative number.')

        except ValueError:
            # If value error, send error:
            errors.append(
                'Weight and repetitions must be a positive number only, containing at most one decimal place.')

        # Check for validation errors:
        # If none, create exercise and return created exercise:
        if len(errors) == 0:
            # Create new validated exercise:
            validated_exercise = {
                "exercise": Exercise(name=kwargs["name"], weight=kwargs["weight"], repetitions=kwargs["repetitions"],
                                     workout=kwargs["workout"]),
            }
            # Save new Workout:
            validated_exercise["exercise"].save()
            # Return created Workout:
            return validated_exercise
        else:
            # Else, if validation fails, print errors to console and return errors object:
            for error in errors:
                print("Validation Error: ", error)
            # Prepare data for controller:
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
                                default="Strength Training")  # Add more categories in the future: ['Strength Training', 'Endurance Training', 'Balance', 'Flexibility']
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ExerciseManager()
