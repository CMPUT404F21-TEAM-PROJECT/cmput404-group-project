from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from ..serializers import AuthorSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from ..models import Author
import requests, environ

env = environ.Env()
environ.Env.read_env()

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
        return Author.objects.get(id=env("LOCAL_HOST") + "/authors/" + id + "/")
    except ObjectDoesNotExist:
        return None

# Returns a string of the UUID given an author's id
def get_uuid_from_id(id):
    # assumes all ids follow this format: http://host/authors/uuid
    parts = id.split('/')
    uuid = parts[-1] if parts[-1] else parts[-2]
    return uuid

# Returns the author object if found, otherwise creates the author
# Returns None if unable to create author
# This will be used to create local copies of remote authors
def find_or_create_author(id):
    uuid = get_uuid_from_id(id)
    author = find_author(uuid)
    if not author:
        # request to get author details from remote server
        response = requests.get(id)
        if response.status_code != 200:
            return None

        response_data = response.json()
        response_data['id'] = uuid
        # TODO: Add some validation to make sure response_data['host'] is in our list of accepted nodes
        #       otherwise do not create the author and return None
        serializer = AuthorSerializer(data = response_data)

        # If given data is valid, save the object to the database
        if serializer.is_valid():
            return serializer.save()
        else:
            author = None
    
    return author
    