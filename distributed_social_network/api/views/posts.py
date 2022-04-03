from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse

from api.util import getAuthHeaderForNode
from ..serializers import PostSerializer, AuthorSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
import base64, jwt, uuid, environ
from .auth import get_payload
from ..models import FollowRequest, Post, Author, Node
from django.db.models import Q
from itertools import chain
import requests

env = environ.Env()
environ.Env.read_env()

# Routes the request for a single post
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def route_single_post(request, author_id, post_id):
    if request.method == 'GET':
        return get_post(request, author_id, post_id)
    elif request.method == 'POST':
        return update_post(request, author_id, post_id)
    elif request.method == 'DELETE':
        return delete_post(request, author_id, post_id)
    elif request.method == 'PUT':
        return create_post_with_id(request, post_id)

# Routes the request for multiple posts
@api_view(['POST', 'GET'])
def route_multiple_posts(request, author_id):
    if request.method == 'POST':
        return create_post(request, author_id)
    elif request.method == 'GET':
        return get_multiple_posts(request, author_id)

# Routes the request for public posts
@api_view(['GET'])
def route_public_posts(request):
    return get_public_posts(request)

# Routes the request for a single image post
@api_view(['GET'])
def route_single_image_post(request, author_id, post_id):
    if request.method == 'GET':
        return get_post_image(request, author_id, post_id)

# Adds a new post to the database.
# Generates a new id for the post
def create_post(request, author_id):   
    # Generate a new id
    post_id = request.data["author"] + "/posts/" + str(uuid.uuid4())
    # If id already exists make a new one
    while get_post(request, author_id, post_id).status_code == 200:
        post_id = request.data["author"] + "/posts/" + str(uuid.uuid4())
    return create_post_with_id(request, post_id)

# Adds a new post to the database.
# Expects JSON request body with post attributes.
def create_post_with_id(request, id):
    # Use the given id
    if env("LOCAL_HOST") in id:
        request.data["id"] = id
    else:
        request.data["id"] = request.data["author"] + "/posts/" + id
    if not request.data['viewableBy']:
        request.data['viewableBy'] = ''
    response = HttpResponse()

    # Check authorization
    try:
        token = request.COOKIES.get('jwt')
        # Request was not authenticated without a token
        if not token:
            token = request.headers['Authorization']
            if not token:
                response.status_code = 401
                return response
        creatorId = jwt.decode(token, key='secret', algorithms=['HS256'])["id"]
        if not (str(request.data['author']) == creatorId):
            response.status_code = 401
            return response
    except KeyError:
        response.status_code = 401
        return response
    
    # Serialize a new Post object
    serializer = PostSerializer(data = request.data)

    # If given data is valid, save the object to the database
    if serializer.is_valid():
        serializer.save()
        # Return the created post
        responseDict = serializer.data
        responseDict['author'] = AuthorSerializer(Author.objects.get(id=responseDict['author'])).data
        response = JsonResponse(responseDict)
        response.status_code = 201
        return response
    print(serializer.errors)

    # If the data is not valid, do not save the object to the database
    response.status_code = 400
    return response

# Deletes the post with id 'id' from the database.
def delete_post(request, authorId, id):
    response = HttpResponse()

    # Find the post with the given id
    post = find_post(id, authorId)
    if post == None:
        response.status_code = 404
        return response

    # Check authorization
    try:
        token = request.COOKIES.get('jwt')
        # Request was not authenticated without a token
        if not token:
            token = request.headers['Authorization']
            if not token:
                response.status_code = 401
                return response
        deleterId = jwt.decode(token, key='secret', algorithms=['HS256'])["id"]
        if not (str(post.author_id) == deleterId):
            response.status_code = 401
            return response
    except KeyError:
        response.status_code = 401
        return response

    # Delete the post
    post.delete()
    response.status_code = 200

    return response

# Updates the post with id 'id' in the database.
def update_post(request, authorId, id):
    response = HttpResponse()

    # Use the given id
    if env("LOCAL_HOST") in id:
        request.data["id"] = id
    else:
        request.data["id"] = request.data["author"] + "/posts/" + id

    # Find the post with the given id
    post = find_post(id, authorId)
    if post == None:
        response.status_code = 404
        return response

    # Check authorization
    try:
        token = request.COOKIES.get('jwt')
        # Request was not authenticated without a token
        if not token:
            token = request.headers['Authorization']
            if not token:
                response.status_code = 401
                return response
        updaterId = jwt.decode(token, key='secret', algorithms=['HS256'])["id"]
        if not (str(post.author_id) == updaterId):
            response.status_code = 401
            return response
    except KeyError:
        response.status_code = 401
        return response

    # Collect the request data
    serializer = PostSerializer(partial = True, instance = post, data=request.data)

    # If given data is valid, save the updated object to the database
    if serializer.is_valid():
        serializer.save()
        # Return the created post
        responseDict = serializer.data
        responseDict['author'] = AuthorSerializer(Author.objects.get(id=responseDict['author'])).data
        response = JsonResponse(responseDict)
        response.status_code = 201
        return response

    # If the data is not valid, do not save the updated object to the database
    response.status_code = 400
    return response

