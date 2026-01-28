from django.db import models
from django.utils.translation import gettext_lazy as _
from encrypted_model_fields.fields import EncryptedCharField, EncryptedTextField

# Create your models here.
class Customer(models.Model):
    class Gender(models.TextChoices):
        '''
        subclass for gender
        takes in 2 params, db value stored in db and _() wrapped label shown in form
        '''
        MALE = 'M',_('Male')
        FEMALE = 'F',_('Female')
        PREFER_NOT_TO_SAY = 'N',_('Prefer not to say')
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    email = models.EmailField(_("customer email"), max_length=254)
    age = models.IntegerField(_("age of customer"))
    gender = models.CharField(_("customers gender"), max_length=1 ,choices=Gender.choices, default=Gender.PREFER_NOT_TO_SAY)
    city = models.CharField(_("city located"), max_length=50)
    created_at = models.DateTimeField(_("date joined"), auto_now_add=True)

    def __str__(self):
        return f' {self.first_name} {self.last_name} {self.age} {self.email} {self.gender}'
    
class UserProfile(models.Model):
    username = models.CharField(_("username"), max_length=50)
    email = models.EmailField(_("user email"))
    ssn = EncryptedCharField(max_length=11)
    bio = EncryptedTextField()

    def __str__(self):
        return self.username