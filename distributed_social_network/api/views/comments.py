from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from ..models import Comment
from ..serializers import CommentSerializer

# Routes the request for multiple comment
# Expects JSON request body with post and author attributes
@api_view(['GET', 'POST'])
def route_multiple_comments(request, post_id, author_id):
    if request.method == 'GET':
        return get_comments(request, post_id)
    elif request.method == 'POST':
        return add_comment(request, author_id, post_id)

# Routes the request for a single comment
@api_view(['GET', 'POST', 'DELETE'])
def route_single_comment(request, post_id, author_id, comment_id):
    if request.method == 'GET':
        return get_comment(request, comment_id)
    elif request.method == 'POST':
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

    # Get all comments, paginated
    comments = paginator.paginate_queryset(Comment.objects.all().filter(post_id=post_id), request)

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
    # Serialize a new Comment object
    serializer = CommentSerializer(data = request.data)
    response = HttpResponse()

    # If given data is valid, save the object to the database
    if serializer.is_valid():
        serializer.save()
        response.status_code = 201
        response.content = "New comment successfully created"
        return response
    
    response.status_code = 400
    response.content = "Error: Issue occurred during serialization"
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

    # Find the comment with the given comment_id
    comment = find_comment(comment_id)
    if comment == None:
        response.status_code = 404
        return response
    
    # Don't allow the primary key (id) to be changed
    if str(request.data.get("id")) != str(comment_id):
        response.status_code = 400
        response.content = "comment_id: {} | id: {}".format(comment_id,request.data.get("id"))
        return response

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

    # Find the comment with the given comment_id
    comment = find_comment(comment_id)

    # Comment with provided id does not exist
    if not comment:
        response.status_code = 404
        response.content = "Error: Comment not found"
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