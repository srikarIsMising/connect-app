from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Create your models here.
class UserManager(BaseUserManager):
    def _create_user(self, institutionId, fullName, email, password=None, **extra_fields):
        if not institutionId:
            raise ValueError('The Institution ID must be set')
        if not fullName:
            raise ValueError('The Full Name must be set')
        if not email:
            raise ValueError('The Email must be set')

        user = self.model(
            institutionId=institutionId,
            fullName=fullName,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user_faculty(self, institutionId, fullName, email, password=None, **extra_fields):
        extra_fields.setdefault('userType', 'faculty')
        return self._create_user(institutionId, fullName, email, password, **extra_fields)

    def create_user_student(self, institutionId, fullName, email, password=None, **extra_fields):
        extra_fields.setdefault('userType', 'student')
        return self._create_user(institutionId, fullName, email, password, **extra_fields)

    def create_superuser(self, institutionId, fullName, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('userType', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(institutionId, fullName, email, password, **extra_fields)
    
    def delete_user(self, institutionId):
        try:
            user = self.get(institutionId=institutionId)
            user.delete()
            return True
        except Users.DoesNotExist:
            return False

class Users(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    ]
    userId = models.BigAutoField(primary_key=True)
    fullName = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    phoneNumber = models.CharField(max_length=15, null=False, blank=False)
    userType = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='faculty')
    institutionId = models.CharField(max_length=20, unique=True, null=False, blank=False, default="1234567890")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'institutionId'
    REQUIRED_FIELDS = ['email', 'fullName']
    def __str__(self):
        return f"{self.fullName} ({self.email})"

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
    designationId = models.AutoField(primary_key=True)
    designationName = models.CharField(max_length=100, unique=True, null=False, blank=False)
    level = models.IntegerField(default=None, blank=False)
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

class StudentsStreams(models.Model):
    streamId = models.IntegerField(primary_key=True)
    streamName = models.CharField(max_length=100, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students_streams'
        verbose_name = 'Student Stream'
        verbose_name_plural = 'Student Streams'

    def __str__(self):
        return self.streamName

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
    
class StudentsCourseDivisions(models.Model):
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
    

