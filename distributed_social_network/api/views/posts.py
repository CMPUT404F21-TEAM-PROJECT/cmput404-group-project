from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from ..serializers import PostSerializer
from rest_framework.pagination import PageNumberPagination
import base64, jwt
from ..models import Post
from rest_framework.decorators import api_view

# Routes the request for a single post
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def route_single_post(request, author_id, post_id):
    if request.method == 'GET':
        return get_post(request, post_id)
    elif request.method == 'POST':
        return update_post(request, post_id)
    elif request.method == 'DELETE':
        return delete_post(request, post_id)
    elif request.method == 'PUT':
        return create_post_with_id(request, post_id)

# Routes the request for multiple posts
@api_view(['POST', 'GET'])
def route_multiple_posts(request, author_id):
    if request.method == 'POST':
        return create_post(request)
    elif request.method == 'GET':
        return get_multiple_posts(request)

# Routes the request for a single image post
@api_view(['GET'])
def route_single_image_post(request, author_id, post_id):
    if request.method == 'GET':
        return get_post_image(request, post_id)

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
    print(serializer.errors)

    # If the data is not valid, do not save the object to the database
    response.status_code = 400
    return response

# Adds a new post to the database.
# Expects JSON request body with post attributes.
def create_post_with_id(request, id):
    # Use the given id
    request.data["id"] = id
    
    # Serialize a new Post object
    serializer = PostSerializer(data = request.data)

    response = HttpResponse()

    # If given data is valid, save the object to the database
    if serializer.is_valid():
        serializer.save()
        response.status_code = 201
        return response
    print(serializer.errors)

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

    # Check authorization
    try:
        cookie = request.COOKIES['jwt']
        deleterId = jwt.decode(cookie, key='secret', algorithms=['HS256'])["id"]
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
def update_post(request, id):
    response = HttpResponse()

    # Use the given id
    request.data["id"] = id

    # Find the post with the given id
    post = find_post(id)
    if post == None:
        response.status_code = 404
        return response

    # Check authorization
    try:
        cookie = request.COOKIES['jwt']
        updaterId = jwt.decode(cookie, key='secret', algorithms=['HS256'])["id"]
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

# Get the image post with id 'id' in the database and return a binary response
def get_post_image(request, id):
    response = HttpResponse()

    # Find the post with the given id
    post = find_post(id)
    if post == None:
        response.status_code = 404
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
def find_post(id):
    # Find the post with the given id
    try:
        return Post.objects.get(id=id)
    except ObjectDoesNotExist:
        return None