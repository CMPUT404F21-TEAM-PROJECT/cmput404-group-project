from rest_framework import serializers
from .models import Author, FollowRequest, Post, Comment

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only = True, default = 'author')
    class Meta:
        model = Author
        fields = '__all__'

class FollowRequestSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only = True, default = 'Follow')
    class Meta:
        model = FollowRequest
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only = True, default = 'post')
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only = True, default = 'comment')
    class Meta:
        model = Comment
        fields = '__all__'