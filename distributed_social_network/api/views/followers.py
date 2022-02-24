from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from ..models import FollowRequest
from ..serializers import AuthorSerializer, FollowRequestSerializer

# Routes the request for a single follower
@api_view(['DELETE', 'PUT', 'GET'])
def route_single_follower(request, author_id, follower_id):
    if request.method == 'DELETE':
        return remove_follower(author_id, follower_id)
    elif request.method == 'PUT':
        return add_follower(author_id, follower_id)
    elif request.method == 'GET':
        return get_follower(author_id, follower_id)

# Routes the request for list of followers
@api_view(['GET'])
def route_multiple_followers(request, author_id):
    if request.method == 'GET':
        return get_followers(author_id)

# Adds author follower_id as a follower of author id 
# TODO: "must be authenticated"
def add_follower(author_id, follower_id):
    response = HttpResponse()
    # look for follow request
    try:
        fr = FollowRequest.objects.get(actor=follower_id, object=author_id)
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

# Removes author follower_id as a follower of author author_id
def remove_follower(author_id, follower_id):
    response = HttpResponse()

    try:
        fr = FollowRequest.objects.get(actor=follower_id, object=author_id)
    except ObjectDoesNotExist:
        response.status_code = 404
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
    for follower in FollowRequest.objects.filter(object=author_id).filter(accepted=True).select_related('actor'):
        follower_list.append(follower)
    
    serializer = AuthorSerializer(follower_list, many=True)
    items = serializer.data
    responseDict = {'type' : 'followers', 'items' : items}

    response = JsonResponse(responseDict)
    response.status_code = 200
    return response