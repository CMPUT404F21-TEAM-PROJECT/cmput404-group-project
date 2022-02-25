from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse, HttpResponse
from ..models import Author, Like, Post, Comment
from ..serializers import AuthorSerializer, LikeSerializer



# Sends a like to inbox of an author
@api_view(["POST"])
def send_like(request, authorID):
    serializer = LikeSerializer(data = request.data)
    response = HttpResponse()

    if find_author(authorID) is None: 
        # If author is not found, return 404
        response.status_code = 404  
    elif serializer.is_valid():
        # If given data is valid, save the object to the database
        serializer.save()
        response.status_code = 201
    else:
        # If the data is not valid, do not save the object to the database
        response.status_code = 400

    return response

# Gets all the likes on an author's post
@api_view(["GET"])
def get_post_likes(request, authorID, postID):
    response = HttpResponse()

    # Find the author and post with the given id's
    author = find_author(authorID)
    post = find_post(postID)
    if author is None or post is None:
        response.status_code = 404
        return response

    # Get likes
    queryString = "{0}/posts/{1}".format(authorID, postID)
    likes = Like.objects.filter(object_contains = queryString)  

    #TODO make sure empty likes doesnt cause issues
    # Create the JSON response dictionary
    serializer = LikeSerializer(likes, many=True)
    responseDict = serializer.data

    # Return the response
    response = JsonResponse(responseDict)
    response.status_code = 200
    return response

# Gets all likes on an author's comment
@api_view(["GET"])
def get_comment_likes(request, authorID, postID, commentID):
    response = HttpResponse()

    # Find the author, post, and comment with the given id's
    author = find_author(authorID)
    post = find_post(postID)
    comment = find_comment(commentID)
    if author is None or post is None or comment is None:
        response.status_code = 404
        return response

    # Get likes
    queryString = "{0}/posts/{1}/comments/{2}".format(authorID, postID, commentID)
    likes = Like.objects.filter(object_contains = queryString)  

    #TODO make sure empty likes doesnt cause issues
    serializer = LikeSerializer(likes, many=True)
    responseDict = serializer.data

    # Return the response
    response = JsonResponse(responseDict)
    response.status_code = 200
    return response

#TODO check that private info is not disclosed (spec mentioned it could be an issue)
# Get all likes an author has sent
@api_view(["GET"])
def get_author_likes(request, authorID):
    response = HttpResponse()

    # Find the author, post, and comment with the given id's
    author = find_author(authorID)
    if author is None:
        response.status_code = 404
        return response

    
    # Get likes
    likes = Like.objects.filter(author=author)

    #TODO make sure empty likes doesnt cause issues
    # Create the JSON response dictionary
    serializer = LikeSerializer(likes, many=True)
    items = serializer.data
    responseDict = {'type' : 'liked', 'items' : items}

    # Return the response
    response = JsonResponse(responseDict)
    response.status_code = 200
    return response

# Returns Post object if found, otherwise returns None
def find_post(id): 
    try:
        return Post.objects.get(id=id)
    except ObjectDoesNotExist:
        return None

# Returns Comment object if found, otherwise returns None
def find_comment(id):
    try:
        return Comment.objects.get(id=id)
    except ObjectDoesNotExist:
        return None


# Returns the author object if found, otherwise returns None
def find_author(id):
    # Find the author with the given id
    try:
        return Author.objects.get(id=id)
    except ObjectDoesNotExist:
        return None