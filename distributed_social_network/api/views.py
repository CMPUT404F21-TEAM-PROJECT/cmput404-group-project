from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse, HttpResponse
from .models import Author, Like
from .serializers import AuthorSerializer, LikeSerializer


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


##################### START LIKE VIEWS ##################### 

'''
LIKE

You can like posts and comments
Send them to the inbox of the author of the post or comment

URL: ://service/authors/{AUTHOR_ID}/inbox/
    POST [local, remote]: send a like object to AUTHOR_ID
URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes
    GET [local, remote] a list of likes from other authors on AUTHOR_ID's post POST_ID
URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes
    GET [local, remote] a list of likes from other authors on AUTHOR_ID's post POST_ID comment COMMENT_ID

'''

'''
LIKED

URL: ://service/authors/{AUTHOR_ID}/liked
    GET [local, remote] list what public things AUTHOR_ID liked.

It's a list of of likes originating from this author
Note: be careful here private information could be disclosed.
'''



# The @api_view decorator will wrap the view so that only HTTP methods that are listed in the decorator will get executed.
@api_view(["POST"])
def send_like(request, authorID):
    serializer = LikeSerializer(data = request.data)
    response = HttpResponse()

    if find_author(authorID) is None: 
        # If author not found, return 404
        response.status_code = 404  
    else:
        if serializer.is_valid():
            # If given data is valid, save the object to the database
            serializer.save()
            response.status_code = 201
        else:
            # If the data is not valid, do not save the object to the database
            response.status_code = 400
        
    return response
  
@api_view(["GET"])
def get_post_likes(authorID, postID):
    response = HttpResponse()

    # Find the author and post with the given id's
    author = find_author(authorID)
    post = find_post(postID)
    if author is None or post is None:
        response.status_code = 404
        return response

    # authors/<str:authorID>/posts/<str:postID>/likes
    # "object":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
    queryString = "{0}/posts/{1}".format(authorID, postID)
    likes = Like.objects.filter(object_contains = queryString)  

    #TODO make sure empty likes doesnt cause issues
    serializer = LikeSerializer(likes, many=True)
    responseDict = serializer.data

    # Return the response
    response = JsonResponse(responseDict)
    response.status_code = 200
    return response

@api_view(["GET"])
def get_comment_likes(authorID, postID, commentID):
    response = HttpResponse()

    # Find the author, post, and comment with the given id's
    author = find_author(authorID)
    post = find_post(postID)
    comment = find_comment(commentID)
    if author is None or post is None or comment is None:
        response.status_code = 404
        return response

    # authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes
    # "object":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
    queryString = "{0}/posts/{1}/comments/{2}".format(authorID, postID, commentID)
    likes = Like.objects.filter(object_contains = queryString)  

    #TODO make sure empty likes doesnt cause issues
    serializer = LikeSerializer(likes, many=True)
    responseDict = serializer.data

    # Return the response
    response = JsonResponse(responseDict)
    response.status_code = 200
    return response

#TODO check that private info is not disclosed
@api_view(["GET"])
def get_author_likes(authorID):
    response = HttpResponse()

    # Find the author, post, and comment with the given id's
    author = find_author(authorID)
    if author is None:
        response.status_code = 404
        return response

    # authors/{AUTHOR_ID}/liked
    # "object":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
    # queryString has "authors/" to prevent authorID being potentially matched with a post or comment with the same ID.
    queryString = "authors/{}".format(authorID)
    likes = Like.objects.filter(object_contains = queryString)  

    #TODO make sure empty likes doesnt cause issues
    serializer = LikeSerializer(likes, many=True)
    responseDict = serializer.data

    # Return the response
    response = JsonResponse(responseDict)
    response.status_code = 200
    return response


# Returns Post object if found, otherwise returns None
def find_post(id):
    return None # TODO Remove once Post is implmented 
    
    try:
        return Post.objects.get(id=id)
    except ObjectDoesNotExist:
        return None


# Returns Comment object if found, otherwise returns None
def find_comment(id):
    return None # TODO Remove once Comment is implmented 
    
    try:
        return Comment.objects.get(id=id)
    except ObjectDoesNotExist:
        return None





##################### END LIKE VIEWS #####################