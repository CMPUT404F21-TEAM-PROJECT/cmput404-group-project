from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from .models import Author
from .serializers import AuthorSerializer

# Routes the request to be deleted or updated
@api_view(['DELETE', 'PATCH'])
def change_author(request, id):
    if request.method == 'DELETE':
        return delete_author(request, id)
    elif request.method == 'PATCH':
        return update_author(request, id)

# Adds a new author to the database.
# Expects JSON request body with author attributes.
@api_view(['POST'])
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
    try:
        author = Author.objects.get(id=id)
    except ObjectDoesNotExist:
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
    try:
        author = Author.objects.get(id=id)
    except ObjectDoesNotExist:
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