# Get the post with id 'id' in the database
def get_post(request, authorId, id):
    response = HttpResponse()

    # Find the post with the given id
    post = find_post(id, authorId)
    if post == None:
        response.status_code = 404
        return response
    authorId = post.author_id

    # Check if the current user is from foreign node
    foreign = False
    payload = get_payload(request, True)
    if payload != None and payload.get("id") == "foreign":
        foreign = True

    # Check if the post is friends only
    if post.visibility == "FRIENDS":
        # Deny access to foreign node users
        if foreign:
            response.status_code = 401
            return response

        # Check if the current user is a friend of the author
        try:
            token = request.COOKIES.get('jwt')
            # Request was not authenticated without a token
            if not token:
                token = request.headers['Authorization']
                if not token:
                    response.status_code = 401
                    return response
            viewerId = uuid.UUID(jwt.decode(token, key='secret', algorithms=['HS256'])["id"])
            followRequests = FollowRequest.objects.filter(Q(actor__exact=authorId) | Q(object__exact=authorId)).filter(accepted__exact=True).filter(Q(actor__exact=viewerId) | Q(object__exact=viewerId))
            if len(followRequests) <= 0:
                response.status_code = 401
                return response
        except KeyError:
            response.status_code = 401
            return response

    # Check if post is viewable by single author only
    if post.viewableBy != '':
        # Deny access to foreign node users
        if foreign:
            response.status_code = 401
            return response

        try:
            token = request.COOKIES.get('jwt')
            # Request was not authenticated without a token
            if not token:
                token = request.headers['Authorization']
                if not token:
                    response.status_code = 401
                    return response
            viewerId = uuid.UUID(jwt.decode(token, key='secret', algorithms=['HS256'])["id"])
            try:
                viewableBy = uuid.UUID(post.viewableBy)
            except:
                viewableBy = None
            if viewerId != viewableBy and viewerId != post.author_id:
                response.status_code = 401
                return response
        except KeyError:
            response.status_code = 401
            return response
    
    # Create the JSON response dictionary
    serializer = PostSerializer(post)
    responseDict = serializer.data
    responseDict['author'] = AuthorSerializer(Author.objects.get(id=responseDict['author'])).data

    # Return the response
    response = JsonResponse(responseDict)
    response.status_code = 200
    return response

# Get all public posts that are viewable by the currently authenticated author
def get_public_posts(request):
    # Get all public posts that are not unlisted
    publicPosts = Post.objects.filter(visibility__exact="PUBLIC").filter(unlisted__exact=False).filter(viewableBy__exact='')

    # Get all public posts from foreign nodes
    nodes = Node.objects.all()

    # loop over each node
    foreignPublicPosts = []
    for node in nodes:
        auth = getAuthHeaderForNode(node.baseUrl)
        try:
            response = requests.get(node.baseUrl + "/authors/", auth=auth, timeout=3)
            authors = response.json().get("items")

            # loop over each author
            for author in authors:
                authorId = author['id']
                
                # convert to url if needed
                if "http://" not in authorId and "https://" not in authorId:
                    authorId = node.baseUrl + "/authors/" + authorId

                # get all posts by that author
                try:
                    response = requests.get(authorId + "/posts/", auth=auth, timeout=0.3)
                    posts = response.json().get('items')
                    foreignPublicPosts = foreignPublicPosts + posts
                except Exception as e:
                    print(e)
                    print("Get request failed at " + authorId + "/posts/")
        except Exception as e:
            print(e)
            print("Get request failed at " + node.baseUrl + "/authors/")

    # Initialize paginator
    paginator = PageNumberPagination()
    paginator.page_query_param = 'page'
    paginator.page_size_query_param = 'size'

    posts = paginator.paginate_queryset(list(chain(publicPosts)), request)

    # Create the JSON response dictionary
    serializer = PostSerializer(posts, many=True)
    items = serializer.data
    for post in items:
        post['author'] = AuthorSerializer(Author.objects.get(id=post['author'])).data

    items = items + foreignPublicPosts
    responseDict = {'type' : 'posts', 'items' : items}

    # Return the response
    response = JsonResponse(responseDict)
    response.status_code = 200
    return response

