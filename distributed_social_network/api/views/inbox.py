from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
import jwt
from ..models import Inbox, Author, Post, Comment
from ..serializers import InboxSerializer, FollowRequestSerializer, PostSerializer, LikeSerializer, AuthorSerializer, CommentSerializer
from ..views import get_follower, find_post, find_author, find_comment
from .auth import get_payload

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
import environ
import requests
from ..util import getAuthHeaderForNode

env = environ.Env()
environ.Env.read_env()

# Routes the request for inbox
@api_view(['GET', 'POST', 'DELETE'])
def route_inbox(request, author_id):
    author_id = env("LOCAL_HOST") + "/authors/" + author_id
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
        elif object_type == 'comment':
            return add_comment(request, author_id, inbox)
        else:
            response.status_code = 400
            return response

    elif request.method == 'DELETE':
        return delete_inbox(request, author_id, inbox)

# Get author_id's inbox
def get_inbox(request, author_id, inbox):
    response = HttpResponse()

    # Check authorization
    viewerId = get_payload(request, False).get("id")
    if not (author_id == viewerId):
        response.status_code = 401
        return response
    
    # get all posts, likes and follow request sent to inbox
    serializer = InboxSerializer(inbox)
    items = []
    data = serializer.data
    for post in data['posts']:
        post['author'] = AuthorSerializer(Author.objects.get(id=post['author'])).data
        items.append(post)
    for like in data['likes']:
        like['author'] = AuthorSerializer(Author.objects.get(id=like['author'])).data
        items.append(like)
    for fr in data['follow_requests']:
        fr['actor'] = AuthorSerializer(Author.objects.get(id=fr['actor'])).data
        fr['object'] = AuthorSerializer(Author.objects.get(id=fr['object'])).data
        items.append(fr)
    for comment in data['comments']:
        comment['author'] = AuthorSerializer(Author.objects.get(id=comment['author'])).data
        items.append(comment)
    
    # TODO: make sure pagination works as expected
    # initialize paginator
    paginator = PageNumberPagination()
    paginator.page_query_param = 'page'
    paginator.page_size_query_param = 'size'

    # paginate all objects in inbox
    paginated_items = paginator.paginate_queryset(items, request)

    data.pop('posts')
    data.pop('likes')
    data.pop('follow_requests')
    data.pop('comments')
    data['items'] = paginated_items 

    response = JsonResponse(data)
    response.status_code = 200
    return response

def delete_inbox(request, author_id, inbox):
    response = HttpResponse()

    # Check authorization
    viewerId = get_payload(request, False).get("id")
    if not (author_id == viewerId):
        response.status_code = 401
        return response
    
    inbox.posts.clear()
    inbox.likes.clear()
    inbox.follow_requests.clear()
    inbox.comments.clear()
    response.status_code = 200

    return response

# Create a follow request and add it to author_id's inbox
def add_follow(request, author_id, inbox):
    response = HttpResponse()

    # get person who sent the follow request
    viewerId = get_payload(request, True).get("id")
    
    # create the follow request
    data = request.data.copy()
    data['actor'] = data.get('actor', viewerId)
    data['object'] = data.get('object', author_id)

    # remote actor
    if viewerId == 'foreign':
        actorId = data['actor']
        # remote actor didn't include actor field in request
        if actorId == 'foreign':
            response.status_code = 400
            return response
        
        actor = find_or_create_author(actorId)
        # unable to create local copy of remote actor
        if not actor:
            response.status_code = 400
            return response
        data['actor'] = actor.id

    serializer = FollowRequestSerializer(data = data)

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
    senderId = get_payload(request, True).get("id")
    data = request.data.copy()

    # remote sender
    if senderId == 'foreign':
        senderId = data.get('author', senderId)
        if senderId != 'foreign' and type(senderId) != type("") and senderId.get('id', None) != None:
            senderId = senderId.get('id')
        # didn't include author field in request
        if senderId == 'foreign':
            response.status_code = 400
            return response
        
        sender = find_or_create_author(senderId)
        # unable to create local copy of remote sender
        if not sender:
            response.status_code = 400
            return response
        
        # check if authord_id is following senderId
        # author = find_author(author_id)
        # follower_response = requests.get(f'{sender.id}/followers/{author.id}')
        # if follower_response.code != 200: # TODO: verify expected response with other teams
        #     response.status_code = 400
        #     return response
        senderId = sender.id

    # not a remote sender, check if author_id is following senderId
    elif get_follower(senderId, author_id).status_code != 200 and author_id != senderId:
        response.status_code = 401
        return response
    
    # find the post
    post = find_or_create_post(data["id"], senderId)
    if post == None:
        response.status_code = 400
        return response

    # add the post to author_id's inbox
    inbox.posts.add(post)
    response.status_code = 200
    return response

