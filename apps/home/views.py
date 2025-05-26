from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def homepage(request):
    return render(request, 'home/homepage.html')
