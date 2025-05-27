from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import *

# Create your views here.
def redirector(request):
    """
    Redirects to the appropriate homepage based on user type.
    """
    if request.user.is_authenticated:
        if request.user.userType == 'faculty':
            return redirect('faculty_home')
        elif request.user.userType == 'student':
            return redirect('student_home')
        elif request.user.userType == 'admin':
            return redirect('admin_home')
    else:
        return redirect('../../auth/login')  # Redirect to login if not authenticated

#student views
@user_is_student
def student_homepage(request):
    return render(request, 'home/students/homepage.html')


#faculty views
@user_is_faculty
def faculty_homepage(request):
    return render(request, 'home/faculty/homepage.html')

#admin views
@user_is_admin
def admin_homepage(request):
    return render(request, 'home/admin_homepage.html')