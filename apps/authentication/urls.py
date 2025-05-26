from django.urls import path
from .views import *

urlpatterns = [
    # Define your authentication app URLs here
    path('login/', login_view, name='login'),
]