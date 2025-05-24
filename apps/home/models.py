from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
class FacultyUsers(AbstractBaseUser):
    userId = models.IntegerField(primary_key=True)
    fullName = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    phoneNumber = models.CharField(max_length=15, unique=True, null=False, blank=False)
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'faculty_users'
        verbose_name = 'Faculty User'
        verbose_name_plural = 'Faculty Users'

class Departmants(models.Model):
    departmentId = models.IntegerField(primary_key=True)
    departmentName = models.CharField(max_length=100, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'departments'
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.departmentName



