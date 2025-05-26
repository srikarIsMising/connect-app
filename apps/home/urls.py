from django.urls import path
from .views import homepage

urlpatterns = [
    # Define your home app URLs here
    path('', homepage, name='home'),
]