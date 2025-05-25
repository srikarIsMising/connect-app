from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
class FacultyUserManager(BaseUserManager):
    def create_user(self, facultyId, fullName, email, phoneNumber, password, **extra_fields):
        if not facultyId:
            raise ValueError('Faculty ID is required')
        if not email:
            raise ValueError('Email is required')
        if not phoneNumber:
            raise ValueError('Phone number is required')
        if not password:
            raise ValueError('Password is required')

        user = self.model(
            facultyId=facultyId,
            fullName=fullName,
            email=self.normalize_email(email),
            phoneNumber=phoneNumber
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, facultyId, fullName, email, phoneNumber, password):
        user = self.create_user(facultyId, fullName, email, phoneNumber, password)
        user.is_active = True
        user.save(using=self._db)
        return user

class FacultyUsers(AbstractBaseUser):
    userId = models.IntegerField(primary_key=True)
    fullName = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    phoneNumber = models.CharField(max_length=15, unique=True, null=False, blank=False)
    facultyId = models.CharField(max_length=20, unique=True, null=False, blank=False, default="1234567890")
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = FacultyUSerManager()
    USERNAME_FIELD = 'facultyId'
    REQUIRED_FIELDS = ['fullName', 'email', 'phoneNumber', 'password']
    def __str__(self):
        return f"{self.fullName} ({self.facultyId})"

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


class FacultyGroups(models.Model):
    userId = models.OneToOneField(FacultyUsers, on_delete=models.CASCADE, related_name='faculty_groups')
    departmentId = models.ForeignKey(FacultyDepartments, on_delete=models.CASCADE, related_name='faculty_groups')
    designationId = models.ForeignKey(FacultyDesignations, on_delete=models.CASCADE, related_name='faculty_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'faculty_groups'
        verbose_name = 'Faculty Group'
        verbose_name_plural = 'Faculty Groups'

class StudentsUsers(AbstractBaseUser):
    userId = models.IntegerField(primary_key=True)
    fullName = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    phoneNumber = models.CharField(max_length=15, unique=True, null=False, blank=False)
    studentId = models.CharField(max_length=20, unique=True, null=False, blank=False, default="1234567890")
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students_users'
        verbose_name = 'Student User'
        verbose_name_plural = 'Student Users'

    def __str__(self):
        return f"{self.fullName} ({self.studentId})"

class StudentsBranch(models.Model):
    branchId = models.IntegerField(primary_key=True)
    branchName = models.CharField(max_length=100, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students_branch'
        verbose_name = 'Student Branch'
        verbose_name_plural = 'Student Branches'
    
    def __str__(self):
        return self.branchName

