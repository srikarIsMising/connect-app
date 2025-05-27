from django.http import HttpResponseForbidden
from functools import wraps

from django.shortcuts import redirect

def user_is_faculty(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.userType == 'faculty':
            return view_func(request, *args, **kwargs)
        return redirect('../../auth/login')
    return _wrapped_view

def user_is_student(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.userType == 'student':
            return view_func(request, *args, **kwargs)
        return redirect('../../auth/login')  # Redirect to login if not authenticated or not a student
    return _wrapped_view

def user_is_admin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.userType == 'admin':
            return view_func(request, *args, **kwargs)
        return redirect('../../auth/login')
    return _wrapped_view