from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
class FacultyUserManager(BaseUserManager):
    def create_user(self, email, fullName, phoneNumber, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not fullName:
            raise ValueError('Users must have a full name')
        if not phoneNumber:
            raise ValueError('Users must have a phone number')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            fullName=fullName,
            phoneNumber=phoneNumber,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullName, phoneNumber, username, password):
        user = self.create_user(email, fullName, phoneNumber, username, password)
        user.is_active = True
        user.save(using=self._db)
        return user


class FacultyUsers(AbstractBaseUser):
    userId = models.IntegerField(primary_key=True)
    fullName = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    phoneNumber = models.CharField(max_length=15, unique=True, null=False, blank=False)
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = FacultyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullName', 'phoneNumber', 'username']
    def __str__(self):
        return self.fullName

    class Meta:
        db_table = 'faculty_users'
        verbose_name = 'Faculty User'
        verbose_name_plural = 'Faculty Users'

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


