from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
import jwt
from ..models import Inbox, Author
from ..serializers import InboxSerializer, FollowRequestSerializer, PostSerializer, LikeSerializer, AuthorSerializer, CommentSerializer
from ..views import get_follower, find_post, find_author, find_comment
from .auth import get_payload

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
    viewerId = get_payload(request).get("id")
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
    viewerId = get_payload(request).get("id")
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
    viewerId = get_payload(request).get("id")
    
    # TODO: handle remote actors
    # create the follow request
    data = request.data.copy()
    data['actor'] = data.get('actor', viewerId)
    data['object'] = data.get('object', author_id)
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

    # check if author_id is following senderId, if not return unauthorized
    senderId = get_payload(request).get("id")
    if get_follower(senderId, author_id).status_code != 200 and author_id != senderId: # TODO: need to deal with remote senders 
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
    response = HttpResponse()

    # check if author_id is following senderId, if not return unauthorized
    senderId = get_payload(request).get("id")
    if get_follower(senderId, author_id).status_code != 200  and author_id != senderId: # TODO: need to deal with remote senders 
        response.status_code = 401
        return response
    
    # TODO: handle remote actors
    # create the like
    data = request.data.copy()
    data['author'] = data.get('author', senderId)

    serializer = LikeSerializer(data = data)

    if find_author(author_id) is None: 
        # If author is not found, return 404
        response.status_code = 404  
    elif serializer.is_valid():
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

    # check if author_id is following senderId, if not return unauthorized
    senderId = get_payload(request).get("id")
    if get_follower(senderId, author_id).status_code != 200  and author_id != senderId: # TODO: need to deal with remote senders 
        response.status_code = 401
        return response
    
    # find the comment
    # TODO: need to handle remote comment
    comment = find_comment(request.data["id"])
    if comment == None:
        response.status_code = 400
        return response

    # add the post to author_id's inbox
    inbox.comments.add(comment)
    response.status_code = 200
    return response