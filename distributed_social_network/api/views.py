from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse, HttpResponse
from .models import Author, Post, Comment

from .serializers import AuthorSerializer, CommentSerializer, PostSerializer

# Routes the request for a single author
@api_view(['DELETE', 'POST', 'GET'])
def route_single_author(request, author_id):
    if request.method == 'DELETE':
        return delete_author(request, author_id)
    elif request.method == 'POST':
        return update_author(request, author_id)
    elif request.method == 'GET':
        return get_single_author(request, author_id)

# Routes the request for multiple authors
@api_view(['POST', 'GET'])
def route_multiple_authors(request):
    if request.method == 'POST':
        return add_author(request)
    elif request.method == 'GET':
        return get_multiple_authors(request)

# Adds a new author to the database.
# Expects JSON request body with author attributes.
def add_author(request):
    # Serialize a new Author object
    serializer = AuthorSerializer(data = request.data)

    response = HttpResponse()

    # If given data is valid, save the object to the database
    if serializer.is_valid():
        serializer.save()
        response.status_code = 201
        return response

    # If the data is not valid, do not save the object to the database
    response.status_code = 400
    return response

# Deletes the author with id 'id' from the database.
def delete_author(request, id):
    response = HttpResponse()

    # Find the author with the given id
    author = find_author(id)
    if author == None:
        response.status_code = 404
        return response

    # Delete the author
    author.delete()
    response.status_code = 200

    return response

# Updates the author with id 'id' in the database.
def update_author(request, id):
    response = HttpResponse()

    # Find the author with the given id
    author = find_author(id)
    if author == None:
        response.status_code = 404
        return response
    
    # Don't allow the primary key (id) to be changed
    if request.data.get("id") != id:
        response.status_code = 400
        return response

    # Collect the request data
    serializer = AuthorSerializer(partial = True, instance = author, data=request.data)

    # If given data is valid, save the updated object to the database
    if serializer.is_valid():
        serializer.save()
        response.status_code = 200
        return response

    # If the data is not valid, do not save the updated object to the database
    response.status_code = 400
    return response

# Get the author with id 'id' in the database
def get_single_author(request, id):
    response = HttpResponse()

    # Find the author with the given id
    author = find_author(id)
    if author == None:
        response.status_code = 404
        return response
    
    # Create the JSON response dictionary
    serializer = AuthorSerializer(author)
    responseDict = serializer.data

    # Return the response
    response = JsonResponse(responseDict)
    response.status_code = 200
    return response

# Get all authors
def get_multiple_authors(request):
    # Initialize paginator
    paginator = PageNumberPagination()
    paginator.page_query_param = 'page'
    paginator.page_size_query_param = 'size'

    # Get all authors, paginated
    authors = paginator.paginate_queryset(Author.objects.all(), request)

    # Create the JSON response dictionary
    serializer = AuthorSerializer(authors, many=True)
    items = serializer.data
    responseDict = {'type' : 'authors', 'items' : items}

    # Return the response
    response = JsonResponse(responseDict)
    response.status_code = 200
    return response

# Returns the author object if found, otherwise returns None
def find_author(id):
    # Find the author with the given id
    try:
        return Author.objects.get(id=id)
    except ObjectDoesNotExist:
        return None

# Routes the request for a single post
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def route_single_post(request, author_id, post_id):
    if request.method == 'GET':
        return get_post(request, post_id)
    elif request.method == 'POST':
        return update_post(request, post_id)
    elif request.method == 'DELETE':
        return delete_post(request, post_id)
    elif request.method == 'PUT':
        return create_post(request, post_id)

# Routes the request for multiple posts
@api_view(['POST', 'GET'])
def route_multiple_posts(request, author_id):
    if request.method == 'POST':
        return create_post(request)
    elif request.method == 'GET':
        return get_multiple_posts(request)

# Adds a new post to the database.
# Expects JSON request body with post attributes.
def create_post(request):
    # Serialize a new Post object
    serializer = PostSerializer(data = request.data)

    response = HttpResponse()

    # If given data is valid, save the object to the database
    if serializer.is_valid():
        serializer.save()
        response.status_code = 201
        return response

    # If the data is not valid, do not save the object to the database
    response.status_code = 400
    return response

# Deletes the post with id 'id' from the database.
def delete_post(request, id):
    response = HttpResponse()

    # Find the post with the given id
    post = find_post(id)
    if post == None:
        response.status_code = 404
        return response

    # Delete the post
    post.delete()
    response.status_code = 200

    return response

# Updates the post with id 'id' in the database.
def update_post(request, id):
    response = HttpResponse()

    # Find the post with the given id
    post = find_post(id)
    if post == None:
        response.status_code = 404
        return response

    # Collect the request data
    serializer = PostSerializer(partial = True, instance = post, data=request.data)

    # If given data is valid, save the updated object to the database
    if serializer.is_valid():
        serializer.save()
        response.status_code = 200
        return response

    # If the data is not valid, do not save the updated object to the database
    response.status_code = 400
    return response

# Get the post with id 'id' in the database
def get_post(request, id):
    response = HttpResponse()

    # Find the post with the given id
    post = find_post(id)
    if post == None:
        response.status_code = 404
        return response
    
    # Create the JSON response dictionary
    serializer = PostSerializer(post)
    responseDict = serializer.data

    # Return the response
    response = JsonResponse(responseDict)
    response.status_code = 200
    return response

# Get all posts
def get_multiple_posts(request):
    # Initialize paginator
    paginator = PageNumberPagination()
    paginator.page_query_param = 'page'
    paginator.page_size_query_param = 'size'

    # Get all posts, paginated
    posts = paginator.paginate_queryset(Post.objects.all(), request)

    # Create the JSON response dictionary
    serializer = PostSerializer(posts, many=True)
    items = serializer.data
    responseDict = {'type' : 'posts', 'items' : items}

    # Return the response
    response = JsonResponse(responseDict)
    response.status_code = 200
    return response

# Returns the post object if found, otherwise returns None
def find_post(id):
    # Find the post with the given id
    try:
        return Post.objects.get(id=id)
    except ObjectDoesNotExist:
        return None

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