from django.urls import path
from .views import *

urlpatterns = [
    # Define your home app URLs here
    path('faculty/', faculty_homepage, name='faculty_home'),
    path('student/', student_homepage, name='student_home'),
    path('admin/', admin_homepage, name='admin_home'),
    path('', redirector, name='home'),
]