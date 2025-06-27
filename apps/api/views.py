from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    """
    Render the home page.
    """
    return HttpResponse("Welcome to the API home page!")