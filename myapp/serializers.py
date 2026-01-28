from rest_framework import serializers
from .models import Blog, Author

#blog and author
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Author
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.__str__', read_only=True)
    class Meta:
        model= Blog
        fields = '__all__'