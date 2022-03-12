from importlib_metadata import re
import jwt
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from rest_framework.pagination import PageNumberPagination
from ..models import Comment, Post
from ..serializers import CommentSerializer
from ..views import find_post
from .auth import get_payload

# Routes the request for multiple comment
# Expects JSON request body with post and author attributes
@api_view(['GET', 'POST'])
def route_multiple_comments(request, post_id, author_id):
    if request.method == 'GET':
        return get_comments(request, post_id)
    elif request.method == 'POST':
        return add_comment(request, author_id, post_id)

# Routes the request for a single comment
@api_view(['GET', 'PUT', 'DELETE'])
def route_single_comment(request, post_id, author_id, comment_id):
    if request.method == 'GET':
        return get_comment(request, comment_id)
    elif request.method == 'PUT':
        return update_comment(request, comment_id)
    elif request.method == 'DELETE':
        return delete_comment(request, comment_id)

# Gets all comments for a particular post
def get_comments(request, post_id):
    response = HttpResponse()
    # Checks that the provided post_id exists within the database
    if not find_post(post_id):
        response.status_code = 404
        response.content = "Error: Post Not Found"
        return response

    # Initialize paginator
    paginator = PageNumberPagination()
    paginator.page_query_param = 'page'
    paginator.page_size_query_param = 'size'

    # Get all comments, ordered by the latest published dates paginated
    comments = paginator.paginate_queryset(Comment.objects.all().filter(post_id=post_id).order_by('-published'), request)

    # Create the JSON response dictionary
    serializer = CommentSerializer(comments, many=True)
    items = serializer.data
    responseDict = {'type' : 'comments', 'items' : items}

    # Return the response
    response = JsonResponse(responseDict)
    response.status_code = 200
    return response

# Adds a new comment to an existing post
# Expects JSON request body with post and author attributes
def add_comment(request, author_id, post_id):
    response = HttpResponse()
    
    # Check authorization
    payload = get_payload(request)
    if not payload:
        response.status_code = 401
        response.content = "Error: Not Authenticated"
    user_id = payload['id']
    # Uses the current user and time as author and published respectively
    request.data["author"] = user_id
    request.data["published"] = timezone.localtime(timezone.now())

    # Serialize a new Comment object
    serializer = CommentSerializer(data = request.data)
    print(request.data)

    # If given data is valid, save the object to the database
    if serializer.is_valid():
        serializer.save()
        responseDict = serializer.data
        response = JsonResponse(responseDict)
        response.status_code = 201
        return response
    
    response.status_code = 400
    response.content = request.data
    return response

# Gets a single comment JSON object
def get_comment(request, comment_id):
    response = HttpResponse()

    # Find the comment with the given comment_id
    comment = find_comment(comment_id)

    # Comment with provided id does not exist
    if not comment:
        response.status_code = 404
        response.content = "Error: Comment not found"
        return response

    # Create the JSON response dictionary
    serializer = CommentSerializer(comment)
    responseDict = serializer.data

    # Return the response
    response = JsonResponse(responseDict)
    response.status_code = 200
    return response

# Adds a new comment to an existing post
# Expects JSON request body with post and author attributes
def update_comment(request, comment_id):
    response = HttpResponse()
     # Check authorization
    payload = get_payload(request)
    if not payload:
        response.status_code = 401
        response.content = "Error: Not Authenticated"
    user_id = payload['id']

    # Find the comment with the given comment_id
    comment = find_comment(comment_id)
    if comment == None:
        response.status_code = 404
        return response
    elif str(comment.author_id) != user_id:
        response.status_code = 401
        response.content = "Error: Comment was not created by this author"
        return response
    
    # Don't allow the primary key (id) to be changed, if no request_id is provided, use the comment_id
    request_id = request.data.get("id")
    if request_id and str(request_id) != str(comment_id):
        response.status_code = 400
        response.content = "Error: Can't change id of comment"
        return response

    # Update the published time of the comment to the current time
    request.data["published"] = timezone.localtime(timezone.now())

    # Collect the request data
    serializer = CommentSerializer(partial = True, instance = comment, data=request.data)

    # If given data is valid, save the updated object to the database
    if serializer.is_valid():
        serializer.save()
        response.status_code = 200
        response.content = "Comment was succesfully updated"
        return response

    # If the data is not valid, do not save the updated object to the database
    response.status_code = 400
    response.content = "Error: Issue occurred during serialization"
    
    return response

# Deletes a comment using the provided id
def delete_comment(request, comment_id):
    response = HttpResponse()
    # Check authorization
    payload = get_payload(request)
    if not payload:
        response.status_code = 401
        response.content = "Error: Not Authenticated"
    user_id = payload['id']

    # Find the comment with the given comment_id
    comment = find_comment(comment_id)

    # Comment with provided id does not exist
    if not comment:
        response.status_code = 404
        response.content = "Error: Comment not found"
        return response
    elif str(comment.author_id) != user_id:
        response.status_code = 401
        response.content = "Error: Comment was not created by this author"
        return response

    comment.delete()
    response.status_code = 200
    response.content = "Comment was successfully deleted"
    return response

# Returns the comment object if found, otherwise returns None
def find_comment(id):
    # Find the comment with the given id
    try:
        return Comment.objects.get(id=id)
    except ObjectDoesNotExist:
        return None
