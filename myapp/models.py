from django.db import models
#from django.utils import timezone
from django.contrib.auth.models import User
#from django.core.urlresolvers import reverse
from cloudinary.models import CloudinaryField
#21
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(blank=True, unique=True)
    #phone_number  = models.IntegerField(blank=True)
    age = models.IntegerField(default=18)

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, unique=True)
    bio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        """
        Docstring for __str__
        string representation for Author model
        :param self: Description
        """
        return f'{self.first_name} {self.last_name}'


class Blog(models.Model):
    """
    Foreign key to relate blog table with the author
    """
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = CloudinaryField('image', null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now_add=True)

    editor = models.ForeignKey("Editor", on_delete=models.CASCADE, default=1)

    # def save(self, *args, **kwargs):
    #     if self.is_published and not self.published_at:
    #         self.published_at = timezone.now()

    def __str__(self):
        return (f'{self.title}')
    
    # def get_absolute_url(self):
    #     """_summary_

    #     Returns:
    #         url to access a particular instance of the model
    #     """
    #     return reverse('model_detail', args=[str(self.id)])

    
class Editor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)


 #MODEL FIELD TYPES
 #text = models.TextField() - stores large amount of text data no args needed
#description = models.TextField(_(""))
 #price = models.FloatField(_("")) - floating point numbers
 #is_active = models.BooleanField(_("")) - true or false -- set a default
 #kyc know you customer, unique field like  birthdate datefield vs datetime
 #date = models.DateField(_(""), auto_now=False, auto_now_add=False) no args
# email = models.EmailField(_(""), max_length=254)
#website = models.URLField(_(""), max_length=200)

#foreign key is 1 to many
#many to many is relationship to many tables like book to genre and each genre has different books
#categories = models.ManyToManyField("app.Model", verbose_name=_("")) inherit from Book object
#categories = models.ManyToManyField(Book)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    content = models.TextField()

    class Meta:
        ordering = ['title', 'author']

categories = models.ManyToManyField(Book)

class Profile(models.Model):
    username = models.CharField(max_length=100)
    avatar = models.FileField(upload_to=None, max_length=100) #add a profile image

#one to one relate e.g user to 1 profile
profile = models.OneToOneField(Profile, on_delete=models.CASCADE)


class Meta:
        verbose_name = "Editor"
        verbose_name_plural = "Editors"
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['last_name', 'first_name']),
        ]

def __str__(self):
    return f"{self.first_name} {self.last_name} - {self.email}"

# django newsletter 20-01-2026
class Subscriber(models.Model):
    email = models.EmailField(unique=True, max_length=254) # unique tue subscribe once
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
#custom user
class CustomUserManager(BaseUserManager):
    """Manager where email is the unique identifier for authentication."""
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email