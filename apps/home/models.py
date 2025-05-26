from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
class Users(AbstractBaseUser):
    USER_TYPRE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    ]
    userId = models.IntegerField(primary_key=True)
    fullName = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)
    phoneNumber = models.CharField(max_length=15, unique=True, null=False, blank=False)
    userType = models.CharField(max_length=20, choices=USER_TYPRE_CHOICES, default='faculty')
    institutionId = models.CharField(max_length=20, unique=True, null=False, blank=False, default="1234567890")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class FacultyDepartments(models.Model):
    departmentId = models.IntegerField(primary_key=True)
    departmentName = models.CharField(max_length=100, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'faculty_departments'
        verbose_name = 'Faculty Department'
        verbose_name_plural = 'Faculty Departments'

    def __str__(self):
        return self.departmentName


class FacultyDesignations(models.Model):
    designationId = models.IntegerField(primary_key=True)
    designationName = models.CharField(max_length=100, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'faculty_designations'
        verbose_name = 'Faculty Designation'
        verbose_name_plural = 'Faculty Designations'

    def __str__(self):
        return self.designationName


class FacultyProfile(models.Model):
    userId = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='faculty_groups')
    departmentId = models.ForeignKey(FacultyDepartments, on_delete=models.CASCADE, related_name='faculty_groups')
    designationId = models.ForeignKey(FacultyDesignations, on_delete=models.CASCADE, related_name='faculty_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'faculty_groups'
        verbose_name = 'Faculty Group'
        verbose_name_plural = 'Faculty Groups'

class StudentsCourse(models.Model):
    courseId = models.IntegerField(primary_key=True)
    courseName = models.CharField(max_length=100, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students_courses'
        verbose_name = 'Student Course'
        verbose_name_plural = 'Student Courses'
    
    def __str__(self):
        return self.courseName
    
class CourseDivisions(models.Model):
    divisionId = models.IntegerField(primary_key=True)
    divisionName = models.CharField(max_length=100, unique=True, null=False, blank=False)
    courseId = models.ForeignKey(StudentsCourse, on_delete=models.CASCADE, related_name='course_divisions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'course_divisions'
        verbose_name = 'Course Division'
        verbose_name_plural = 'Course Divisions'

    def __str__(self):
        return self.divisionName
    

