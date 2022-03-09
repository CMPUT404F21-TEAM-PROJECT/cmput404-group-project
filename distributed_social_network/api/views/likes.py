from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from ..models import Author, Like, Post, Comment
from ..serializers import  LikeSerializer
from ..views import find_post
from django.db.models import Q


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
    likes = Like.objects.filter(Q(object__contains = queryString) & ~Q(object__contains = "comments") )  

    # Create the JSON response dictionary
    serializer = LikeSerializer(likes, many=True)
    items = serializer.data
    object = post.id #Url to post. (postID is just the id where as post.id is the full url)
    responseDict = {'type' : 'liked', 'items' : items, 'object' : object}

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
        #TODO fix issue with comment = None
        response.status_code = 404
        return response

    # Get likes
    queryString = "{0}/posts/{1}/comments/{2}".format(authorID, postID, commentID)
    likes = Like.objects.filter(object__contains = queryString)  

    serializer = LikeSerializer(likes, many=True)
    items = serializer.data
    object = comment.id #Url to coment. (commentID is just the id where as comment.id is the full url)
    responseDict = {'type' : 'liked', 'items' : items, 'object' : object}

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
    object = author.url
    responseDict = {'type' : 'liked', 'items' : items, "object" : object}

    # Return the response
    response = JsonResponse(responseDict)
    response.status_code = 200
    return response

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