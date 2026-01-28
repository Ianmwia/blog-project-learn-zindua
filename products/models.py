from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Product(models.Model):
    name = models.CharField(_("product name"), max_length=50)
    description = models.TextField(_("description"))
    price = models.DecimalField(_("product price"), max_digits=10, decimal_places=2)
    stock = models.IntegerField(_("amount of products"))
    created_at = models.DateTimeField(_("when product was created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("when stock was increased"), auto_now=True)
    image_url = models.URLField(_("product image"), blank=True)

    def __str__(self):
        return self.name
    