# Get all posts written by author_id given as an argument, that are viewable by the currently authenticated author
def get_multiple_posts(request, author_id):
    author_id = env("LOCAL_HOST") + "/authors/" + author_id
    # Get all public posts that are not unlisted
    publicPosts = Post.objects.filter(author__exact=author_id).filter(visibility__exact="PUBLIC").filter(unlisted__exact=False).filter(viewableBy__exact='')

    friendsPosts = []
    privatePosts = []

    # Check if the current user is from foreign node
    permissionForAny = False
    foreign = False
    payload = get_payload(request, True)
    if payload != None and payload.get("id") == "foreign":
        foreign = True

    # Get the current user id
    if not foreign and payload != None:
        try:
            token = request.COOKIES.get('jwt')
            # Request was not authenticated without a token
            if not token:
                token = request.headers['Authorization']
                if not token:
                    permissionForAny = False
                else:
                    viewerId = jwt.decode(token, key='secret', algorithms=['HS256'])["id"]

                    # Get all friends only posts that are not unlisted
                    friendsPosts = Post.objects.filter(visibility__exact="FRIENDS").filter(unlisted__exact=False)
                    privatePosts = Post.objects.filter(~Q(viewableBy__exact='')).filter(unlisted__exact=False)
                    permissionForAny = True
            else:
                viewerId = jwt.decode(token, key='secret', algorithms=['HS256'])["id"]

                # Get all friends only posts that are not unlisted
                friendsPosts = Post.objects.filter(visibility__exact="FRIENDS").filter(unlisted__exact=False)
                privatePosts = Post.objects.filter(~Q(viewableBy__exact='')).filter(unlisted__exact=False)
                permissionForAny = True
        except KeyError:
            permissionForAny = False

        if permissionForAny:
            # Loop over friends posts
            allowedFriendsPosts = []
            for post in friendsPosts:
                # Check if the current user is a friend of the author
                followRequests = FollowRequest.objects.filter(Q(actor__exact=post.author_id) | Q(object__exact=post.author_id)).filter(accepted__exact=True).filter(Q(actor__exact=viewerId) | Q(object__exact=viewerId))
                if len(followRequests) > 0:
                    allowedFriendsPosts.append(post)
            
            # Loop over private posts
            allowedPrivatePosts = []
            for post in privatePosts:
                # Check if the current user is the viewableBy user
                try:
                    viewableBy = uuid.UUID(post.viewableBy)
                except:
                    viewableBy = None
                if viewableBy == viewerId or post.author_id == viewerId:
                    allowedPrivatePosts.append(post)

    # Initialize paginator
    paginator = PageNumberPagination()
    paginator.page_query_param = 'page'
    paginator.page_size_query_param = 'size'

    # Get posts, paginated
    if permissionForAny and not foreign:
        posts = paginator.paginate_queryset(list(chain(publicPosts, allowedFriendsPosts, allowedPrivatePosts)), request)
    else:
        posts = paginator.paginate_queryset(list(chain(publicPosts)), request)

    # Create the JSON response dictionary
    serializer = PostSerializer(posts, many=True)
    items = serializer.data
    for post in items:
        post['author'] = AuthorSerializer(Author.objects.get(id=post['author'])).data
    responseDict = {'type' : 'posts', 'items' : items, 'count': len(list(chain(publicPosts)))}

    # Return the response
    response = JsonResponse(responseDict)
    response.status_code = 200
    return response

# Get the image post with id 'id' in the database and return a binary response
def get_post_image(request, authorId, id):
    response = HttpResponse()

    # Find the post with the given id
    post = find_post(id, authorId)
    if post == None:
        response.status_code = 404
        return response
    authorId = post.author_id

    # Check if the current user is from foreign node
    foreign = False
    payload = get_payload(request, True)
    if payload != None and payload.get("id") == "foreign":
        foreign = True

    # Check if the post is friends only
    if post.visibility == "FRIENDS":
        # Deny access to foreign node users
        if foreign:
            response.status_code = 401
            return response

        # Check if the current user is a friend of the author
        try:
            token = request.COOKIES.get('jwt')
            # Request was not authenticated without a token
            if not token:
                token = request.headers['Authorization']
                if not token:
                    response.status_code = 401
                    return response
            viewerId = uuid.UUID(jwt.decode(token, key='secret', algorithms=['HS256'])["id"])
            followRequests = FollowRequest.objects.filter(Q(actor__exact=authorId) | Q(object__exact=authorId)).filter(accepted__exact=True).filter(Q(actor__exact=viewerId) | Q(object__exact=viewerId))
            if len(followRequests) <= 0:
                response.status_code = 401
                return response
        except KeyError:
            response.status_code = 401
            return response

    # Check if post is viewable by single author only
    if post.viewableBy != '':
        # Deny access to foreign node users
        if foreign:
            response.status_code = 401
            return response

        try:
            token = request.COOKIES.get('jwt')
            # Request was not authenticated without a token
            if not token:
                token = request.headers['Authorization']
                if not token:
                    response.status_code = 401
                    return response
            viewerId = uuid.UUID(jwt.decode(token, key='secret', algorithms=['HS256'])["id"])
            if viewerId != uuid.UUID(post.viewableBy) and viewerId != post.author_id:
                response.status_code = 401
                return response
        except KeyError:
            response.status_code = 401
            return response
    
    # Check if the post is an image post
    if post.contentType != "application/base64" and post.contentType != "image/png;base64" and post.contentType != "image/jpeg;base64":
        response.status_code = 404
        return response

    # Return the response
    response.status_code = 200
    response.content = base64.b64decode(post.content)
    return response

# Returns the post object if found, otherwise returns None
def find_post(id, authorId):
    # Find the post with the given id
    print(env("LOCAL_HOST") + "/authors/" + authorId + "/posts/" + id)
    try:
        return Post.objects.get(id=env("LOCAL_HOST") + "/authors/" + authorId + "/posts/" + id)
    except ObjectDoesNotExist:
        return None
