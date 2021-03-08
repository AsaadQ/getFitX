from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def calc(request):
    return render(request, 'kalori.html')

def home(request):
    return render(request, 'home.html')