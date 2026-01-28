"""
URL configuration for blogproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django_registration.backends.one_step.views import RegistrationView
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView #generate token, when expired we refresh

schema_view = get_schema_view(
    openapi.Info(
        title='E-Commerce Api',
        default_version='v1',
        description='Api Documentation'
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("myapp.urls")),
    path('api/', include("myapp.urls")),
    #path('api/', include("products.urls")),
    # / end in / to mean there is more to get from there going forward
    #path('api/v1', include("products.urls", 'v1', namespace='v1')), # api versioning
    #path('api/v1/products/', include(("products.urls", 'v1'), namespace='v1')),
    path('api/v1/products/',include(("products.urls", "products"), namespace="v1")),
    path('api/customers', include("customers.urls")),
    path('customers/', include("customers.urls")),
    path('api/', include("orders.urls")),
    path('api/', include("cart.urls")),

    #swagger urls
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    #jwt token
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token', TokenRefreshView.as_view(), name='token_refresh'),


    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', RegistrationView.as_view(success_url='/'),name='django_registration_register'),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
]

handler404 = 'myapp.views.error_404'