from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from ..models import FollowRequest, Author
from ..serializers import AuthorSerializer, FollowRequestSerializer
from .auth import get_payload

# Routes the request for a single follower
@api_view(['DELETE', 'PUT', 'GET'])
def route_single_follower(request, author_id, follower_id):
    if request.method == 'DELETE':
        return remove_follower(request, author_id, follower_id)
    elif request.method == 'PUT':
        return add_follower(request, author_id, follower_id)
    elif request.method == 'GET':
        return get_follower(author_id, follower_id)

# Routes the request for list of followers
@api_view(['GET'])
def route_multiple_followers(request, author_id):
    if request.method == 'GET':
        return get_followers(author_id)

# Routes the request for list of following
@api_view(['GET'])
def route_multiple_following(request, author_id):
    if request.method == 'GET':
        return get_following(author_id)

# Adds author follower_id as a follower of author id
def add_follower(request, author_id, follower_id):
    response = HttpResponse()

    # Check authorization
    viewerId = get_payload(request).get("id")
    if not (author_id == viewerId):
        response.status_code = 401
        return response

    # look for follow request
    try:
        fr = FollowRequest.objects.get(actor=follower_id, object=author_id)
    except ObjectDoesNotExist:
        response.status_code = 404
        return response
    
    if fr.accepted:
        response.status_code = 400
    # accept the follow request
    else:
        fr.accepted = True
        fr.save()
        response.status_code = 200
        return response

# Removes author follower_id as a follower of author author_id
def remove_follower(request, author_id, follower_id):
    response = HttpResponse()

    # Check authorization
    viewerId = get_payload(request).get("id")
    if not (author_id == viewerId or follower_id == viewerId):
        response.status_code = 401
        return response

    try:
        fr = FollowRequest.objects.get(actor=follower_id, object=author_id)  
    except ObjectDoesNotExist:
        response.status_code = 400
        return response

    # delete the follow request
    fr.delete()
    response.status_code = 200

    return response

# Check if author follower_id is a follower of author author_id
def get_follower(author_id, follower_id):
    response = HttpResponse()

    try:
        fr = FollowRequest.objects.get(actor=follower_id, object=author_id)
    except ObjectDoesNotExist:
        response.status_code = 404
        return response

    if fr.accepted:
        serializer = FollowRequestSerializer(fr) # NOTE: should we return follower instead of the follow request data?
        responseDict = serializer.data
        responseDict['actor'] = AuthorSerializer(Author.objects.get(id=responseDict['actor'])).data
        responseDict['object'] = AuthorSerializer(Author.objects.get(id=responseDict['object'])).data
        response = JsonResponse(responseDict)
        response.status_code = 200
        return response
    else:
        response.status_code = 404
        return response

# Get a list of author author_id's followers
def get_followers(author_id):
    response = HttpResponse()

    # find accepted friend requests
    follower_list = []
    for fr in FollowRequest.objects.filter(object=author_id).filter(accepted=True):
        follower_list.append(fr.actor)
    
    serializer = AuthorSerializer(follower_list, many=True)
    items = serializer.data
    responseDict = {'type' : 'followers', 'items' : items}

    response = JsonResponse(responseDict)
    response.status_code = 200
    return response

# Get a list of people who author author_id is following
def get_following(author_id):
    response = HttpResponse()

    # find accepted friend requests
    follower_list = []
    for fr in FollowRequest.objects.filter(actor=author_id).filter(accepted=True):
        follower_list.append(fr.object)
    
    serializer = AuthorSerializer(follower_list, many=True)
    items = serializer.data
    responseDict = {'type' : 'following', 'items' : items}

    response = JsonResponse(responseDict)
    response.status_code = 200
    return response