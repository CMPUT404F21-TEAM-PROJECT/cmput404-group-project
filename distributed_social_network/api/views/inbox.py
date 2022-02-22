from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
import jwt
from ..models import Inbox
from ..serializers import InboxSerializer

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

# Routes the request for inbox
@api_view(['GET', 'POST', 'DELETE'])
def route_inbox(request, author_id):
    if request.method == 'GET':
        return get_inbox(request, author_id)
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass

# Get author_id's inbox
def get_inbox(author_id):
    response = HttpResponse()
    try:
        inbox = Inbox.objects.get(author=author_id)
    except ObjectDoesNotExist:
        response.status_code = 404
        return response

    # Check authorization
    try:
        cookie = request.COOKIES['jwt']
        viewerId = jwt.decode(cookie, key='secret', algorithms=['HS256'])["id"]
        if not (str(inbox.author) == viewerId):
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

    response = JsonResponse(responseDict)
    response.status_code = 200
    return response
