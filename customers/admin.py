from django.contrib import admin

from customers.models import Customer, UserProfile

# Register your models here.
admin.site.register(Customer)
admin.site.register(UserProfile)