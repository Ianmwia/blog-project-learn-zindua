from django import forms
from .models import Blog, Author
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

#consume the models here
# follows same schema as models with class objects
class BlogForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), empty_label='Select an Author')

    class Meta:
        ''' 
        pulls all data from the blog to avoid rewriting same as blog
        stored in a variable
        2.define fields you want represented in an array
        
        '''
        model = Blog
        fields = ['author', 'title', 'image', 'content', 'is_published']

    def __init__(self, *args, **kwargs):
        return super(BlogForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_date = super().clean()
        return cleaned_date
    

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your Name'
            }
        ),
    )
    email = forms.EmailField(
        widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email'}),
    )
    subject = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
    )
    message = forms.CharField(
        widget = forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Send Us A Message', 'rows': 5}),
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # custom validation
        if 'example.com' in email:
            raise forms.ValidationError('Example.com emails are not allowed')
        return email
    
class CustomUserCreationForm(UserCreationForm):
    CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('normal', 'Normal'),
    ]
    role = forms.ChoiceField(choices=CHOICES, required=True, label='Select role')

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'role']

    #define roles
    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data['role'] == 'admin':
            user.is_superuser = True
            user.is_staff = True
        elif self.cleaned_data['role'] == 'staff':
            user.is_superuser = False
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False

        if commit:
            user.save()

        return user