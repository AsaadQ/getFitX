from django.db import models
import re  # regex for email validation
import bcrypt  # bcrypt for password encryption/decryption
from decimal import *  # for decimal number purposes
from django.contrib.auth.models import User

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(models.Manager):
    """Additional instance method functions for `User`"""

    def register(self, **kwargs):
        """
        Validates and registers a new user.
        Parameters:
        - `self` - Instance to whom this method belongs.
        - `**kwargs` - Dictionary object of registration values from controller to be validated.
        Validations:
        - Username - Required; No fewer than 2 characters; letters only
        - Email - Required, Valid Format, Not Taken
        - Password - Required; Min 8 char, Matches Password Confirmation
        """

        # Create empty errors list, which we'll return to generate django messages back in our controller:
        errors = []

        # ---------------#
        # -- USERNAME: --#
        # ---------------#
        # Check if username is less than 2 characters:
        if len(kwargs["username"][0]) < 2:
            errors.append('Username is required and must be at least 2 characters long.')

        # Check if username contains letters, numbers and basic characters only:
        USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9!@#$%^&*()?]*$')  # Create regex object
        # Test username against regex object:
        if not USERNAME_REGEX.match(kwargs["username"][0]):
            errors.append('Username must contain letters, numbers and basic characters only.')

        # ---------------#
        # -- EXISTING: --#
        # ---------------#
        # Check for existing User via username:
        if len(User.objects.filter(username=kwargs["username"][0])) > 0:
            errors.append('Username is already registered to another user.')

        # ------------#
        # -- EMAIL: --#
        # ------------#
        # Check if email field is empty:
        if len(kwargs["email"][0]) < 5:
            errors.append('Email field must be at least 5 characters.')

        # Else if email is greater than 5 characters:
        else:
            # Check if email is in valid format (using regex):
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
            if not EMAIL_REGEX.match(kwargs["email"][0]):
                errors.append('Email field is not a valid email format.')
            else:
                # ---------------#
                # -- EXISTING: --#
                # ---------------#
                # Check for existing User via email:
                if len(User.objects.filter(email=kwargs["email"][0])) > 0:
                    errors.append('Email address is already registered to another user.')

        # ---------------#
        # -- PASSWORD: --#
        # ---------------#
        # Check if password is less than 8 characters:
        if len(kwargs["password"][0]) < 8 or len(kwargs["password_confirmation"][0]) < 8:
            errors.append('Password fields are required and must be at least 8 characters.')
        else:
            # Check if password matches confirmation password:
            if kwargs["password"][0] != kwargs["password_confirmation"][0]:
                errors.append('Password and confirmation must match.')

        # -----------------#
        # -- TOS ACCEPT: --#
        # -----------------#
        # Check if TOS box is accepted:
        # Note: HTML5 required attribute is set, but just in case:
        if kwargs["tos_accept"][0] == "on":
            kwargs["tos_accept"][0] = True
        else:
            errors.append("Terms of service must be accepted.")

        # Check for validation errors:
        # If none, hash password, create user and send new user back:
        if len(errors) == 0:
            kwargs["password"][0] = bcrypt.hashpw((kwargs["password"][0]).encode(), bcrypt.gensalt(14))
            # Create new validated User:
            validated_user = {
                "logged_in_user": User(username=kwargs["username"][0], email=kwargs["email"][0],
                                       password=kwargs["password"][0], tos_accept=kwargs["tos_accept"][0]),
            }
            # Save new User:
            validated_user["logged_in_user"].save()
            # Return created User:
            return validated_user
        else:
            # Else, if validation fails, print errors to console and return errors object:
            for error in errors:
                print("Validation Error: ", error)
            # Prepare data for controller:
            errors = {
                "errors": errors,
            }
            return errors

    def login(self, **kwargs):
        """
        Validates and logs in a new user.
        Parameters:
        - `self` - Instance to whom this method belongs.
        - `**kwargs` - Dictionary object of login values from controller.
        Validations:
        - All fields required.
        - Existing User is found.
        - Password matches User's stored password.
        """

        # Create empty errors list:
        errors = []

        # ------------------#
        # --- ALL FIELDS ---#
        # ------------------#
        # Check that all fields are required:
        if len(kwargs["username"][0]) < 1 or len(kwargs["password"][0]) < 1:
            errors.append('All fields are required.')
        else:
            # ------------------#
            # ---- EXISTING ----#
            # ------------------#
            # Look for existing User to login by username:
            try:
                logged_in_user = User.objects.get(username=kwargs["username"][0])

                # ------------------#
                # ---- PASSWORD ----#
                # ------------------#
                # Compare passwords with bcrypt:
                # Note: We must encode both prior to testing
                try:

                    password = kwargs["password"][0].encode()
                    hashed = logged_in_user.password.encode()

                    if not (bcrypt.checkpw(password, hashed)):
                        print("ERROR: PASSWORD IS INCORRECT")
                        # Note: We send back a general error that does not specify what credential is invalid: this is for security purposes and is admittedly a slight inconvenience to our user, but makes it harder to gather information from the server during brute for attempts
                        errors.append("Username or password is incorrect.")

                except ValueError:
                    # If user's stored password is unable to be used by bcrypt (likely b/c password is not hashed):
                    errors.append('This user is corrupt. Please contact the administrator.')

            # If existing User is not found:
            except User.DoesNotExist:
                print("ERROR: USERNAME IS INVALID")
                # Note: See password validation note above:
                errors.append('Username or password is incorrect.')

        # If no validation errors, return logged in user:
        if len(errors) == 0:
            # Prepare data for controller:
            validated_user = {
                "logged_in_user": logged_in_user,
            }
            # Send back validated logged in User:
            return validated_user
        # Else, if validation fails print errors and return errors to controller:
        else:
            for error in errors:
                print("Validation Error: ", error)
            # Prepare data for controller:
            errors = {
                "errors": errors,
            }
            return errors


class User(models.Model):
    """Creates instances of `User`."""

    username = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=22)
    tos_accept = models.BooleanField(default=False)
    level = models.IntegerField(default=1)
    level_name = models.CharField(max_length=15, default="Newbie")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() # Adds additional instance methods to `User`


class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @receiver(post_save, sender=User)  # add this
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profil.objects.create(user=instance)

    @receiver(post_save, sender=User)  # add this
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()