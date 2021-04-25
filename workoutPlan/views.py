from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Workout, Exercise
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def dashboard(request):

    # Load dashboard with data:
    return render(request, "workout/dashboard.html")


def ny_Trening(request):

    try:
        user = User.objects.get(id=request.session['_auth_user_id'])

        data = {
            'user': user,
        }

        if request.method == "GET":
            return render(request, "workout/add_workout.html", data)

        if request.method == "POST":
            workout = {
                "name": request.POST["name"],
                "description": request.POST["description"],
                "user": user
            }

            validated = Workout.objects.new(**workout)

            try:
                if len(validated["errors"]) > 0:
                    print("Workout Kunne ikke ble laget")
                    for error in validated["errors"]:
                        messages.error(request, error, extra_tags='workout')
                    return redirect("/workout")
            except KeyError:
                print("Workout Passert valdering og er lagret")

                id = str(validated['workout'].id)
                return redirect('/workout/' + id)

    except (KeyError, User.DoesNotExist) as err:
        messages.info(request, "Du må være Logget inn..", extra_tags="invalid_session")
        return redirect("/")


def workout(request, id):

    try:
        user = User.objects.get(id=request.session["_auth_user_id"])

        data = {
            'user': user,
            'workout': Workout.objects.get(id=id),
            'exercises': Exercise.objects.filter(workout__id=id).order_by('-updated_at'),
        }

        return render(request, "workout/workout.html", data)

    except (KeyError, User.DoesNotExist) as err:
        messages.info(request, "Du må være Logget Inn.", extra_tags="invalid_session")
        return redirect("/")


def alle_Trening(request):

    try:
        user = User.objects.get(id=request.session["_auth_user_id"])

        workout_list = Workout.objects.filter(user__id=user.id).order_by('-id')

        page = request.GET.get('page', 1)

        paginator = Paginator(workout_list, 12)
        try:
            workouts = paginator.page(page)
        except PageNotAnInteger:
            workouts = paginator.page(1)
        except EmptyPage:
            workouts = paginator.page(paginator.num_pages)

        data = {
            'user': user,
            'workouts': workouts,
        }

        return render(request, "workout/all_workouts.html", data)

    except (KeyError, User.DoesNotExist) as err:
        messages.info(request, "Du må være logget inn.", extra_tags="invalid_session")
        return redirect("/")


def exercise(request, id):

    try:
        user = User.objects.get(id=request.session["_auth_user_id"])

        if request.method == "GET":
            # Slett Økt
            Exercise.objects.get(id=request.GET["exercise_id"]).delete()

            return redirect("/workout/" + id)

        if request.method == "POST":

            exercise = {
                "name": request.POST["name"],
                "weight": request.POST["weight"],
                "repetitions": request.POST["repetitions"],
                "workout": Workout.objects.get(id=id),
            }

            print(exercise)
            validated = Exercise.objects.new(**exercise)

            try:
                if len(validated["errors"]) > 0:
                    print("Exercise Kunne ikke ble laget")

                    # Loop through errors and Generate Django Message for each with custom level and tag:
                    for error in validated["errors"]:
                        messages.error(request, error, extra_tags='exercise')

                    # Reload workout page:
                    return redirect("/workout/" + id)
            except KeyError:
                # If validation successful, load newly created workout page:
                print("Exercise passert Validering og er lagret")

                # Reload workout:
                return redirect('/workout/' + id)

    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "Du må være logget inn", extra_tags="invalid_session")
        return redirect("/")


def edit_workout(request, id):

    try:
        user = User.objects.get(id=request.session["_auth_user_id"])

        data = {
            'user': user,
            'workout': Workout.objects.get(id=id),
            'exercises': Exercise.objects.filter(workout__id=id),
        }

        if request.method == "GET":
            return render(request, "workout/edit_workout.html", data)

        if request.method == "POST":
            workout = {
                'name': request.POST['name'],
                'description': request.POST['description'],
                'workout_id': data['workout'].id,
            }

            validated = Workout.objects.update(**workout)

            try:
                if len(validated["errors"]) > 0:
                    print("Workout kunne ikke bli lagt")
                    for error in validated["errors"]:
                        messages.error(request, error, extra_tags='edit')
                    return redirect("/workout/" + str(data['workout'].id) + "/edit")
            except KeyError:
                print("oppdater Økt passert Validering og er lagret")

                return redirect("/workout/" + str(data['workout'].id))

    except (KeyError, User.DoesNotExist) as err:
        messages.info(request, "Du må være logget inn..", extra_tags="invalid_session")
        return redirect("/")


def delete_workout(request, id):

    try:
        user = User.objects.get(id=request.session["_auth_user_id"])

        # Slett Økt
        Workout.objects.get(id=id).delete()

        return redirect('/dashboard')


    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("/")


def complete_workout(request, id):

    try:
        user = User.objects.get(id=request.session["_auth_user_id"])

        if request.method == "GET":
            return redirect("/workout/" + id)

        if request.method == "POST":
            workout = Workout.objects.get(id=id)
            workout.completed = True
            workout.save()

            print("Øvelst Fullført")

            return redirect('/workout/' + id)

    except (KeyError, User.DoesNotExist) as err:
        messages.info(request, "Du må være logget inn.", extra_tags="invalid_session")
        return redirect("/")
