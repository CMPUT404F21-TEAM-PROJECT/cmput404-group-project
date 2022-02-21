from rest_framework.decorators import api_view

# Routes the request for a single author
@api_view(['DELETE', 'POST', 'GET'])
def route_single_author(request, author_id):
    if request.method == 'DELETE':
        return delete_author(request, author_id)
    elif request.method == 'POST':
        return update_author(request, author_id)
    elif request.method == 'GET':
        return get_single_author(request, author_id)

# Routes the request for multiple authors
@api_view(['POST', 'GET'])
def route_multiple_authors(request):
    if request.method == 'POST':
        return add_author(request)
    elif request.method == 'GET':
        return get_multiple_authors(request)

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
        return create_post(request, post_id)

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
