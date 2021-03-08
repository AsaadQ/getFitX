from django.http import HttpResponse
from django.shortcuts import render
from .models import Days
from .models import Ultra
from .models import Hard
from .models import Basic


# Create your views here.
def dager(request):
    days = Days.objects.all()
    days_navn = []
    for day in days:
        days_navn.append(day.day_name)
    return HttpResponse(days_navn)


def valg(request):
    return render(request, 'Plans/WorkoutValg.html')


def Basic_work(request):
    workout_basic = Basic.objects.all()
    return render(request, 'Plans/workoutBasic.html', {'workout_basic': workout_basic})


def Basic_hard(request):
    workout_hard = Hard.objects.all()
    return render(request, 'Plans/workoutHard.html', {'workout_hard': workout_hard})


def Basic_ultra(request):
    workout_ultra = Ultra.objects.all()
    return render(request, 'Plans/workoutUltra.html', {'workout_ultra': workout_ultra})
