from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


# Create your views here.

def Planner(request):
    return render(request, 'MatPlan/Planner.html')


def Over(request):
    return render(request, 'MatPlan/Over.html')


def Under(request):
    return render(request, 'MatPlan/Under.html')


def Vegen(request):
    return render(request, 'MatPlan/Vegen.html')
