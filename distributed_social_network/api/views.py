from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse, HttpResponse
from .models import Author, FollowRequest
from .serializers import AuthorSerializer, FollowRequestSerializer

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

# Routes the request for a single follower
@api_view(['DELETE', 'PUT', 'GET'])
def route_single_follower(request, id, f_id):
    if request.method == 'DELETE':
        return remove_follower(id, f_id)
    elif request.method == 'PUT':
        return add_follower(id, f_id)
    elif request.method == 'GET':
        return get_follower(id, f_id)

# Routes the request for list of followers
@api_view(['GET'])
def route_multiple_followers(request, id):
    if request.method == 'GET':
        return get_followers(id)

# Adds author f_id as a follower of author id 
# TODO: "must be authenticated"
def add_follower(id, f_id):
    response = HttpResponse()
    # look for follow request
    try:
        fr = FollowRequest.objects.get(actor=f_id, object=id)
    except ObjectDoesNotExist:
        response.status_code = 400
        return response
    
    if fr.accepted:
        response.status_code = 400
    # accept the follow request
    else:
        fr.accepted = True
        fr.save()
        response.status_code = 200
        return response

# Removes author f_id as a follower of author id
def remove_follower(id, f_id):
    response = HttpResponse()

    try:
        fr = FollowRequest.objects.get(actor=f_id, object=id)
    except ObjectDoesNotExist:
        response.status_code = 404
        return response

    # Delete the author
    fr.delete()
    response.status_code = 200

    return response

# Check if author f_id is a follower of author id
def get_follower(id, f_id):
    response = HttpResponse()

    try:
        fr = FollowRequest.objects.get(actor=f_id, object=id)
    except ObjectDoesNotExist:
        response.status_code = 404
        return response

    if fr.accepted:
        serializer = FollowRequestSerializer(fr) # NOTE: should we return follower instead of the follow request data?
        responseDict = serializer.data
        response = JsonResponse(responseDict)
        response.status_code = 200
        return response
    else:
        response.status_code = 404
        return response

# Get a list of author id's followers
def get_followers(id):
    response = HttpResponse()

    # find accepted friend requests
    follower_list = []
    for follower in FollowRequest.objects.filter(object=id).filter(accepted=True).select_related('actor'):
        follower_list.append(follower)
    
    serializer = AuthorSerializer(follower_list, many=True)
    items = serializer.data
    responseDict = {'type' : 'followers', 'items' : items}

    response = JsonResponse(responseDict)
    response.status_code = 200
    return response
