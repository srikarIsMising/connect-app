from django.shortcuts import redirect, render

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        redirect(request, 'home/homepage.html')
    else:
        # Render the login form
        return render(request, 'auth/login.html')
