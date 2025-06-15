from django.urls import path
from .views import *

urlpatterns = [
    # Define your home app URLs here
    path('faculty/', faculty_homepage, name='faculty_home'),
    path('student/', student_homepage, name='student_home'),
    path('admin/', admin_homepage, name='admin_home'),
    path('admin/user_management/', user_management, name='user_management'),
    path('admin/add_user/', add_user, name='add_user'),
    path('admin/faculty_designations_management/', faculty_designations_management, name='faculty_designations_management'),
    # Redirector for the home page
    path('', redirector, name='home'),
]