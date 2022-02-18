from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse, HttpResponse
from .models import Author, Post
from .serializers import AuthorSerializer, PostSerializer

# Routes the request for a single author
@api_view(['DELETE', 'PATCH', 'GET'])
def route_single_author(request, id):
    if request.method == 'DELETE':
        return delete_author(request, id)
    elif request.method == 'PATCH':
        return update_author(request, id)
    elif request.method == 'GET':
        return get_single_author(request, id)

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
def route_single_post(request, id):
    if request.method == 'GET':
        return get_post(request, id)
    elif request.method == 'POST':
        return update_post(request, id)
    elif request.method == 'DELETE':
        return delete_post(request, id)
    elif request.method == 'PUT':
        return create_post(request, id)

# Routes the request for multiple posts
@api_view(['POST', 'GET'])
def route_multiple_posts(request):
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