from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only = True, default = 'author')
    class Meta:
        model = Author
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only = True, default = 'Like')
    class Meta:
        model = Like
        fields = '__all__'