from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BlogForm, ContactForm
from .models import Blog, Subscriber, Author
import datetime
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
#serializers
from .serializers import BlogSerializer, AuthorSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.db import IntegrityError

#serializers api -- func based api views vs class based serializers

class BlogListCreateAPIView(APIView):
    #methods
    def get(self, request):
        blogs = Blog.objects.select_related('author').all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'detail':'Invalid Data'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

class BlogDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            raise exceptions.NotFound(f"Blog with ID {pk} not found.")

    def get(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def put(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data)
            except IntegrityError:
                return Response({"detail": "Invalid data."}, status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blog = self.get_object(pk)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AuthorListAPIView(APIView):
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)
        

# Create your views here.
def index(request):
    return HttpResponse("Hello World! Welcome to django")

def home(request):
    context2 = {"Message": "Hello and welcome to my first django project"}
    return render(request,"home.html", context=context2)


def add_blog(request):
    
        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES)
            if form.is_valid():
                blog = form.save(commit=False)
                blog.save()
                return redirect('blog_list')
        else:
            form = BlogForm()
        return render(request, 'add_blog.html', {"form": form})


 
def blog_list(request):
    blogs = Blog.objects.all().order_by('created_at')
    # blog = Blog.objects.filter(title_contains = 'blog')
    # select * from blog where title like '%blog%'

    
    context = {'blogs': blogs}
    return render(request, 'blog_list.html', context )
def filter_demo(request):
    context = {"message": ("Fisheries form"
    " a large part of economies in many African countries, making data on fish stocks a highly"
    " coveted strategic asset, but few governments have resources to conduct regular searches. West Africa, meanwhile, "
    "has become the global epicenter of illegal fishing, losing up to $9.4 billion a year to unreported and unregulated "
    "catches, according to estimates from the Financial Transparency Coalition."),
    
    'my_date' : datetime.datetime.now()
    }
    
    return render(request, 'filter_demo.html', context)

def subscribe(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Subscriber.objects.filter(email=email).exists():
            messages.error(request, 'You have already subscribed')
        else:
            subscriber = Subscriber(email=email)
            subscriber.save()
            messages.success(request, 'Thank You for subscribing')
            return redirect('blog_list')
    return render(request, 'subscribe.html')

#404
def error_404(request, exception):
    return render(request, '404.html')

#forms .py contact form
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            #send email
            send_mail(
                f'{subject} from {name}', 
                message, 
                email,
                ['admin@example.com']
            )
        return render(request, 'contact_success.html')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

#logout
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been Logged out successfully')
    return redirect('login')

#override registration to add roles
def registration(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.success(request, 'Registration Successful')
            return redirect('blog_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'django_registration_register', {'form': form})

# define serializers
