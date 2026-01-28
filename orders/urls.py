from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views
from .views import checkout

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("checkout", checkout, name = 'checkout'),

]
