from django.shortcuts import render
from rest_framework import viewsets
from .models import Customer, UserProfile
from .serializers import CustomerSerializer

# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

def create_profile(request):
    user_profile = UserProfile.objects.create(
        username = 'Ian',
        email = 'ian@example.com',
        ssn = '123-446-7',
        bio = 'This is a bio about Ian'
    )

    context = {
        'user_profile': user_profile
    }
    
    print(user_profile.ssn)
    print(user_profile.bio)

    return render(user_profile, 'user_profile.html', context)
    