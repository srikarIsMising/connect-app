from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import *
from apps.home.models import *
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    return render(request, 'home/admin/homepage.html')

@user_is_admin
def user_management(request):
    """
    Admin view for managing users.
    """
    users = Users.objects.all()
    total_users = users.count()
    faculty_count = users.filter(userType='faculty').count()
    student_count = users.filter(userType='student').count()
    admin_count = users.filter(userType='admin').count()

    if request.method == 'GET':
        # Handle search functionality
        search_institutionId = request.GET.get('search', '').strip()
        searct_type = request.GET.get('userType', '').strip()
        if search_institutionId:
            users = users.filter(institutionId__icontains=search_institutionId)
        if searct_type:
            if searct_type == 'all':
                users = users.all()
            else  : users = users.filter(userType=searct_type)

    if request.method == 'POST' and request.POST.get('deleteUser'):
        institutionId = request.POST.get('institutionId')
        userId = request.POST.get('userId')
        if institutionId and userId:
            if Users.objects.filter(userId = userId).exists() and Users.objects.filter(userId = userId).first().institutionId == institutionId:
                if request.user.institutionId == institutionId:
                    messages.error(request, "You cannot delete your own account.")
                    return redirect('user_management')
                else:
                    user_to_delete = Users.objects.get(userId=userId)
                    user_to_delete.delete()
                    messages.success(request, f"User with ID {institutionId} has been deleted successfully.")
                    return redirect('user_management')
            else:
                messages.error(request, f"User with ID {institutionId} does not exist or does not match the provided user ID.")
                return redirect('user_management')
        else:
            messages.error(request, "Institution ID and User ID are required to delete a user.")
            return redirect('user_management')
        
    return render(request, 'home/admin/user_management.html', {'page_obj': users, 'total_users': total_users, 'faculty_count': faculty_count, 'student_count': student_count, 'admin_count': admin_count})

@user_is_admin
def add_user(request):
    if request.method == 'POST':
        institution_id = request.POST.get('institutionId')
        full_name = request.POST.get('fullName')
        email = request.POST.get('email')
        phone_number = request.POST.get('phoneNumber')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        user_type = request.POST.get('userType')

        if not all([institution_id, full_name, email, password, user_type]):
            messages.error(request, "All required fields must be filled")
            return render(request, 'home/admin/add_user.html')
            
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'home/admin/add_user.html')

        # Check if user already exists
        if Users.objects.filter(institutionId=institution_id).exists():
            messages.error(request, f"User with ID {institution_id} already exists")
            return render(request, 'home/admin/add_user.html')

        if user_type == 'admin':
            user = Users.objects.create_superuser(
                institutionId=institution_id,
                fullName=full_name,
                email=email,
                password=password
            )
        elif user_type == 'student':
            user = Users.objects.create_user_student(
                institutionId=institution_id,
                fullName=full_name,
                email=email,
                password=password
            )
        elif user_type == 'faculty':
            user = Users.objects.create_user_faculty(
                institutionId=institution_id,
                fullName=full_name,
                email=email,
                password=password
            )

        # Set additional properties
        user.phoneNumber = phone_number if phone_number else ""
        user.userType = user_type

        if user_type == 'admin':
            user.is_staff = True
            user.is_superuser = True
            
        user.save()
        
        return redirect('user_management')
        
    return render(request, 'home/admin/add_user.html')


@user_is_admin
def faculty_designations_management(request):
    designations = FacultyDesignations.objects.all()
    print(designations)
    if (request.method == "POST"):
        designationName = request.POST.get('designationName')
        designationLevel = request.POST.get('level')
        if designationName and designationLevel:
            # Check if the designation already exists
            if FacultyDesignations.objects.filter(designationName=designationName).exists():
                messages.error(request, f"Designation '{designationName}' with level '{designationLevel}' already exists.")
                return redirect('faculty_designations_management')
            # Create a new designation
            print(f"Adding designation: {designationName} with level: {designationLevel}")
            FacultyDesignations.objects.create(designationName=designationName, level=designationLevel, created_at=datetime.now(), updated_at=datetime.now())
            # messages.success(request, f"Designation '{designationName}' with level '{designationLevel}' added successfully.")
        else:
            return redirect('/')
    # Placeholder for faculty designations management logic
    return render(request, 'home/admin/faculty_designations_management.html', {'designations': designations})
