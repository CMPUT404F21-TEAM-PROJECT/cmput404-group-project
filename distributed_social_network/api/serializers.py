from rest_framework import serializers
from .models import Author, FollowRequest, Post, Comment, User, Inbox, Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'passwod': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            # set_password() is a function provided by django to hash the password
            instance.set_password(password)
            instance.save()
        return instance


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

class InboxSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only = True, default = 'inbox')
    posts = PostSerializer(many = True)
    likes = LikeSerializer(many = True)
    follow_requests = FollowRequestSerializer(many = True)
    comments = CommentSerializer(many = True)
    class Meta:
        model = Inbox
        fields = '__all__'