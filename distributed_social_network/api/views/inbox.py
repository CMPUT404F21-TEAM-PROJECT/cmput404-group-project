from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
import jwt
from ..models import Inbox, Author
from ..serializers import InboxSerializer, FollowRequestSerializer, PostSerializer
from ..views import get_follower, find_post

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

# Routes the request for inbox
@api_view(['GET', 'POST', 'DELETE'])
def route_inbox(request, author_id):
    response = HttpResponse()
    try:
        inbox = Inbox.objects.get(author=author_id)
    except ObjectDoesNotExist:
        response.status_code = 404
        return response

    if request.method == 'GET':
        return get_inbox(request, author_id, inbox)

    elif request.method == 'POST':
        object_type = request.data['type'].lower()
        if object_type == 'post':
            return add_post(request, author_id, inbox)
        elif object_type == 'like':
            return add_like(request, author_id, inbox)
        elif object_type == 'follow':
            return add_follow(request, author_id, inbox)
        else:
            response.status_code = 400
            return response

    elif request.method == 'DELETE':
        return delete_inbox(request, author_id, inbox)

# Get author_id's inbox
def get_inbox(request, author_id, inbox):
    # Check authorization
    try:
        cookie = request.COOKIES['jwt']
        viewerId = jwt.decode(cookie, key='secret', algorithms=['HS256'])["id"]
        if not (str(inbox.author.id.id) == viewerId):
            response.status_code = 401
            return response
    except KeyError:
        response.status_code = 401
        return response
    
    # get all posts, likes and follow request sent to inbox
    serializer = InboxSerializer(inbox)
    items = []
    data = serializer.data
    for post in data['posts']:
        items.append(post)
    # for like in data['likes']:
    #     items.append(likes)
    for fr in data['follow_requests']:
        items.append(fr)
    
    # TODO: make sure pagination works as expected
    # initialize paginator
    paginator = PageNumberPagination()
    paginator.page_query_param = 'page'
    paginator.page_size_query_param = 'size'

    # paginate all objects in inbox
    paginated_items = paginator.paginate_queryset(items, request)

    data.pop('posts')
    # data.pop('likes')
    data.pop('follow_requests')
    data['items'] = paginated_items 

    response = JsonResponse(data)
    response.status_code = 200
    return response

def delete_inbox(request, author_id, inbox):
    response = HttpResponse()

    # Check authorization
    try:
        cookie = request.COOKIES['jwt']
        viewerId = jwt.decode(cookie, key='secret', algorithms=['HS256'])["id"]
        if not (str(inbox.author.id.id) == viewerId):
            response.status_code = 401
            return response
    except KeyError:
        response.status_code = 401
        return response
    
    inbox.posts.clear()
    # inbox.likes.clear()
    inbox.follow_requests.clear()
    response.status_code = 200

    return response

# Create a follow request and add it to author_id's inbox
def add_follow(request, author_id, inbox):
    # get the viewer (person who sent the follow request)
    try:
        cookie = request.COOKIES['jwt']
        viewerId = jwt.decode(cookie, key='secret', algorithms=['HS256'])["id"]
    except KeyError:
        response.status_code = 401
        return response
    
    # TODO: handle remote actors
    # create the follow request
    data = request.data.copy()
    data['actor'] = viewerId
    data['object'] = author_id
    serializer = FollowRequestSerializer(data = data)
    response = HttpResponse()

    # If given data is valid, save the follow request to the database
    if serializer.is_valid():
        fr = serializer.save()
        # add the follow request to author_id's inbox
        inbox.follow_requests.add(fr)
        response.status_code = 201
        return response

    print(serializer.errors)
    response.status_code = 400
    return response

# Get the post and add it to author_id's inbox
def add_post(request, author_id, inbox):
    response = HttpResponse()

    # check if author_id is following senderId, if not return unauthorized
    try:
        cookie = request.COOKIES['jwt']
        senderId = jwt.decode(cookie, key='secret', algorithms=['HS256'])["id"]
        if get_follower(senderId, author_id).status_code != 200: # TODO: need to deal with remote senders 
            response.status_code = 401
            return response
    except KeyError:
        response.status_code = 401
        return response
    
    # find the post
    # TODO: need to handle remote posts
    post = find_post(request.data["id"])
    if post == None:
        response.status_code = 400
        return response

    # add the post to author_id's inbox
    inbox.posts.add(post)
    response.status_code = 200
    return response

# Create a like and add it to author_id's inbox
def add_like(request, author_id, inbox):
    pass