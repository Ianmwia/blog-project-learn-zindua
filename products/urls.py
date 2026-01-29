from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views
from .views import ProductsViewSet, ExampleView

router = DefaultRouter()
router.register(r'', views.ProductsViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path('example/', ExampleView.as_view(), name='example-view')

]
