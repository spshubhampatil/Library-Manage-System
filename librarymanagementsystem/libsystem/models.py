from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    User)
from django.utils import timezone


class SiteUserManager(BaseUserManager):   

    def create_user(self, email, password=None, is_staff=False, is_active=True,
                    is_admin=False,):
        
        if not password:
            raise ValueError('user must have a password')

        user = self.model(
            email=email,
            password=password,
           
        )

        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  password=None,):
        user = self.create_user(
            email=email,            
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password=None, ):
        user = self.create_user(
            email=email,            
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user



class SiteUser(AbstractBaseUser):

    profile_name = models.CharField(max_length=30, null=True, blank=True)
    
    email = models.EmailField(
        'Email-id', max_length=255, null=True, blank=True,unique=True)
    name = models.CharField('Name', max_length=50,
                            null=True, blank=True)

    
    is_deleted = models.BooleanField(default=False)

   
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)      

    password = models.CharField(max_length=2000, null=True, blank=True)

    auto_timedate = models.DateTimeField(default=timezone.now, blank=True)

    objects = SiteUserManager()

    USERNAME_FIELD = 'email'
    

    def __str__(self):
        return str(self.profile_name)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @is_staff.setter
    def is_staff(self, value):
        self._is_staff = value



class Book(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book", null=True, blank=True)
    isbn = models.CharField('ISBN', max_length=13, null=True, blank=True)       
    total_copies = models.IntegerField( null=True, blank=True)
    available_copies = models.IntegerField( null=True, blank=True)
    pic=models.ImageField(blank=True, null=True, upload_to='book_image')

    def __str__(self):
        return self.title