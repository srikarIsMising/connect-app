from traceback import print_tb

from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        # If the user is already authenticated, redirect to the homepage or another page
        return redirect('../../')

    if request.method == 'POST':
        institutionId = request.POST.get('institutionId')
        password = request.POST.get('password')
        # Here you would typically authenticate the user
        # For example, using Django's built-in authentication system:
        print(institutionId)
        print(password)
        user = authenticate(request, institutionId=institutionId, password=password)
        if user is not None:
            # If the user is authenticated, log them in
            login(request, user)
            if user.userType == 'faculty':
                # Redirect to the faculty homepage or any other page
                return redirect('../../faculty/')
            elif user.userType == 'student':
                # Redirect to the student homepage or any other page
                return redirect('../../student/')
            elif user.userType == 'admin':
                # Redirect to the admin homepage or any other page
                return redirect('../../admin/')
        else:
            print('unable to authenticate user')
            # If authentication fails, you can render an error message
            return render(request, 'auth/login.html', {'error': 'Invalid credentials'})

    else:
        # Render the login form
        return render(request, 'auth/login.html')


def logout_view(request):
    # Log out the user
    logout(request)
    # Redirect to the login page or any other page
    return redirect('../login')  # Adjust the redirect URL as needed

