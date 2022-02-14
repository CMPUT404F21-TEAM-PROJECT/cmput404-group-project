from rest_framework import serializers
from .models import Author, Like

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only = True, default = 'author')
    class Meta:
        model = Author
        fields = '__all__'


#TODO check if this supports foreign key for author
class LikeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only = True, default = 'Like')
    class Meta:
        model = Like
        fields = '__all__'