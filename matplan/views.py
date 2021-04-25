from django.shortcuts import render


# Create your views here.

def Planner(request):
    return render(request, 'MatPlan/Planner.html')
