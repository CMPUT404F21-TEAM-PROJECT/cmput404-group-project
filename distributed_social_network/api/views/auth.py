import jwt, datetime
from rest_framework.decorators import api_view
from django.http import HttpResponse
from ..models import User
from ..serializers import AuthorSerializer, UserSerializer


# Authenticates a request and returns the user id to be used within the apis
def get_user_id(request):
    token = request.COOKIES.get('jwt')
    # Request was not authenticated without a token
    if not token:
        return None
    
    # Check whether the access token has expired
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    
    user = User.objects.filter(id=payload['id']).first()
    serializer = UserSerializer(user)

    return serializer.data['id']

# Creates a new user object and their respective author object
@api_view(['POST'])
def create_new_user(request):
    response = HttpResponse()
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        response.status_code = 201
        response.content = "New user created successfully"
        # Serialize a new Author object
        try:
            authorDict = {'id': serializer.data['id'], 'displayName': serializer.data['username']}
            author_serializer = AuthorSerializer(data = authorDict)

            # If given data is valid, save the object to the database
            if author_serializer.is_valid():
                author_serializer.save()
        except:
            response.status_code = 400
            response.content = "Error while serializing the author"
    else:
        response.status_code = 400
        response.content = "Error occurred during serialization"

    return response

# Logs in a new user and returns a jwt access token for authentication
@api_view(['POST'])
def login_user(request):
    response = HttpResponse()
    # Parse username and password from request to user for logging in
    username = request.data['username']
    password = request.data['password']
    
    # Finds user from database
    user = User.objects.filter(username=username).first()
    
    # Check if user exists within the database
    if not user:
        response.status_code = 404
        response.content = "Error 404: User was not found"
        return response

    # Checks the provided password with the hashed one
    if not user.check_password(password):
        response.status_code = 401
        response.content = "Error 401: Incorrect Password"
        return response

    
    # Creates an access token that lasts for one hour
    payload = {
        'id': str(user.id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')
    responseDict = {'jwt' : token}

    response = HttpResponse()
    response.status_code = 201
    response.content = "User successfully logged in"
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = responseDict

    return response