# Create a like and add it to author_id's inbox
def add_like(request, author_id, inbox):
    response = HttpResponse()
    data = request.data.copy()
    senderId = get_payload(request, True).get("id")
    data['author'] = data.get('author', senderId)

    # remote sender
    if senderId == 'foreign':
        # didn't include author field in request
        if data['author'] == 'foreign': 
            response.status_code = 400
            return response
        
        sender = find_or_create_author(data['author'])
        # unable to create local copy of remote actor
        if not sender:
            response.status_code = 400
            return response
        
        # check if authord_id is following senderId
        # author = find_author(author_id)
        # follower_response = requests.get(f'{sender.id}/followers/{author.id}')
        # if follower_response.code != 200: # TODO: verify expected response with other teams
        #     response.status_code = 400
        #     return response

    # not a remote sender, check if author_id is following senderId
    elif get_follower(senderId, author_id).status_code != 200 and author_id != senderId:
        response.status_code = 401
        return response

    serializer = LikeSerializer(data = data)

    if serializer.is_valid():
        # If given data is valid, save the object to the database
        like = serializer.save()
        response.status_code = 201
        inbox.likes.add(like)
    else:
        print(serializer.errors)
        # If the data is not valid, do not save the object to the database
        response.status_code = 400

    return response

# Create a comment and add it to author_id's inbox
def add_comment(request, author_id, inbox):
    response = HttpResponse()
    senderId = get_payload(request, True).get("id")
    data = request.data.copy()

    # remote sender
    if senderId == 'foreign':
        senderId = data.get('author', senderId)
        # didn't include author field in request
        if senderId == 'foreign':
            response.status_code = 400
            return response
        
        sender = find_or_create_author(senderId)
        # unable to create local copy of remote sender
        if not sender:
            response.status_code = 400
            return response
        
        # check if authord_id is following senderId
        
        #author = find_author(author_id)
        #follower_response = requests.get(f'{sender.id}/followers/{author.id}')
        #if follower_response.code != 200: # TODO: verify expected response with other teams
        #    response.status_code = 400
        #    return response
        
    # not a remote sender, check if author_id is following senderId
    elif get_follower(senderId, author_id).status_code != 200 and author_id != senderId:
        response.status_code = 401
        return response

    # find the comment
    comment = find_or_create_comment(data["id"])
    if comment == None:
        response.status_code = 400
        return response

    # add the comment to author_id's inbox
    inbox.comments.add(comment)
    response.status_code = 200
    return response

# Returns the author object if found, otherwise creates the author
# Returns None if unable to create author
# This will be used to create local copies of remote authors
def find_or_create_author(id):
    if ("http://" not in id) and ("https://" not in id):
        id = "http://tik-tak-toe-cmput404.herokuapp.com/authors/" + id
    
    try:
        author = Author.objects.get(id=id)
    except ObjectDoesNotExist:
        # request to get author details from remote server
        response = requests.get(id, auth=getAuthHeaderForNode(id))
        if response.status_code != 200:
            return None

        response_data = response.json()
        response_data.pop("type")
        # TODO: Add some validation to make sure response_data['host'] is in our list of accepted nodes
        #       otherwise do not create the author and return None
        serializer = AuthorSerializer(data = response_data)

        # If given data is valid, save the object to the database
        if serializer.is_valid():
            return serializer.save()
        else:
            return None
    else:
        return author

# Returns the comment object if found, otherwise creates the comment
# Returns None if unable to create comment
# This will be used to create local copies of remote comments
def find_or_create_comment(id):
    try:
        return Comment.objects.get(id=id)
    except ObjectDoesNotExist:
        # request to get comment details from remote server
        response = requests.get(id, auth=getAuthHeaderForNode(id))
        if response.status_code != 200:
            return None

        response_data = response.json()
        response_data.pop("type")
        # TODO: Add some validation to make sure response_data['host'] is in our list of accepted nodes
        #       otherwise do not create the author and return None
        serializer = CommentSerializer(data = response_data)

        # If given data is valid, save the object to the database
        if serializer.is_valid():
            return serializer.save()
        else:
            return None

# Returns the post object if found, otherwise creates the post
# Returns None if unable to create post
# This will be used to create local copies of remote posts
def find_or_create_post(id, authorId):
    try:
        if ("http://" not in id) and ("https://" not in id):
            id = authorId + "/posts/" + id
        return Post.objects.get(id=id)
    except ObjectDoesNotExist:
        # request to get post details from remote server
        response = requests.get(id, auth=getAuthHeaderForNode(id))
        if response.status_code != 200:
            return None

        response_data = response.json()
        # clean input
        response_data.pop("type")
        if response_data.get('source', None) == '':
            response_data.pop('source')
        if response_data.get('origin', None) == '':
            response_data.pop('origin')

        response_data['viewableBy'] = ''
        # TODO: Add some validation to make sure response_data['host'] is in our list of accepted nodes
        #       otherwise do not create the author and return None
        serializer = PostSerializer(data = response_data)

        # If given data is valid, save the object to the database
        if serializer.is_valid():
            return serializer.save()
        else:
            return None
