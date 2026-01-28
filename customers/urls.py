from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views
from .views import CustomerViewSet

router = DefaultRouter()
#prefix and viewset created at class name of view
router.register(r'', views.CustomerViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("user-profile", views.create_profile, name='create-profile'),

]
