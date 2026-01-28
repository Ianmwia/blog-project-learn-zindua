from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views
from .views import CartViewSet, add_item, remove_item, summary

router = DefaultRouter()
router.register(r'cart', views.CartViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("add_item/", add_item, name='add_item'),
    path("remove_item/", remove_item, name='remove_item'),
    path("summary/", summary, name='summary'),


]
